# Deployment Guide

This guide covers deploying the Customer Service Support System to free cloud platforms.

## Quick Overview

- **Frontend**: Deploy to Netlify (static site, super easy)
- **Backend**: Deploy to Render or Railway (both have free tiers)

## Frontend Deployment (Netlify)

Netlify is perfect for the static frontend - it's free and takes about 2 minutes.

### Steps

1. Go to [netlify.com](https://netlify.com) and sign in with GitHub

2. Click "Add new site" → "Import an existing project"

3. Select your GitHub repository

4. Configure settings:
   - **Build command**: Leave empty (it's already configured in netlify.toml)
   - **Publish directory**: `frontend`

5. Click "Deploy site"

That's it! Netlify will give you a URL like `https://yoursite.netlify.app`

The frontend is already configured to connect to the backend at the Render URL.

## Backend Deployment (Render)

Render has a free tier with 750 hours/month. Note that it has 512MB RAM which can be tight for the ML model.

### Steps

1. Go to [render.com](https://render.com) and sign in with GitHub

2. Click "New +" → "Web Service"

3. Connect your GitHub repository

4. Configure:
   - **Name**: customer-service-backend (or whatever you want)
   - **Region**: Choose closest to you
   - **Branch**: main (or your branch name)
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn api.main:app --host 0.0.0.0 --port $PORT`

5. Add environment variables:
   - `ANTHROPIC_API_KEY`: Your API key from Anthropic
   - `PYTHON_VERSION`: 3.11.0
   - `ENVIRONMENT`: production

6. Click "Create Web Service"

7. Wait for deployment (5-10 minutes first time)

### Getting Your URL

Once deployed, Render gives you a URL like `https://yourservice.onrender.com`

Test it: `https://yourservice.onrender.com/health` should return `{"status":"healthy"}`

### Known Limitation

Render's free tier (512MB RAM) can struggle with the HuggingFace embedding model (~350MB). If you experience timeouts:
- Upgrade to Starter plan ($7/month, 2GB RAM)
- Or try Railway (8GB free tier)

## Alternative: Railway

Railway has 8GB RAM on free tier (500 hours/month), which is plenty for this app.

### Steps

1. Go to [railway.app](https://railway.app) and sign in with GitHub

2. Click "+ New Project" → "Deploy from GitHub repo"

3. Select your repository

4. Railway will detect the Dockerfile automatically

5. Add environment variables:
   - `ANTHROPIC_API_KEY`: Your API key
   - `PORT`: 8000

6. Click "Deploy"

7. After deployment, go to Settings → Networking → Generate Domain

That's it! Railway's 8GB RAM should handle everything smoothly.

## Updating the Frontend

If you deploy the backend to a different URL, update `frontend/app.js`:

```javascript
const API_URL = window.location.hostname === 'localhost'
  ? 'http://localhost:8000'
  : window.location.hostname.includes('127.0.0.1')
    ? 'http://localhost:8000'
    : 'https://your-backend-url.com';  // Update this line
```

Commit and push - Netlify will auto-redeploy.

## Testing Your Deployment

### Backend Health Check
```bash
curl https://your-backend-url.com/health
```

Expected: `{"status":"healthy"}`

### Full Test
1. Visit your frontend URL
2. Enter a name
3. Ask a question (e.g., "How do I reset my password?")
4. Should get a response in 5-15 seconds

### Troubleshooting

**Backend timeout on first query**
- This is normal - the HuggingFace model downloads on first use
- Subsequent queries will be fast

**500 Error**
- Check your API key is set correctly in environment variables
- Look at backend logs in Render/Railway dashboard

**CORS Error**
- Make sure backend URL in frontend/app.js is correct
- Backend is configured to allow all origins

## Monitoring

Both Render and Railway have dashboards where you can:
- View logs in real-time
- Check memory/CPU usage
- See deployment history
- Monitor uptime

For production use, consider setting up monitoring with UptimeRobot (free) to keep the service from sleeping.

## Cost Summary

| Service | Plan | Cost |
|---------|------|------|
| Netlify | Free | $0 |
| Render Free | 750hrs/month | $0 |
| Render Starter | Always-on | $7/month |
| Railway | 500hrs/month | $0 |

The free tiers are fine for demos and light usage. For production with consistent traffic, the Render Starter plan or Railway's paid tier are worth it.
