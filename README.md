# Customer Service Support System

An AI-powered assistant that helps customer service representatives answer questions by searching through a knowledge base of documents and generating accurate responses.

**Live Demo**: https://constumer-service-ai.netlify.app/

## Overview

This system uses a multi-agent RAG (Retrieval-Augmented Generation) architecture with Claude Sonnet 4.5 to provide intelligent customer service responses. It searches through PDF documents, finds relevant information, and generates well-sourced answers with confidence scores.

## Features

- **Smart Search**: Finds relevant information from PDF knowledge base
- **AI-Generated Answers**: Uses Claude to create clear, accurate responses
- **Source Citations**: Shows which documents informed each answer
- **Confidence Scoring**: Indicates reliability of responses
- **Clean Interface**: Simple, intuitive design for quick queries

## Tech Stack

**Backend**
- Python 3.11 with FastAPI
- LangChain for RAG pipeline
- ChromaDB for vector storage
- Claude Sonnet 4.5 API
- HuggingFace embeddings

**Frontend**
- Vanilla JavaScript
- HTML5/CSS3
- No frameworks (keep it simple)

**Deployment**
- Frontend: Netlify
- Backend: Render/Railway
- Both on free tiers

## Getting Started

### Prerequisites

- Python 3.11+
- Anthropic API key ([get one here](https://console.anthropic.com/))
- Git

### Local Setup

1. Clone the repository
```bash
git clone https://github.com/emkritik/customer-service-ai-system.git
cd customer-service-ai-system
```

2. Set up backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

3. Run backend
```bash
uvicorn api.main:app --reload --port 8000
```

4. Run frontend (new terminal)
```bash
cd frontend
python -m http.server 3000
```

5. Visit http://localhost:3000

## Project Structure

```
.
├── backend/
│   ├── api/                 # FastAPI endpoints
│   ├── rag/                 # RAG pipeline logic
│   ├── database/            # Query logging
│   ├── chroma_db/           # Vector database
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── styles.css
└── knowledge_base/          # PDF documents
```

## How It Works

1. **User asks a question** through the web interface
2. **Vector search** finds relevant document chunks from the knowledge base
3. **Claude processes** the question with the context from documents
4. **System validates** the answer for accuracy
5. **Response shown** with sources and confidence score

## Architecture

The system uses a streamlined 2-agent design:
- **Agent 1**: Reformulates query + generates answer (combined for efficiency)
- **Agent 2**: Validates response accuracy (quick check)

This reduces API calls and improves response time compared to traditional 3-agent setups.

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions to Render or Railway.

**Note**: The backend requires decent RAM (2GB+) for the HuggingFace embedding model. Free tier limitations on some platforms may affect initialization.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

MIT License - see LICENSE file for details

## Acknowledgments

Built with Claude Sonnet 4.5, LangChain, and FastAPI.
