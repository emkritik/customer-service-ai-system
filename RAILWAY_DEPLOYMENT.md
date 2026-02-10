# Complete Railway Deployment Guide

## Why Railway?

Railway is **perfect** for this project:
- ✅ **8GB RAM** (vs Render's 512MB) - No memory issues!
- ✅ **No forced sleep** - Stays responsive
- ✅ **500 hours/month** free tier
- ✅ **Simpler setup** - Less configuration
- ✅ **Faster deploys** - 3-5 minutes

---

## 📋 **Complete Step-by-Step Guide**

### **Step 1: Create Railway Account (2 minutes)**

1. Go to [railway.app](https://railway.app)
2. Click **"Login"** or **"Start a New Project"**
3. **Sign in with GitHub** (recommended)
4. Authorize Railway to access your repositories
5. Verify your email if prompted

---

### **Step 2: Create New Project (1 minute)**

1. Click **"+ New Project"** (big button in dashboard)
2. Select **"Deploy from GitHub repo"**
3. Find and select: `customer-service-ai-system` (or your repo name)
4. Railway will start analyzing the repo
5. Click **"Add variables"** (before deploying!)

---

### **Step 3: Add Environment Variables (2 minutes)**

**CRITICAL**: Do this BEFORE first deployment!

1. You'll see a **"Variables"** section
2. Click **"+ Add Variable"**
3. Add these three variables:

#### Variable 1: API Key
```
Name: ANTHROPIC_API_KEY
Value: sk-ant-api03-YOUR-ACTUAL-KEY-HERE
```
**⚠️ IMPORTANT**: Use your REAL Anthropic API key!

#### Variable 2: Python Version
```
Name: PYTHON_VERSION
Value: 3.11
```

#### Variable 3: Port
```
Name: PORT
Value: 8000
```

4. Click **"Deploy"** button

---

### **Step 4: Configure Build Settings (3 minutes)**

Railway auto-detects Python, but let's verify:

1. After deployment starts, click on your service (the card that appears)
2. Click **"Settings"** tab
3. Scroll to **"Build"** section
4. Verify these settings:

#### Build Command:
```bash
pip install -r backend/requirements.txt
```

#### Start Command:
```bash
cd backend && uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

#### Root Directory:
Leave **empty** (blank)

5. If you need to change anything, click **"Save"**

---

### **Step 5: Wait for Deployment (5-10 minutes)**

**First deployment takes longer** because it:
- Installs Python packages
- Downloads HuggingFace model (~120MB)
- Initializes the vector database

**What you'll see**:
1. **"Building"** - Installing dependencies (2-3 min)
2. **"Deploying"** - Starting the service (1-2 min)
3. **"Active"** (green) - Ready to use!

**Watch the logs**:
- Click **"Deployments"** tab
- Click on the active deployment
- See real-time logs
- Look for: `Customer Service Support System - STARTING`

---

### **Step 6: Get Your URL (1 minute)**

1. Go to **"Settings"** tab
2. Scroll to **"Networking"** section
3. Under **"Public Networking"**:
   - You'll see **"Generate Domain"** button
   - Click it
4. Copy the generated URL:
   ```
   https://your-project-name.up.railway.app
   ```

**Example**: `https://customer-service-ai-system-production.up.railway.app`

---

### **Step 7: Update Frontend (2 minutes)**

Update your frontend to use the Railway backend:

#### Edit `frontend/app.js`:

Find line 5 and replace with your Railway URL:

```javascript
const API_URL = window.location.hostname === 'localhost'
  ? 'http://localhost:8000'
  : window.location.hostname.includes('127.0.0.1')
    ? 'http://localhost:8000'
    : 'https://your-project-name.up.railway.app';  // Your Railway URL
```

**Example**:
```javascript
: 'https://customer-service-ai-system-production.up.railway.app';
```

#### Commit and push:
```bash
git add frontend/app.js
git commit -m "Update API URL to Railway"
git push origin main
```

---

### **Step 8: Deploy Frontend (Optional)**

You have two options:

#### Option A: Netlify (Recommended - Free & Easy)

1. Go to [netlify.com](https://netlify.com)
2. Sign up with GitHub
3. Click **"Add new site"** → **"Import an existing project"**
4. Select your GitHub repo
5. Configure:
   - **Build command**: Leave empty
   - **Publish directory**: `frontend`
6. Click **"Deploy"**
7. Get your URL: `https://your-site.netlify.app`

#### Option B: GitHub Pages (Also Free)

1. Go to your repo on GitHub
2. Click **"Settings"** → **"Pages"**
3. Source: **"Deploy from a branch"**
4. Branch: **main** → Folder: **/frontend**
5. Save
6. URL: `https://yourusername.github.io/repo-name`

---

### **Step 9: Test Your Deployment (5 minutes)**

#### Test Backend Health:

Open in browser:
```
https://your-project.up.railway.app/health
```

**Expected**: `{"status":"healthy"}`

#### Test Warmup Endpoint:

```
https://your-project.up.railway.app/warmup
```

**Expected**: `{"status":"warm","message":"Vector store loaded and ready"}`

#### Test Full Query (Command Line):

```bash
cd "/Users/manoliskritikos/Downloads/Costumer Service Support System"

# Update the URL in test_backend_slow.py first
# Or run directly:
curl -X POST "https://your-project.up.railway.app/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How to get a loan?",
    "user_name": "Test User"
  }'
```

**Expected**: JSON response with answer (takes 5-10 seconds)

#### Test Frontend:

1. Open your frontend URL (Netlify/GitHub Pages)
2. Enter your name
3. Enter question: "How to get a loan?"
4. Click "Get Answer"
5. **Should work!** Response in 5-10 seconds

---

## ✅ **Verification Checklist**

After deployment, verify everything works:

- [ ] Railway deployment shows "Active" (green)
- [ ] `/health` endpoint returns `{"status":"healthy"}`
- [ ] `/warmup` endpoint returns success message
- [ ] `/api/query` POST request returns answer
- [ ] Frontend loads and displays correctly
- [ ] Frontend can communicate with backend
- [ ] Queries return results in 5-10 seconds
- [ ] Confidence scores are reasonable (>70%)
- [ ] Source documents are displayed

---

## 🎯 **Expected Performance**

| Metric | Performance |
|--------|-------------|
| **First Request** | 30-60 seconds (cold start - one time) |
| **Subsequent Requests** | 5-10 seconds (fast!) |
| **Uptime** | 500 hours/month free |
| **Memory** | 8GB (plenty for this app) |
| **Cold Starts** | Minimal (Railway keeps services warmer) |

---

## 📊 **Monitoring Your Deployment**

### Railway Dashboard

1. Go to [railway.app](https://railway.app)
2. Click on your project
3. View:
   - **Deployments**: See deployment history
   - **Metrics**: CPU, memory, network usage
   - **Logs**: Real-time application logs
   - **Variables**: Manage environment variables

### Key Metrics to Watch

- **Memory Usage**: Should stay under 2GB
- **CPU Usage**: Spikes during queries (normal)
- **Response Time**: 5-10 seconds average
- **Deployment Status**: Should always be "Active"

### Viewing Logs

1. Click **"Deployments"** tab
2. Click on active deployment (green dot)
3. See logs in real-time
4. Look for:
   ```
   Customer Service Support System - STARTING
   Uvicorn running on http://0.0.0.0:8000
   === NEW QUERY ===
   === QUERY COMPLETE === Response time: 7500ms
   ```

---

## 🔧 **Troubleshooting**

### Issue 1: Deployment Failed

**Symptoms**: Red "Failed" status

**Solutions**:
1. Check **Build Logs** for errors
2. Verify `requirements.txt` is correct
3. Make sure `backend/` folder structure is correct
4. Check Python version is set to 3.11

### Issue 2: "Application Failed to Respond"

**Symptoms**: 502 Bad Gateway error

**Solutions**:
1. Check **Service Logs** for Python errors
2. Verify `ANTHROPIC_API_KEY` is set correctly
3. Make sure `chroma_db/` folder is committed to Git
4. Check that `PORT` environment variable is set

### Issue 3: "Vector Store Not Found"

**Symptoms**: Error in logs: `Vector store not found`

**Solutions**:
1. Verify `backend/chroma_db/` folder exists in your Git repo
2. Run locally first: `cd backend && python init_rag.py`
3. Commit the generated `chroma_db/` folder:
   ```bash
   git add backend/chroma_db/
   git commit -m "Add pre-built vector database"
   git push
   ```
4. Redeploy on Railway

### Issue 4: Slow First Request

**Symptoms**: First query takes 60+ seconds

**This is NORMAL!**
- First request downloads HuggingFace model
- Subsequent requests are fast (5-10s)
- This is expected behavior

**Optional Solution**: Set up UptimeRobot (see RENDER_SOLUTION.md) to keep it warm

### Issue 5: Frontend Can't Connect

**Symptoms**: "Unable to connect to server" error

**Solutions**:
1. Verify Railway backend URL in `frontend/app.js`
2. Check CORS is enabled (it is in our code)
3. Test backend URL directly in browser
4. Make sure Railway service is "Active" (not sleeping)

---

## 💰 **Cost Analysis**

### Free Tier Limits

| Resource | Limit | Sufficient? |
|----------|-------|-------------|
| **Execution Time** | 500 hours/month | ✅ Yes (~16 hours/day) |
| **Memory** | 8GB | ✅ Yes (app uses ~2GB) |
| **CPU** | Shared | ✅ Yes (light usage) |
| **Bandwidth** | 100GB | ✅ Yes (plenty) |

### When You'll Hit Limits

With **normal usage** (demo/portfolio):
- 500 hours = **~16 hours per day**
- If you need more, upgrade to Pro ($5/month)

### Upgrade Options

**Hobby Plan** ($5/month):
- Unlimited execution time
- Priority support
- More resources
- No limits

**Worth it if**:
- Running 24/7
- High traffic
- Production use

---

## 🔐 **Security Best Practices**

1. ✅ **Never commit `.env` files** - Already in `.gitignore`
2. ✅ **Use Railway environment variables** - We do this
3. ✅ **Keep API keys secret** - Only in Railway dashboard
4. ✅ **Use HTTPS** - Railway provides this automatically
5. ✅ **Enable Railway's security features** - Automatic

---

## 📱 **Next Steps After Deployment**

### 1. Test Thoroughly
- Try multiple different questions
- Test edge cases
- Verify confidence scores
- Check source attribution

### 2. Monitor Performance
- Watch Railway metrics
- Check response times
- Monitor error rates
- Review logs regularly

### 3. Optimize (Optional)
- Add caching layer
- Implement request queuing
- Add rate limiting
- Set up monitoring alerts

### 4. Share Your Project
- Add Railway URL to README
- Create demo video
- Share on LinkedIn/Twitter
- Add to portfolio

---

## 🆘 **Getting Help**

### Railway Support
- [Railway Docs](https://docs.railway.app/)
- [Railway Discord](https://discord.gg/railway)
- Help button in Railway dashboard

### Common Resources
- [Python Deployment Guide](https://docs.railway.app/guides/python)
- [Environment Variables](https://docs.railway.app/develop/variables)
- [Troubleshooting](https://docs.railway.app/troubleshoot/fixing-common-errors)

---

## ✅ **Success Checklist**

You're done when:

- [ ] Railway service is "Active" and green
- [ ] Backend responds to `/health` with success
- [ ] Backend responds to `/warmup` successfully
- [ ] Test query returns valid answer (5-10s)
- [ ] Frontend is deployed and accessible
- [ ] Frontend can query backend successfully
- [ ] End-to-end flow works (question → answer)
- [ ] Logs show no errors
- [ ] Response times are acceptable (<10s)

---

## 🎉 **Congratulations!**

Your Customer Service Support System is now:
- ✅ **Deployed** on Railway
- ✅ **Fast** (5-10 second responses)
- ✅ **Reliable** (no sleep issues)
- ✅ **Secure** (proper environment variables)
- ✅ **Production-ready**

**Total Cost**: $0/month with free tier!

**Your URLs**:
- Backend: `https://your-project.up.railway.app`
- Frontend: `https://your-site.netlify.app` (or GitHub Pages)

Share these URLs in your portfolio! 🚀
