# Railway Deployment Guide

## Files Created for Railway Deployment:

1. **Procfile** - Defines how Railway should start your app
2. **railway.json** - Railway-specific configuration
3. **nixpacks.toml** - Build configuration for Python environment
4. **.railwayignore** - Files to ignore during deployment

## Deployment Steps:

### 1. Push to GitHub
```bash
git add .
git commit -m "Add Railway deployment files"
git push origin main
```

### 2. Deploy on Railway
1. Go to [railway.app](https://railway.app)
2. Sign up/Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `CoalSampleAnalyzer` repository
6. Railway will automatically detect Python and deploy

### 3. Environment Variables (if needed)
- Railway will automatically set `PORT` environment variable
- No additional environment variables needed for this app

### 4. Domain
- Railway provides a free domain: `yourapp.railway.app`
- You can also add custom domains in the Railway dashboard

## Important Changes Made:

1. **opencv-python → opencv-python-headless**: Headless version works better in server environments
2. **numpy<2.0.0**: Ensures compatibility with OpenCV
3. **debug=False**: Production mode for deployment
4. **PORT environment variable**: App now uses Railway's assigned port

## Expected Deployment Time:
- Build time: 2-5 minutes
- Your app will be available at: `https://[random-name].railway.app`

## Troubleshooting:
- Check Railway logs if deployment fails
- Ensure all files are committed to GitHub
- Railway automatically installs requirements.txt dependencies