# Netlify Deployment Guide

## ⚠️ Important Notice

**Your Flask application with full OpenCV/NumPy/Matplotlib functionality CANNOT run on Netlify.**

This deployment creates a **static demo version** with:
- ✅ Static HTML pages
- ✅ Image gallery
- ✅ Basic serverless functions
- ❌ No complex image processing
- ❌ No thermal analysis
- ❌ No OpenCV functionality

## Files Created for Netlify:

1. **netlify.toml** - Netlify configuration
2. **build_static.py** - Converts Flask app to static HTML  
3. **netlify/functions/analyze.py** - Basic serverless function
4. **package.json** - Build configuration

## Deployment Steps:

### Option 1: Netlify Web Interface
1. Go to [netlify.com](https://netlify.com)
2. Connect your GitHub repository
3. Build settings:
   - Build command: `python build_static.py`
   - Publish directory: `static_build`
4. Deploy

### Option 2: Netlify CLI
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Build static version
python build_static.py

# Deploy
netlify deploy --prod --dir=static_build
```

## What You Get:

### ✅ Working Features:
- Static image gallery
- Basic UI/UX
- Sample coal images display
- Basic serverless API endpoints

### ❌ Missing Features:
- Real image processing
- Thermal analysis
- OpenCV functionality
- Complex calculations
- File uploads

## Recommended Alternatives:

For full functionality, deploy your Flask app to:

1. **Heroku** (Best choice)
   ```bash
   git push heroku main
   ```

2. **Railway** 
   - Supports Python/Flask natively
   - Good for image processing

3. **Render**
   - Free tier available
   - Python support

4. **DigitalOcean App Platform**
   - Reliable Python hosting

## Current Status:
- 🔧 Railway config removed
- 📦 Netlify config added
- 🎨 Static build ready
- ⚡ Basic serverless functions included

Your full-featured Flask app will work much better on Railway, Heroku, or Render!