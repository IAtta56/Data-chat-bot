# Hugging Face Spaces Deployment Guide

## 🚀 Quick Deploy

1. **Create Hugging Face Account**
   - Go to [huggingface.co](https://huggingface.co)
   - Sign up for free

2. **Create New Space**
   - Go to [Spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Name: `datachat-ai`
   - License: MIT
   - SDK: Docker
   - Hardware: CPU Basic (Free)

3. **Upload Code**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/datachat-ai
   git push hf main
   ```

4. **Add Secret (Optional - for higher rate limits)**
   - Go to Space Settings > Repository secrets
   - Add `HF_TOKEN` with your Hugging Face token
   - Get token from [Settings > Access Tokens](https://huggingface.co/settings/tokens)

5. **Wait for Build**
   - Space will build automatically (5-10 minutes)
   - Check logs for any errors

## 🎯 Features

- ✅ **100% Free** - No API keys needed
- ✅ **Auto-scaling** - Handles traffic automatically
- ✅ **Persistent Storage** - User data saved
- ✅ **HTTPS** - Secure by default
- ✅ **Custom Domain** - Available on paid plans

## 📊 Rate Limits

**Without HF_TOKEN:**
- 1,000 requests/day
- Good for personal use

**With HF_TOKEN (Free):**
- 30,000 requests/month
- Perfect for small teams

**Pro Tier ($9/month):**
- Higher limits
- GPU acceleration
- Custom domains

## 🔧 Environment Variables

Add in Space Settings if needed:

```
HF_TOKEN=your_huggingface_token_here
```

## 📝 Post-Deployment

1. Test the app at: `https://huggingface.co/spaces/YOUR_USERNAME/datachat-ai`
2. Share with users
3. Monitor usage in Space analytics

## 🐛 Troubleshooting

**Build fails?**
- Check Dockerfile syntax
- Ensure all dependencies in requirements.txt
- Check build logs in Space

**App crashes?**
- Check logs: Space > Logs
- Verify port 7860 is exposed
- Test locally first with Docker

**Slow performance?**
- Upgrade to GPU space ($0.60/hour)
- Optimize model loading
- Use caching

## 💡 Tips

- Keep database.db in .dockerignore
- Use environment variables for secrets
- Test locally with: `docker build -t datachat . && docker run -p 7860:7860 datachat`
- Enable Space sleeping to save resources
