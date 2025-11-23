# 🚀 LLM Council - Live Deployment Guide

## Current Status
✅ Frontend built successfully
✅ Backend code ready
⚠️ Need to configure environment variables on Render

## 🔧 Step 1: Configure Backend on Render

### Go to Render Dashboard
1. Navigate to https://dashboard.render.com
2. Find your `llm-council-backend` service
3. Click on it

### Add Environment Variables
Click **Environment** tab and add these variables:

```
GROQ_API_KEY=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
DATABASE_URL=postgresql://neondb_owner:npg_iUGqF31QdZfo@ep-empty-art-a96hqpju-pooler.gwc.azure.neon.tech/neondb?sslmode=require&channel_binding=require
CORS_ORIGINS=*
```

### Save & Deploy
- Click **Save Changes**
- Render will automatically redeploy your backend

---

## 📦 Step 2: Deploy Frontend to Netlify

### Option A: Automatic (Git Push)
If your site is connected to GitHub:
```bash
git add .
git commit -m "Fix: Update to Groq API and Humbl AI design"
git push origin main
```
Netlify will auto-deploy!

### Option B: Manual Deploy
1. Go to https://app.netlify.com
2. Find your site
3. Drag the `frontend/dist` folder to the deploy area

---

## 🔍 Step 3: Verify Deployment

### Check Backend
Visit: `https://llm-council-backend.onrender.com/`

You should see:
```json
{"status": "ok", "service": "LLM Council API"}
```

### Check Frontend
Visit your Netlify URL (e.g., `https://your-site.netlify.app`)

### Test the Council
1. Type a question or click an example prompt
2. Click Send or press Enter
3. You should see:
   - ⏳ Loading indicator
   - 📊 Stage 1: Individual responses from 5 models
   - 🏆 Stage 2: Rankings
   - ✨ Stage 3: Final synthesis

---

## ❌ Troubleshooting

### If Council Doesn't Respond:

#### Check Browser Console
1. Press F12 (DevTools)
2. Go to **Console** tab
3. Look for errors like:
   - `Failed to fetch` → Backend is down
   - `CORS error` → CORS not configured
   - `401/403` → API key issue

#### Check Network Tab
1. Press F12
2. Go to **Network** tab
3. Try sending a message
4. Look for the `/api/conversations/{id}/messages/stream` request
5. Check if it's:
   - ✅ **200 OK** → Working!
   - ❌ **500 Error** → Backend error (check Render logs)
   - ❌ **Failed** → Can't connect to backend

#### Check Render Logs
1. Go to Render Dashboard
2. Click your backend service
3. Click **Logs** tab
4. Look for errors when you try to send a message

### Common Issues:

**Issue**: "Cannot connect to backend"
**Fix**: Check that `VITE_API_BASE_URL` in `netlify.toml` matches your Render URL

**Issue**: "All models failed to respond"
**Fix**: 
- Check `GROQ_API_KEY` is set on Render
- Verify the key is correct (starts with `gsk_`)

**Issue**: "CORS error"
**Fix**: Make sure `CORS_ORIGINS=*` is set on Render

---

## 📋 Quick Checklist

Before asking for help, verify:
- [ ] Backend is deployed and showing "ok" status
- [ ] `GROQ_API_KEY` is set on Render
- [ ] `DATABASE_URL` is set on Render
- [ ] Frontend is deployed (can see the UI)
- [ ] Browser console shows no CORS errors
- [ ] Network tab shows requests to correct backend URL

---

## 🎯 Expected Behavior

When working correctly:
1. You type/click a question
2. A new conversation appears in sidebar (on mobile, open menu to see)
3. Loading indicator shows "Consulting the council..."
4. Stage 1 completes (5 model responses)
5. Stage 2 completes (rankings)
6. Stage 3 completes (final answer)
7. Conversation title updates automatically

---

## 📞 Need Help?

If still not working:
1. Check Render logs for backend errors
2. Check browser console for frontend errors
3. Verify all environment variables are set
4. Try creating a conversation manually via API:
   ```bash
   curl https://llm-council-backend.onrender.com/api/conversations
   ```
