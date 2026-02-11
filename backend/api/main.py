import os
import time
import json
import re
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import anthropic

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Initialize
from rag.vectorstore import search_knowledge_base
from database.db import init_db, save_query, get_statistics

app = FastAPI(title="Customer Service Support System")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

class QueryRequest(BaseModel):
    question: str
    user_name: str

# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests"""
    start_time = time.time()
    logger.info(f"→ {request.method} {request.url.path}")
    response = await call_next(request)
    duration = int((time.time() - start_time) * 1000)
    logger.info(f"← {request.method} {request.url.path} | {response.status_code} | {duration}ms")
    return response

@app.post("/api/query")
async def process_query(request: QueryRequest):
    """OPTIMIZED: Process query with 2 API calls instead of 3"""

    logger.info(f"=== NEW QUERY ===")
    logger.info(f"User: {request.user_name}")
    logger.info(f"Question: {request.question}")

    start_time = time.time()

    try:
        # STEP 1: Get relevant documents (no LLM call - just vector search)
        logger.info("[Vector Search] Retrieving relevant documents...")
        try:
            # Use cached vectorstore instead of loading fresh each time
            vectorstore = get_or_load_vectorstore()
            retrieved_docs = vectorstore.similarity_search(request.question, k=3)
            context = "\n\n".join([
                f"Source: {doc.metadata['source']} (Page {doc.metadata['page']})\n{doc.page_content}"
                for doc in retrieved_docs
            ])
            sources = [
                {"document": doc.metadata['source'], "page": doc.metadata['page']}
                for doc in retrieved_docs
            ]
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": "Unable to search knowledge base. Please try again.",
                    "error_type": "search_failure"
                }
            )

        # STEP 2: OPTIMIZED - Reformulation + Answer in ONE call
        logger.info("[Agent 1+2 Combined] Reformulating and answering...")
        try:
            combined_prompt = f"""You are a banking customer service AI assistant.

Original Question from Rep: {request.question}

Retrieved Knowledge Base Information:
{context}

Your task:
1. First, identify the true intent and reformulate this into a search-optimized query (5-10 words)
2. Then, provide a clear, accurate answer using the retrieved information

Respond in this exact JSON format:
{{
    "reformulated_query": "your optimized search query here",
    "answer": "your detailed answer here (2-4 sentences)"
}}"""

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=600,
                messages=[{"role": "user", "content": combined_prompt}]
            )

            response_text = message.content[0].text.strip()

            # Extract JSON
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                reformulated_query = result['reformulated_query']
                answer = result['answer']
            else:
                reformulated_query = request.question[:50]
                answer = response_text

            logger.info(f"[Agent 1+2] Reformulated: {reformulated_query}")

        except Exception as e:
            logger.error(f"Reformulation/Answer failed: {e}")
            reformulated_query = request.question
            answer = "I apologize, but I'm having trouble generating an answer right now. Please try again or contact support."

        # STEP 3: Fast validation
        logger.info("[Agent 3] Validating answer...")
        try:
            validation_prompt = f"""Rate answer quality 0-100.
Q: {request.question[:100]}
A: {answer[:200]}
Just respond with a number (0-100):"""

            validation_msg = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=10,
                messages=[{"role": "user", "content": validation_prompt}]
            )

            confidence_text = validation_msg.content[0].text.strip()
            confidence_match = re.search(r'\d+', confidence_text)
            confidence_score = int(confidence_match.group()) if confidence_match else 50
            confidence_score = max(0, min(100, confidence_score))

        except Exception as e:
            logger.error(f"Validation failed: {e}")
            confidence_score = 50

        logger.info(f"[Agent 3] Confidence: {confidence_score}%")

        # Calculate response time
        response_time_ms = int((time.time() - start_time) * 1000)
        logger.info(f"=== QUERY COMPLETE === Response time: {response_time_ms}ms")

        # Save to database
        try:
            source_doc = sources[0]['document'] if sources else "Unknown"
            save_query(
                user_name=request.user_name,
                original_question=request.question,
                reformulated_query=reformulated_query,
                answer=answer,
                confidence_score=confidence_score,
                source_document=source_doc,
                response_time_ms=response_time_ms
            )
        except Exception as e:
            logger.error(f"Database save failed: {e}")

        return {
            "success": True,
            "original_question": request.question,
            "reformulated_query": reformulated_query,
            "answer": answer,
            "confidence_score": confidence_score,
            "sources": sources,
            "response_time_ms": response_time_ms
        }

    except Exception as e:
        logger.error(f"=== QUERY FAILED === {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "An unexpected error occurred. Please try again.",
                "error_type": "internal_error"
            }
        )

@app.get("/api/stats")
async def get_stats():
    """Get dashboard statistics"""
    logger.info("Dashboard stats requested")
    try:
        stats = get_statistics()
        logger.info(f"Returning stats: {stats['total_queries']} total queries")
        return stats
    except Exception as e:
        logger.error(f"Stats failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Customer Service Support System API", "status": "running"}

@app.api_route("/health", methods=["GET", "HEAD"])
async def health():
    return {"status": "healthy"}

@app.get("/warmup")
async def warmup():
    """Warmup endpoint to preload vector store and keep service alive"""
    try:
        logger.info("Warmup request received - preloading vectorstore...")
        vectorstore = get_or_load_vectorstore()
        logger.info("Warmup complete - vectorstore ready")
        return {
            "status": "warm",
            "message": "Vector store loaded and ready",
            "cached": _vectorstore_cache is not None
        }
    except Exception as e:
        logger.error(f"Warmup failed: {e}")
        return {
            "status": "cold",
            "message": "Warmup failed but service is running",
            "error": str(e)
        }

@app.get("/api/pdf/{filename}")
async def get_pdf(filename: str):
    """Serve PDF files from knowledge base"""
    try:
        # Security: Only allow PDF files and prevent directory traversal
        if not filename.endswith('.pdf') or '/' in filename or '\\' in filename:
            raise HTTPException(status_code=400, detail="Invalid filename")

        pdf_path = os.path.join("..", "knowledge_base", filename)

        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=404, detail="PDF file not found")

        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=filename
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "System error. Please try again."
        }
    )

# Global variable to cache the vector store
_vectorstore_cache = None

def get_or_load_vectorstore():
    """Get cached vector store or load it"""
    global _vectorstore_cache
    if _vectorstore_cache is None:
        logger.info("Loading vector store for the first time...")
        from rag.vectorstore import load_vectorstore
        _vectorstore_cache = load_vectorstore()
        logger.info("Vector store loaded and cached")
    return _vectorstore_cache

# Startup/shutdown events
@app.on_event("startup")
async def startup_event():
    logger.info("=" * 60)
    logger.info("Customer Service Support System - STARTING")
    logger.info(f"Environment: {os.environ.get('ENVIRONMENT', 'development')}")
    logger.info("=" * 60)

    # Note: Vector store loads on first request due to Render free tier memory limits
    logger.info("⚠️  First query will take 30-60s (cold start)")
    logger.info("Subsequent queries will be fast (<10s)")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Customer Service Support System - SHUTTING DOWN")
