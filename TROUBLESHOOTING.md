# Troubleshooting Guide - Production Deployment

## Error: "Unable to connect to the server"

This means the frontend cannot reach the backend. Follow these steps:

### Step 1: Verify Backend URL

Your frontend is configured to use: `https://customer-service-ai-system.onrender.com`

**Test it**: Open these URLs in your browser:

1. **Health Check**: https://customer-service-ai-system.onrender.com/health
   - Expected: `{"status":"healthy"}`

2. **Root**: https://customer-service-ai-system.onrender.com/
   - Expected: `{"message":"Customer Service Support System API","status":"running"}`

3. **API Docs**: https://customer-service-ai-system.onrender.com/docs
   - Expected: Interactive Swagger UI

**If you get an error on ANY of these**, your backend isn't running. Proceed to Step 2.

**If all URLs work**, skip to Step 4 (CORS issue).

---

### Step 2: Check Render Service Status

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click on your backend service (`customer-service-backend`)
3. Check the status:
   - ✅ **Live (green)** → Backend is running, proceed to Step 4
   - ⏸️ **Suspended** → Click "Resume" to start it
   - ❌ **Deploy failed (red)** → Proceed to Step 3

---

### Step 3: Fix Build Failures

#### Common Build Error 1: Missing Dependencies

**Symptom**: Logs show `ModuleNotFoundError: No module named 'dotenv'`

**Fix**: Verify `backend/requirements.txt` includes all dependencies:
```bash
# Check your requirements.txt
cat backend/requirements.txt | grep dotenv
```

Should show: `python-dotenv==1.0.0`

#### Common Build Error 2: Init Script Failed

**Symptom**: Logs show `No such file or directory: knowledge_base/`

**Fix**: Update your Render build command to handle missing PDFs:

**Go to Render Dashboard** → Your Service → Settings → Build Command:

**Change from:**
```bash
pip install -r backend/requirements.txt && cd backend && python init_rag.py
```

**Change to:**
```bash
pip install -r backend/requirements.txt && cd backend && mkdir -p ../knowledge_base && python init_rag.py
```

Or if you have PDFs committed, ensure they're in the repo.

#### Common Build Error 3: Python Version

**Symptom**: Logs show Python version incompatibility

**Fix**: Add to Render environment variables:
- Key: `PYTHON_VERSION`
- Value: `3.11.0`

#### Common Build Error 4: Missing API Key

**Symptom**: Backend starts but crashes on first request

**Fix**: Verify environment variable in Render:
1. Go to Service → Environment
2. Check `ANTHROPIC_API_KEY` is set
3. Value should start with `sk-ant-`
4. Click "Save Changes"

---

### Step 4: Fix CORS Issues

**Symptom**:
- Backend URLs work in browser
- Frontend still shows connection error
- Browser console shows CORS error

**Fix**: The backend already has CORS enabled (`allow_origins=["*"]`), but check:

1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for red CORS errors
4. Check Network tab for failed requests

**If you see CORS errors**, update `backend/api/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Already set
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then redeploy.

---

### Step 5: Test Backend Directly

Use this curl command to test the backend:

```bash
curl -X POST "https://customer-service-ai-system.onrender.com/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How to get a loan?",
    "user_name": "Test User"
  }'
```

**Expected**: JSON response with answer

**If you get an error**: Check Render logs for details.

---

### Step 6: Check Frontend URL Configuration

Verify your frontend is using the correct URL:

1. Open browser DevTools (F12) on your frontend page
2. Check Console tab
3. Look for: `Using API URL: https://customer-service-ai-system.onrender.com`

**If URL is wrong**, update `frontend/app.js` line 5:
```javascript
: 'https://YOUR-ACTUAL-BACKEND-URL.onrender.com';
```

Commit and push to redeploy frontend.

---

## Quick Diagnostic Checklist

Run through this checklist:

- [ ] Backend service shows "Live" in Render dashboard
- [ ] `https://customer-service-ai-system.onrender.com/health` returns `{"status":"healthy"}`
- [ ] `ANTHROPIC_API_KEY` is set in Render environment variables
- [ ] Frontend console shows correct API URL
- [ ] No CORS errors in browser console
- [ ] Backend logs show no errors (check Render → Logs tab)

---

## Still Not Working?

### Get Detailed Error Information

1. **Check browser console**:
   - Open DevTools (F12)
   - Go to Console tab
   - Look for error messages
   - Go to Network tab
   - Try submitting again
   - Click on the failed request
   - Check the error response

2. **Check Render logs**:
   - Go to Render dashboard
   - Click your backend service
   - Click "Logs" tab
   - Look for errors around the time you submitted the query

3. **Test with local backend**:
   ```bash
   cd backend
   uvicorn api.main:app --reload --port 8000
   ```

   Then temporarily change frontend to use local:
   ```javascript
   const API_URL = 'http://localhost:8000';
   ```

   If this works, the issue is with Render deployment.

---

## Most Common Solutions

### Solution 1: Cold Start (Render Free Tier)

**Issue**: First request after 15 minutes of inactivity takes 30-60 seconds

**Symptom**:
- Health check works
- First query times out
- Second query works

**Solution**:
- Wait 60 seconds for the first request
- Or upgrade to paid plan to avoid cold starts

### Solution 2: Missing Environment Variable

**Issue**: Backend crashes on API call

**Fix**:
1. Go to Render → Your Service → Environment
2. Add: `ANTHROPIC_API_KEY` = `your-key-here`
3. Click "Save Changes" (this triggers redeploy)
4. Wait for deployment to complete (5-10 minutes)

### Solution 3: Build Command Error

**Issue**: Deployment fails during build

**Fix**: Simplify build command:
```bash
pip install -r backend/requirements.txt
```

Then manually run init later or skip it if you have persistent disk.

---

## Contact for Help

If you're still stuck, provide:

1. **Render deployment logs** (last 50 lines)
2. **Browser console errors** (screenshot)
3. **Response from health check URL**
4. **Service status** (Live, Failed, Suspended)

This will help diagnose the specific issue.
