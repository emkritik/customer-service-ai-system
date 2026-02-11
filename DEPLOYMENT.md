# Deployment Guide - Render

## Prerequisites
- GitHub account
- Render account (free tier)
- Anthropic API key

## Deployment Steps

### 1. Prepare Repository
```bash
# Ensure all changes committed
git add .
git commit -m "Production ready"
git push origin main
```

### 2. Deploy Backend on Render

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Configure:
   - **Name**: customer-service-backend
   - **Region**: Oregon (or closest to you)
   - **Branch**: main
   - **Root Directory**: (leave empty)
   - **Environment**: Python 3
   - **Build Command**: 
     ```
     pip install -r backend/requirements.txt && cd backend && python init_rag.py
     ```
   - **Start Command**:
     ```
     cd backend && uvicorn api.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan**: Free

5. Add Environment Variables:
   - `ANTHROPIC_API_KEY` = your-key-here
   - `PYTHON_VERSION` = 3.11.0
   - `ENVIRONMENT` = production

6. Add Persistent Disk:
   - Name: data-disk
   - Mount Path: `/opt/render/project/src/backend`
   - Size: 1 GB

7. Click "Create Web Service"
8. Wait for deployment (5-10 minutes first time)
9. **Copy your backend URL**: `https://YOUR-APP.onrender.com`

### 3. Deploy Frontend on Render

1. Click "New +" → "Static Site"
2. Connect same GitHub repository
3. Configure:
   - **Name**: customer-service-frontend
   - **Branch**: main
   - **Publish Directory**: `frontend`
   - **Build Command**: (leave empty)

4. Click "Create Static Site"
5. **Copy your frontend URL**: `https://YOUR-FRONTEND.onrender.com`

### 4. Update Frontend API URL

Edit `frontend/app.js`:
```javascript
const API_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:8000'
  : 'https://YOUR-BACKEND-NAME.onrender.com';  // UPDATE THIS
```

Commit and push - frontend will auto-redeploy.

### 5. Test Production

1. Visit frontend URL
2. Enter name and question
3. Verify answer appears
4. Check response time

### 6. View Logs

1. Go to Render dashboard
2. Click backend service
3. Click "Logs" tab
4. See real-time logs

## Troubleshooting

**Cold starts**: First request after inactivity takes 30-60s (free tier limitation)

**Build fails**: Check that all PDFs are in `knowledge_base/` folder

**API errors**: Verify `ANTHROPIC_API_KEY` is set correctly in Render

**Database issues**: Ensure persistent disk is mounted

## URLs
- **Frontend**: https://your-frontend.onrender.com
- **Backend**: https://your-backend.onrender.com
- **API Docs**: https://your-backend.onrender.com/docs

## Performance Monitoring

Monitor response times in the logs. Look for lines like:
```
=== QUERY COMPLETE === Response time: 7500ms
```

Expected performance:
- **Local**: 4-8 seconds
- **Production (Render Free)**: 8-12 seconds (due to cold starts)
- **Production (Warmed up)**: 4-8 seconds

## Maintenance

### Updating the Deployment

1. Make changes locally
2. Test locally
3. Commit and push to GitHub
4. Render will automatically redeploy

### Viewing Database

Database is stored in the persistent disk. To view data:
1. Go to Render dashboard
2. Click on your service
3. Click "Shell" tab
4. Run: `sqlite3 data/customer_service.db`
5. Run SQL: `SELECT * FROM queries ORDER BY timestamp DESC LIMIT 10;`

### Monitoring Costs

Render free tier includes:
- 750 hours/month compute time
- 1 GB persistent disk
- Automatic sleep after 15 min inactivity

**Note**: Cold starts add 30-60s to first request after sleep.

## Security Notes

- Never commit `.env` files
- Keep `ANTHROPIC_API_KEY` in Render environment variables only
- API key is loaded from environment using `python-dotenv`
- All secrets are excluded via `.gitignore`

## Vercel Frontend Deployment

### Why Vercel?
- Optimized for static sites
- Global CDN (fast worldwide)
- No cold starts
- Free tier generous
- Instant deployment

### Steps

1. **Sign up for Vercel**
   - Go to https://vercel.com
   - Click "Sign Up"
   - Choose "Continue with GitHub"
   - Authorize Vercel

2. **Deploy Frontend**
   - Click "New Project"
   - Import your GitHub repository
   - Configure:
     * Framework Preset: Other
     * Root Directory: `frontend`
     * Build Command: (leave empty)
     * Output Directory: (leave empty)
   - Click "Deploy"

3. **Verify Deployment**
   - After deployment completes, click "Visit" to open your site
   - Your frontend is now live with automatic HTTPS
   - Frontend is already configured to use: `https://customer-service-ai-system.onrender.com`

4. **Configure Domain (Optional)**
   - In Vercel dashboard → Settings → Domains
   - Add custom domain if desired

### Testing

1. Visit your Vercel URL
2. Click "Wake Up Backend" (if needed for first use)
3. Submit test query
4. Verify answer appears

### Monitoring

Vercel provides:
- Deployment logs
- Analytics (page views, performance)
- Real-time errors (if any)

Access via: Vercel Dashboard → Your Project → Analytics

### Auto-Deployment

- Push to GitHub → Vercel automatically redeploys
- Preview deployments for pull requests
- Production deployment from main branch

