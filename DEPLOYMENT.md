# Deployment Guide - DynamicRAGSystem

This guide covers deploying the DynamicRAGSystem application to various platforms.

## 🚀 Quick Deployment Overview

- **Frontend**: Deploy to Vercel (recommended) or Netlify
- **Backend**: Deploy to Railway, Heroku, or cloud providers
- **Database**: ChromaDB runs locally or use cloud vector databases

## 📋 Prerequisites

- GitHub repository with the code
- OpenAI API key
- Vercel account (for frontend)
- Railway/Heroku account (for backend)

## 🎨 Frontend Deployment (Vercel)

### Step 1: Prepare Frontend

1. **Ensure frontend is ready:**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Create production environment file:**
   ```bash
   echo "REACT_APP_API_URL=https://your-backend-url.railway.app" > .env.production
   ```

### Step 2: Deploy to Vercel

1. **Connect GitHub to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Sign in with GitHub
   - Click "New Project"
   - Import your repository

2. **Configure build settings:**
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
   - **Install Command**: `npm install`

3. **Set environment variables:**
   - `REACT_APP_API_URL`: Your backend URL
   - `GENERATE_SOURCEMAP`: `false`

4. **Deploy:**
   - Click "Deploy"
   - Wait for deployment to complete
   - Your frontend will be available at `https://your-app.vercel.app`

### Alternative: Netlify Deployment

1. **Build the project:**
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy to Netlify:**
   - Go to [netlify.com](https://netlify.com)
   - Drag and drop the `build` folder
   - Or connect your GitHub repository

3. **Set environment variables:**
   - Go to Site Settings > Environment Variables
   - Add `REACT_APP_API_URL`

## 🔧 Backend Deployment (Railway)

### Step 1: Prepare Backend

1. **Create Railway configuration:**
   ```bash
   # In backend directory
   echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile
   ```

2. **Create railway.json:**
   ```json
   {
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
       "healthcheckPath": "/health"
     }
   }
   ```

### Step 2: Deploy to Railway

1. **Connect GitHub to Railway:**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

2. **Configure deployment:**
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Set environment variables:**
   - Go to Variables tab
   - Add `OPENAI_API_KEY`: Your OpenAI API key

4. **Deploy:**
   - Railway will automatically build and deploy
   - Your backend will be available at `https://your-app.railway.app`

### Alternative: Heroku Deployment

1. **Create Heroku app:**
   ```bash
   heroku create your-app-name
   ```

2. **Set environment variables:**
   ```bash
   heroku config:set OPENAI_API_KEY=your-openai-api-key
   ```

3. **Deploy:**
   ```bash
   git subtree push --prefix backend heroku main
   ```

## 🐳 Docker Deployment

### Step 1: Create Dockerfiles

**Backend Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile:**
```dockerfile
FROM node:16-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Step 2: Create Docker Compose

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./backend/chroma_db:/app/chroma_db

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    depends_on:
      - backend
```

### Step 3: Deploy with Docker

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d
```

## ☁️ Cloud Provider Deployment

### AWS Deployment

1. **EC2 Instance:**
   - Launch Ubuntu EC2 instance
   - Install Docker and Docker Compose
   - Clone repository and run `docker-compose up -d`

2. **Elastic Beanstalk:**
   - Create Python platform
   - Deploy backend with `eb deploy`
   - Deploy frontend to S3 + CloudFront

3. **ECS/Fargate:**
   - Create ECS cluster
   - Define task definitions
   - Deploy with ECS service

### Google Cloud Platform

1. **Cloud Run:**
   - Build container images
   - Deploy to Cloud Run
   - Set environment variables

2. **App Engine:**
   - Create `app.yaml` for backend
   - Deploy with `gcloud app deploy`

### Azure

1. **Container Instances:**
   - Build and push to Azure Container Registry
   - Deploy with Azure Container Instances

2. **App Service:**
   - Create Python web app
   - Deploy backend code
   - Deploy frontend as static site

## 🔧 Environment Configuration

### Production Environment Variables

**Backend:**
```bash
OPENAI_API_KEY=your-openai-api-key
LOG_LEVEL=INFO
CHROMA_DB_PATH=/app/chroma_db
```

**Frontend:**
```bash
REACT_APP_API_URL=https://your-backend-url.com
GENERATE_SOURCEMAP=false
```

### Security Considerations

1. **API Keys**: Store securely in environment variables
2. **CORS**: Configure for production domains only
3. **HTTPS**: Use SSL certificates for all endpoints
4. **Rate Limiting**: Implement rate limiting for production
5. **File Upload Limits**: Set appropriate file size limits

## 📊 Monitoring and Logging

### Health Checks

- **Backend**: `GET /health` endpoint
- **Frontend**: Basic connectivity checks

### Logging

1. **Backend Logging:**
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   ```

2. **Frontend Logging:**
   ```javascript
   console.log('Frontend started');
   ```

### Monitoring Tools

- **Vercel Analytics**: Built-in for frontend
- **Railway Metrics**: Built-in for backend
- **Uptime Monitoring**: UptimeRobot, Pingdom
- **Error Tracking**: Sentry, LogRocket

## 🔄 CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Railway
        run: |
          # Deploy backend to Railway
          
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        run: |
          # Deploy frontend to Vercel
```

## 🚨 Troubleshooting

### Common Deployment Issues

1. **Build Failures:**
   - Check dependencies in requirements.txt/package.json
   - Verify Node.js/Python versions
   - Check for missing environment variables

2. **Runtime Errors:**
   - Check logs in deployment platform
   - Verify environment variables are set
   - Check API connectivity

3. **CORS Issues:**
   - Update CORS origins in backend
   - Check frontend API URL configuration

4. **File Upload Issues:**
   - Check file size limits
   - Verify file type restrictions
   - Check storage permissions

### Debug Commands

```bash
# Check backend health
curl https://your-backend-url.com/health

# Check frontend build
cd frontend && npm run build

# Check Docker containers
docker ps
docker logs container-name
```

## 📈 Performance Optimization

### Backend Optimization

1. **Caching**: Implement Redis caching
2. **Database**: Use managed ChromaDB service
3. **CDN**: Use CDN for static files
4. **Load Balancing**: Multiple backend instances

### Frontend Optimization

1. **Code Splitting**: Lazy load components
2. **Image Optimization**: Compress images
3. **Caching**: Browser caching strategies
4. **CDN**: Use Vercel's global CDN

## 🔒 Security Checklist

- [ ] Environment variables secured
- [ ] HTTPS enabled
- [ ] CORS properly configured
- [ ] File upload validation
- [ ] Rate limiting implemented
- [ ] Error messages sanitized
- [ ] Dependencies updated
- [ ] Security headers set

## 📞 Support

For deployment issues:
1. Check platform-specific documentation
2. Review error logs
3. Test locally first
4. Contact platform support if needed
