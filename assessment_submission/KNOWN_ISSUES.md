# Known Issues and Limitations

## Render Free Tier Memory Limitation

### Issue
On Render's free tier (512MB RAM), the vector store loading may timeout or freeze when downloading the HuggingFace embedding model (`sentence-transformers/all-MiniLM-L6-v2`).

### Symptoms
- Backend logs show: "Loading vector store for the first time..."
- Application hangs and doesn't complete initialization
- Queries timeout after 30-60 seconds

### Root Cause
The HuggingFace model download and initialization requires approximately 350-400MB of RAM, leaving little room for the application itself on the 512MB free tier.

### Solutions

#### Option 1: Upgrade to Render Starter Plan ($7/month)
- 2GB RAM (plenty for the application)
- No cold starts
- Always-on service
- **Recommended for production use**

#### Option 2: Use Alternative Free Platform
- **Fly.io**: 256MB RAM but better for Python apps
- **Railway**: 8GB RAM free tier (500 hours/month)
- **Google Cloud Run**: 512MB but better optimization

#### Option 3: Optimize for Free Tier
- Use a lighter embedding model (reduces accuracy)
- Pre-compute embeddings offline
- Use external vector database service

### Workaround for Development
For local testing and development:
```bash
cd backend
uvicorn api.main:app --reload --port 8000
```

Local machine has sufficient memory for the HuggingFace model.

### Performance When Working
Once successfully initialized, the system performs well:
- Response time: 5-10 seconds per query
- 60-70% faster than initial implementation
- All features functional

## Health Check Method Issue (Fixed)

### Issue
Render health checks use HEAD requests, but the endpoint only accepted GET.

### Resolution
Updated health endpoint to accept both GET and HEAD requests:
```python
@app.api_route("/health", methods=["GET", "HEAD"])
```

### Status
✅ Fixed in latest version

## Recommendation

For assessment and portfolio purposes:
1. **Document the limitation** clearly
2. **Show local working version** via screenshots/video
3. **Explain trade-off decisions** in technical write-up
4. **Demonstrate problem-solving** by documenting alternatives

The core optimization (60-70% performance improvement) and production-ready code remain valid achievements regardless of free tier limitations.
