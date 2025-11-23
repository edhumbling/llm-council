# Deployment Guide

## Quick Deploy to Render

### Prerequisites
1. Create a Render account at https://render.com
2. Get your OpenRouter API key from https://openrouter.ai
3. Push your code to a Git repository (GitHub, GitLab, or Bitbucket)

### Deploy Backend

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your repository
4. Configure:
   - **Name**: `llm-council-backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**:
     - `OPENROUTER_API_KEY`: Your OpenRouter API key
     - `CORS_ORIGINS`: Your frontend URL (e.g., `https://llm-council-frontend.onrender.com`)

### Deploy Frontend

1. Go to https://dashboard.render.com
2. Click "New +" → "Static Site"
3. Connect your repository
4. Configure:
   - **Name**: `llm-council-frontend`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/dist`
   - **Environment Variables**:
     - `VITE_API_BASE_URL`: Your backend URL (e.g., `https://llm-council-backend.onrender.com`)

### Alternative: Deploy with render.yaml

If you have the Render CLI or use the dashboard, you can deploy using the `render.yaml` file:

1. Install Render CLI: `npm install -g render-cli`
2. Run: `render deploy`

## Other Deployment Options

### Vercel (Frontend) + Railway (Backend)

**Frontend on Vercel:**
1. Import your repo to Vercel
2. Set root directory to `frontend`
3. Build command: `npm run build`
4. Output directory: `dist`
5. Environment variable: `VITE_API_BASE_URL` = your backend URL

**Backend on Railway:**
1. Create new project on Railway
2. Connect your repo
3. Add environment variable: `OPENROUTER_API_KEY`
4. Railway will auto-detect Python and install dependencies

### Fly.io (Full Stack)

1. Install Fly CLI: `flyctl auth login`
2. Run: `flyctl launch`
3. Configure environment variables in Fly dashboard

## Important Notes

- The current storage uses local JSON files, which are ephemeral in most cloud deployments
- For production, consider using a database (PostgreSQL, MongoDB, etc.)
- Make sure to set CORS_ORIGINS to your frontend URL
- The backend needs persistent storage for conversations if you want them to survive restarts
