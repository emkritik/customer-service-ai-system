from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agents.reformulation_agent import ReformulationAgent
from agents.search_agent import SearchAgent
from agents.validation_agent import ValidationAgent
from database.db import init_db, save_query, get_statistics
import time
import os

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

# Initialize agents
reformulation_agent = ReformulationAgent()
search_agent = SearchAgent()
validation_agent = ValidationAgent()

class QueryRequest(BaseModel):
    question: str
    user_name: str

@app.post("/api/query")
async def process_query(request: QueryRequest):
    """Process customer service query through 3-agent pipeline"""
    try:
        start_time = time.time()

        # Agent 1: Reformulation
        print(f"[Agent 1] Reformulating query...")
        reformulation_result = reformulation_agent.reformulate(request.question)
        reformulated_query = reformulation_result['reformulated_query']

        # Agent 2: Search
        print(f"[Agent 2] Searching knowledge base...")
        search_result = search_agent.search(reformulated_query)
        answer = search_result['answer']
        sources = search_result['sources']
        context = search_result['context']

        # Agent 3: Validation
        print(f"[Agent 3] Validating answer...")
        validation_result = validation_agent.validate(
            request.question,
            answer,
            context
        )
        confidence_score = validation_result['confidence_score']

        # Calculate response time
        response_time_ms = int((time.time() - start_time) * 1000)

        # Save to database
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
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    """Get dashboard statistics"""
    try:
        stats = get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Customer Service Support System API"}

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
        print(f"Error serving PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
