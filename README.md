# Customer Service Support System

AI-powered customer service assistant using multi-agent RAG pipeline with Claude.

## Architecture

**User Question → Reformulation Agent → Search Agent (RAG) → Validation Agent → Response**

The system uses three sequential AI agents to process customer service queries:

1. **Reformulation Agent**: Analyzes the question and reformulates it into an optimized search query
2. **Search Agent**: Retrieves relevant information from the knowledge base (RAG) and generates an answer
3. **Validation Agent**: Evaluates the answer quality and assigns a confidence score

## Features

- Multi-agent orchestration with Claude Sonnet 4.5
- RAG system with vector embeddings (ChromaDB + HuggingFace)
- Rep View UI for customer service representatives
- Manager Dashboard with analytics and statistics
- SQLite database tracking all queries
- Confidence scoring with visual indicators
- Source document attribution
- Response time tracking

## Setup Instructions

### 1. Prerequisites

- Python 3.9+
- Anthropic API key

### 2. Installation

```bash
# Navigate to project directory
cd "Costumer Service Support System"

# Install backend dependencies
cd backend
pip install -r requirements.txt
```

### 3. Configuration

Set your Anthropic API key as an environment variable:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

On Windows:
```cmd
set ANTHROPIC_API_KEY=your-api-key-here
```

### 4. Add Knowledge Base

Place your 8 banking PDF files in the `knowledge_base/` directory. The system will automatically:
- Extract text from all PDFs
- Split content into chunks
- Create vector embeddings
- Build a searchable knowledge base

### 5. Initialize System

Run the initialization script to set up the database and vector store:

```bash
cd backend
python init_rag.py
```

This will:
- Create the SQLite database
- Load all PDFs from knowledge_base/
- Generate embeddings using sentence-transformers
- Build the ChromaDB vector store
- Verify the setup is complete

### 6. Start Backend

```bash
# From the backend directory
uvicorn api.main:app --reload --port 8000
```

The API will be available at [http://localhost:8000](http://localhost:8000)

### 7. Open Frontend

**Option 1: Direct file open**
- Open [frontend/index.html](frontend/index.html) directly in your web browser

**Option 2: Simple HTTP server**
```bash
cd frontend
python -m http.server 8080
```
Then visit [http://localhost:8080](http://localhost:8080)

## Testing the System

### Example Questions to Try

1. **"Customer is yelling that money was stolen from his card"**
   - Tests fraud/dispute handling
   - Should retrieve fraud security documentation
   - Expected: Information about unauthorized charge disputes

2. **"What's the fee if account goes below minimum balance?"**
   - Tests fee policy queries
   - Should retrieve fees and refunds documentation
   - Expected: Specific fee amounts and conditions

3. **"Customer can't log into mobile app"**
   - Tests technical troubleshooting
   - Should retrieve app troubleshooting guide
   - Expected: Step-by-step login assistance

4. **"How long does it take to get a mortgage?"**
   - Tests loan information queries
   - Should retrieve loans and mortgages documentation
   - Expected: Timeline information for mortgage processing

### Understanding Results

**Reformulated Query**: Shows how the system optimized your question for searching the knowledge base

**Confidence Score**:
- **Green (90-100%)**: High confidence - answer is accurate and complete
- **Yellow (70-89%)**: Medium confidence - answer is good but may lack some details
- **Red (0-69%)**: Low confidence - verify answer carefully before using

**Sources**: Shows which PDF document and page the information came from

## Demo Script

1. Show the Rep View interface
2. Enter representative name (e.g., "John Smith")
3. Enter a customer question
4. Click "Get Answer" and observe the processing
5. Point out the reformulated query that appears
6. Review the generated answer
7. Highlight the confidence score with color coding
8. Show the source document reference
9. Switch to Manager Dashboard
10. Show statistics updating in real-time
11. Highlight low-confidence queries for review

## Project Structure

```
customer-service-system/
├── backend/
│   ├── agents/                  # AI Agents
│   │   ├── reformulation_agent.py
│   │   ├── search_agent.py
│   │   └── validation_agent.py
│   ├── rag/                     # RAG System
│   │   ├── document_loader.py
│   │   └── vectorstore.py
│   ├── database/                # Database Layer
│   │   ├── db.py
│   │   └── models.py
│   ├── api/                     # FastAPI Backend
│   │   └── main.py
│   ├── init_rag.py             # Initialization Script
│   └── requirements.txt
├── frontend/                    # Web UI
│   ├── index.html              # Rep View
│   ├── dashboard.html          # Manager Dashboard
│   ├── app.js                  # Frontend Logic
│   └── styles.css              # Styling
├── knowledge_base/             # PDF Documents (user-provided)
├── chroma_db/                  # Vector Database (auto-created)
├── data/                       # SQLite Database (auto-created)
│   └── customer_service.db
└── README.md
```

## API Endpoints

### POST /api/query
Process a customer service query through the 3-agent pipeline.

**Request:**
```json
{
  "question": "Customer wants to know about overdraft fees",
  "user_name": "John Smith"
}
```

**Response:**
```json
{
  "success": true,
  "original_question": "Customer wants to know about overdraft fees",
  "reformulated_query": "overdraft fee policy charges amount",
  "answer": "Overdraft fees are $35 per transaction...",
  "confidence_score": 92,
  "sources": [
    {"document": "fees_and_charges.pdf", "page": 3}
  ],
  "response_time_ms": 2847
}
```

### GET /api/stats
Get dashboard statistics.

**Response:**
```json
{
  "total_queries": 127,
  "avg_confidence": 86.3,
  "active_reps": 8,
  "avg_response_time": 2456,
  "user_stats": [...],
  "document_stats": [...],
  "low_confidence_queries": [...]
}
```

## Troubleshooting

### "Vector store not found" error
- Make sure you ran `python init_rag.py` first
- Check that the `chroma_db/` directory was created

### "No PDF files found" error
- Verify your PDF files are in the `knowledge_base/` directory
- Ensure files have `.pdf` extension

### "API connection failed" in frontend
- Ensure backend is running on port 8000
- Check that ANTHROPIC_API_KEY environment variable is set
- Verify no other service is using port 8000

### Low confidence scores
- PDFs may not contain relevant information for the question
- Try more specific questions related to your document content
- Check that the reformulated query is appropriate
- Verify PDFs were loaded correctly during initialization

### Agent errors
- Ensure ANTHROPIC_API_KEY is valid and has sufficient credits
- Check internet connection for API calls
- Review backend console for detailed error messages

## Technical Details

### RAG Pipeline
- **Embeddings**: HuggingFace sentence-transformers/all-MiniLM-L6-v2
- **Vector Store**: ChromaDB with persistent storage
- **Chunk Size**: 500 characters with 50-character overlap
- **Retrieval**: Top 3 most relevant chunks per query

### Agents
- **Model**: Claude Sonnet 4.5 (claude-sonnet-4-20250514)
- **Reformulation**: 100 max tokens
- **Search/Answer**: 500 max tokens
- **Validation**: 50 max tokens

### Database Schema
- Stores: timestamp, user_name, original_question, reformulated_query, answer, confidence_score, source_document, response_time_ms
- Enables: analytics, low-confidence tracking, usage statistics

## System Requirements

- Python 3.9 or higher
- 4GB RAM minimum (8GB recommended for large PDFs)
- 1GB disk space for dependencies and vector database
- Internet connection for API calls

## License

This is a demonstration project for educational purposes.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Verify all setup steps were completed
3. Check backend console logs for error details
4. Ensure API key is valid and has credits
