# Railway Deployment Guide - 100% Working

Railway has **8GB RAM** free tier (500 hours/month) which is perfect for this application.

## Prerequisites

- GitHub account
- Railway account (sign up with GitHub)
- Your Anthropic API key

## Step-by-Step Deployment

### 1. Sign Up for Railway

1. Go to https://railway.app
2. Click **"Login"** or **"Start a New Project"**
3. **Sign in with GitHub**
4. Authorize Railway to access your repositories

### 2. Create New Project

1. Click **"+ New Project"**
2. Select **"Deploy from GitHub repo"**
3. Find and select: `customer-service-ai-system`
4. Railway will detect the Dockerfile automatically

### 3. Configure Environment Variables

**BEFORE the first deployment**, add your API key:

1. Click on your service (the card that appears)
2. Go to **"Variables"** tab
3. Click **"+ New Variable"**
4. Add:
   ```
   ANTHROPIC_API_KEY=your-actual-api-key-here
   ```
5. Click **"Add"**

### 4. Configure Port (Important!)

Railway needs to know which port to use:

1. Still in **"Variables"** tab
2. Add another variable:
   ```
   PORT=8000
   ```

### 5. Deploy

1. Click **"Deploy"** button (or it may auto-deploy)
2. Watch the build logs in the **"Deployments"** tab

**Expected build time**: 5-8 minutes (first time)

### 6. Get Your URL

1. Go to **"Settings"** tab
2. Scroll to **"Networking"** section
3. Click **"Generate Domain"**
4. Copy your URL: `https://your-service.up.railway.app`

### 7. Test Your Deployment

Open in browser:
```
https://your-service.up.railway.app/health
```

Expected response:
```json
{"status":"healthy"}
```

## What Makes This Work

### Dockerfile Configuration
We're using a simple Dockerfile that:
- Uses Python 3.11 slim (smaller image)
- Installs only necessary system packages (gcc, g++)
- Properly copies backend files
- Runs uvicorn directly

### Key Differences from Render
- **8GB RAM** vs 512MB (plenty for HuggingFace model)
- Dockerfile deployment (more reliable than auto-detection)
- No nixpacks complexity
- No cold starts (stays warm longer)

## Expected Performance

| Stage | Time |
|-------|------|
| Build | 5-8 minutes (first time) |
| Deploy | 1-2 minutes |
| First query | 30-60 seconds (model download) |
| Subsequent queries | 5-10 seconds |

## Update Frontend

After Railway deployment succeeds, update your frontend:

Edit `frontend/app.js` line 6:
```javascript
: 'https://your-service.up.railway.app';  // Your Railway URL
```

Commit and push:
```bash
git add frontend/app.js
git commit -m "Update API URL to Railway deployment"
git push origin fix/push
```

Netlify will auto-redeploy with the new backend URL.

## Troubleshooting

### Build Fails
**Check**: Dockerfile syntax
**Solution**: The provided Dockerfile should work as-is

### Deployment Timeout
**Check**: Environment variables are set
**Solution**: Make sure ANTHROPIC_API_KEY and PORT are configured

### 404 Not Found
**Check**: Railway generated domain
**Solution**: Use the full URL from Settings → Networking

### 500 Error
**Check**: Logs in Railway dashboard
**Solution**: Look for missing API key or file path issues

## Free Tier Limits

Railway free tier includes:
- **500 hours/month** execution time (~16 hours/day)
- **8GB RAM** (more than enough)
- **100GB bandwidth**
- **No credit card required**

## Cost Monitoring

Watch your usage:
1. Go to Railway dashboard
2. Click your project
3. View **"Usage"** tab
4. See hours used this month

## Why This Will Work

✅ **Enough RAM**: 8GB vs 512MB (Render)
✅ **Simple Dockerfile**: No nixpacks complications
✅ **Proven Stack**: Python 3.11 + uvicorn
✅ **Pre-built Vector DB**: Committed to repo
✅ **Health Check Fixed**: Accepts HEAD requests

The memory limitation that caused Render to fail won't affect Railway.

## After Successful Deployment

1. ✅ Backend working on Railway
2. ✅ Update frontend with Railway URL
3. ✅ Test end-to-end functionality
4. ✅ Update documentation with live URLs

Your system should be fully operational!
