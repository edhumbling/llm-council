# Netlify Deployment Guide

## Quick Deploy

1. **Connect your repository to Netlify**
   - Go to [Netlify Dashboard](https://app.netlify.com)
   - Click "Add new site" → "Import an existing project"
   - Connect your Git repository

2. **Configure Build Settings**
   - **Base directory**: `frontend`
   - **Build command**: `npm install && npm run build`
   - **Publish directory**: `frontend/dist`

3. **Set Environment Variables**
   - Go to Site settings → Environment variables
   - Add: `VITE_API_BASE_URL` = your backend URL (e.g., `https://your-backend.onrender.com`)

4. **Deploy**
   - Netlify will automatically deploy on every push to your main branch
   - Or click "Deploy site" to deploy immediately

## Manual Deploy

If you want to deploy manually:

```bash
cd frontend
npm install
npm run build
# Then drag and drop the 'dist' folder to Netlify
```

## Important Notes

- The `_redirects` file in `frontend/public/` ensures all routes redirect to `index.html` (required for SPAs)
- The `netlify.toml` file in the root configures the build settings
- Make sure your backend is deployed and accessible (e.g., on Render, Railway, or Fly.io)
- Set the `VITE_API_BASE_URL` environment variable to point to your backend
