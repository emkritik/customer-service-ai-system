# Render Free Tier Solution

## The Problem

Render's free tier has two limitations that affect this app:
1. **512MB RAM** - Tight for loading HuggingFace embeddings
2. **15-minute sleep** - Service shuts down after inactivity

## The Solution: Keep-Alive Monitoring

Use a free monitoring service to ping your backend every 10 minutes, keeping it warm.

---

## Step 1: Set Up UptimeRobot (Free Forever)

### 1. Create Account
Go to [uptimerobot.com](https://uptimerobot.com) and sign up (free)

### 2. Add Monitor
1. Click **"+ Add New Monitor"**
2. Configure:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: Customer Service Backend Warmup
   - **URL**: `https://customer-service-ai-system.onrender.com/warmup`
   - **Monitoring Interval**: 10 minutes (maximum for free)
   - **Alert Contacts**: (optional - your email)

3. Click **"Create Monitor"**

### 3. How It Works
- UptimeRobot pings `/warmup` every 10 minutes
- This keeps Render from sleeping (15 min threshold)
- Also preloads the vector store
- Result: Service stays warm and responsive!

---

## Step 2: Update Frontend Message

The first request after deployment will still be slow. Let's add a better user message.

### Update Loading Text

Edit `frontend/index.html`, find the loading section and update it:

```html
<div id="loading" style="display: none;" class="loading">
    <div class="spinner"></div>
    <p>Processing your question...</p>
    <p style="font-size: 0.9em; color: #666;">
        ⚠️ First request may take 30-60 seconds (system warming up)
    </p>
</div>
```

---

## Step 3: Test It

### Wait 2-3 Minutes
After setting up UptimeRobot, wait a few minutes for it to ping the service.

### Then Test:
```bash
# This should work now!
python test_backend_slow.py
```

**Expected Result**:
```
✓ Response received in 8.5 seconds
✓ Success!
Answer: To get a loan, you need to...
Confidence: 85%
```

---

## Alternative: Cron-Job.org (Another Free Option)

If you prefer, use [cron-job.org](https://cron-job.org) instead:

1. Sign up (free)
2. Create cronjob:
   - **URL**: `https://customer-service-ai-system.onrender.com/warmup`
   - **Schedule**: Every 10 minutes
   - **Method**: GET
3. Enable the job

---

## How This Solves the Issues

### Before:
- ❌ Service sleeps after 15 min
- ❌ Cold start takes 60-90 seconds
- ❌ First request times out

### After:
- ✅ Service stays warm (pinged every 10 min)
- ✅ Vector store pre-loaded by `/warmup`
- ✅ Requests respond in 5-10 seconds
- ✅ No timeouts!

---

## Cost Analysis

| Service | Cost | Purpose |
|---------|------|---------|
| Render | FREE | Backend hosting |
| UptimeRobot | FREE | Keep-alive pings |
| Render Static | FREE | Frontend hosting |
| **Total** | **$0/month** | **Fully free!** |

---

## Monitoring Your Service

### UptimeRobot Dashboard
- See uptime percentage
- Response time graphs
- Get alerts if service goes down

### Render Logs
- Watch `/warmup` requests every 10 min
- See "Warmup complete - vectorstore ready"
- Monitor actual query performance

---

## Expected Performance

| Scenario | Response Time | Notes |
|----------|---------------|-------|
| **With UptimeRobot** | 5-10 seconds | Service stays warm |
| **Without UptimeRobot** | 60-120 seconds | Cold start every time |
| **After 15+ min idle** | 30-60 seconds | One slow request, then fast |

---

## Troubleshooting

### If It's Still Slow

1. **Check UptimeRobot is running**:
   - Go to UptimeRobot dashboard
   - Verify monitor is "Up" and green
   - Check last ping time (should be <10 min ago)

2. **Check Render logs**:
   - Go to Render → Your Service → Logs
   - Look for: `Warmup request received` every 10 min
   - Look for: `Warmup complete - vectorstore ready`

3. **Verify the URL**:
   - Make sure UptimeRobot is pinging the correct URL
   - URL should end in `/warmup` not `/health`

### If Vector Store Fails to Load

Check Render logs for errors. Most common issues:
- Out of memory (upgrade to paid plan)
- Missing chroma_db folder (check git commit)
- ANTHROPIC_API_KEY not set

---

## Upgrade Options (Optional)

If you need better performance:

### Render Starter ($7/month)
- 2GB RAM (no memory issues)
- No sleep (always on)
- Faster cold starts
- Worth it for production use

### Benefits:
- ✅ No UptimeRobot needed
- ✅ Always fast (5-10s every request)
- ✅ More reliable
- ✅ Better for real users

But **free tier works fine** with the keep-alive solution!

---

## Summary

1. ✅ Set up UptimeRobot (5 minutes)
2. ✅ Point it to `/warmup` endpoint
3. ✅ Wait 10 minutes for first ping
4. ✅ Test - should work perfectly!

**Your system is now production-ready on Render's free tier!** 🎉
