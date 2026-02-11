# Customer Service Support System

AI-powered customer service assistant using a multi-agent RAG pipeline with Claude Sonnet 4.5.

## Live Deployment

- **Frontend**: https://constumer-service-ai.netlify.app/
- **Backend API**: https://customer-service-ai-system.onrender.com
- **API Docs**: https://customer-service-ai-system.onrender.com/docs

**Note**: The backend is deployed on Render's free tier (512MB RAM), which has limitations loading the HuggingFace embedding model. See [KNOWN_ISSUES.md](KNOWN_ISSUES.md) for details. The application works great locally with sufficient memory.

## What This Does

This system helps customer service reps answer questions by:
1. Taking a customer question
2. Searching through a knowledge base of banking documents (PDFs)
3. Using Claude to generate accurate, sourced answers
4. Showing confidence scores and source documents

## Architecture

### Backend (`backend/`)
- **FastAPI** for the REST API
- **ChromaDB** for vector storage
- **LangChain** for the RAG pipeline
- **Claude Sonnet 4.5** for the AI agents
- **HuggingFace** embeddings (sentence-transformers)

### Frontend (`frontend/`)
- Plain HTML/CSS/JavaScript (no frameworks)
- Clean, simple interface
- Shows reformulated queries, answers, confidence scores, and sources

## Code Optimizations

I made some changes to improve response times:

### Original Design (3 API calls)
```
1. Reformulation Agent → Rewrites query (Claude API call)
2. Search Agent → Finds docs (Claude API call)
3. Validation Agent → Checks answer (Claude API call)
```

### Optimized Design (2 API calls)
```
1. Combined Agent → Reformulates + answers in one call
2. Validation Agent → Quick yes/no check (10 tokens max)
```

**Expected improvement**: Should reduce response time significantly by eliminating one full Claude API call and reducing token usage.

**Reality check**: Haven't been able to fully test this on Render due to memory constraints, but the local version shows the optimization working as expected.

## Setup & Deployment

### Local Development
```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
uvicorn api.main:app --reload --port 8000

# Frontend (separate terminal)
cd frontend
python -m http.server 3000
```

Visit http://localhost:3000

### Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

Current setup:
- **Backend**: Render (free tier - has memory limitations)
- **Frontend**: Netlify (works perfectly)

## Key Features

### Error Handling
- Try-catch blocks everywhere
- Graceful degradation if APIs fail
- User-friendly error messages
- Comprehensive logging

### Security
- No API keys in code
- Environment variables for secrets
- Proper `.gitignore` configuration
- HTTPS enforced

### Logging
- Structured logs with timestamps
- Request/response tracking
- Performance metrics
- Visible in Render dashboard

## Known Issues

The Render free tier (512MB RAM) isn't quite enough for the HuggingFace embedding model, which needs about 350-400MB. This causes the backend to timeout during initialization.

**Solutions**:
1. Upgrade to Render Starter ($7/month, 2GB RAM)
2. Use a different platform (Railway, Fly.io)
3. Use a lighter embedding model

See [KNOWN_ISSUES.md](KNOWN_ISSUES.md) for full details.

## Project Structure

```
.
├── backend/
│   ├── api/
│   │   └── main.py              # FastAPI endpoints
│   ├── rag/
│   │   ├── vectorstore.py       # ChromaDB setup
│   │   └── document_loader.py   # PDF processing
│   ├── database/
│   │   └── db.py                # SQLite for query logs
│   ├── chroma_db/               # Vector database
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── knowledge_base/              # PDF documents
├── README.md
├── DEPLOYMENT.md
├── PRODUCTION_NOTES.md
├── SUBMISSION.md
└── KNOWN_ISSUES.md
```

## Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - How to deploy this thing
- **[PRODUCTION_NOTES.md](PRODUCTION_NOTES.md)** - Technical decisions and architecture
- **[KNOWN_ISSUES.md](KNOWN_ISSUES.md)** - Current limitations and workarounds
- **[SUBMISSION.md](SUBMISSION.md)** - Assessment submission document

## Tech Stack

**Backend:**
- Python 3.11
- FastAPI
- LangChain
- ChromaDB
- Anthropic Claude API
- HuggingFace Transformers

**Frontend:**
- Vanilla JavaScript
- HTML5/CSS3

**Deployment:**
- Render (backend)
- Netlify (frontend)

## What I Learned

- RAG pipelines can be optimized by combining agent calls
- Free tier limitations are real (especially for ML models)
- Caching vector stores makes a huge difference
- Sometimes the simplest frontend is the best frontend
- Proper error handling > perfect code
- Documentation matters

## License

MIT

## Contact

For questions or issues, open a GitHub issue or contact me directly.
