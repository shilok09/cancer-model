# Render Deployment Guide

## Prerequisites

- GitHub account (to host your repository)
- Render account (free at https://render.com)
- CatBoost model file: `catboost_cancer_progression_model.cbm`

---

## Step 1: Prepare Your Repository

### 1.1 Create GitHub Repository

```bash
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Cancer progression prediction API"

# Add remote (replace with your GitHub repo URL)
git remote add origin https://github.com/yourusername/cancer-progression-api.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 1.2 Required Files Structure

```
cancer-progression-api/
├── main.py                                    # FastAPI application
├── requirements.txt                           # Python dependencies
├── render.yaml                                # Render configuration (optional)
├── catboost_cancer_progression_model.cbm      # Trained model (IMPORTANT!)
├── .gitignore                                 # Git ignore file
├── README.md                                  # Documentation
└── TEST_API.md                               # Testing guide
```

### 1.3 Create .gitignore

Create `.gitignore` file:

```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.DS_Store
.env
.env.local
*.log
```

### 1.4 Important: Add Model to Git LFS (Large File Storage)

Since the CatBoost model is large (40-50MB), use Git LFS:

```bash
# Install Git LFS (if not already installed)
git lfs install

# Track the model file with LFS
git lfs track "*.cbm"

# Add and commit
git add .gitattributes
git commit -m "Add Git LFS tracking for model files"

# Now add and push the model
git add catboost_cancer_progression_model.cbm
git commit -m "Add trained CatBoost model"
git push origin main
```

Alternatively, if your model is small enough (<100MB), you can add it directly to Git.

---

## Step 2: Configure Render Deployment

### 2.1 Create render.yaml

Create a `render.yaml` file in your project root:

```yaml
services:
  - type: web
    name: cancer-progression-api
    runtime: python310
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: "3.10.12"
      - key: MODEL_PATH
        value: "./catboost_cancer_progression_model.cbm"
```

### 2.2 Update requirements.txt

Ensure your `requirements.txt` includes all dependencies (already provided).

---

## Step 3: Deploy to Render

### 3.1 Via Render Dashboard (Easiest)

1. **Sign in to Render**: https://dashboard.render.com

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Select "Build and deploy from a Git repository"
   - Connect your GitHub account
   - Select your repository

3. **Configure**:
   - **Name**: `cancer-progression-api`
   - **Runtime**: `Python 3.10`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free tier (sufficient for testing)

4. **Environment Variables** (optional):
   - `MODEL_PATH`: `./catboost_cancer_progression_model.cbm`
   - `LOG_LEVEL`: `info`

5. **Click Deploy**

### 3.2 Via render.yaml (Automatic)

Render will automatically detect and use `render.yaml` if present in repo.

---

## Step 4: Verify Deployment

### 4.1 Check Deployment Status

1. Go to your service dashboard on Render
2. Look for "Deploy log" - should show:
   ```
   ✓ Build succeeded
   ✓ Service deployed
   ```

### 4.2 Get Your API URL

Your API will be available at:
```
https://cancer-progression-api.onrender.com
```

(The exact URL depends on your chosen name)

### 4.3 Test the API

```bash
# Health check
curl https://cancer-progression-api.onrender.com/health

# Make a prediction
curl -X POST https://cancer-progression-api.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "demographic_gender": "male",
    "diagnoses_tumor_grade": "2",
    "diagnoses_age_at_diagnosis": 65,
    ...
  }'
```

### 4.4 Interactive Documentation

Access Swagger UI:
```
https://cancer-progression-api.onrender.com/docs
```

---

## Step 5: Production Considerations

### 5.1 Set Environment Variables

In Render Dashboard → Your Service → Environment:

```
MODEL_PATH = ./catboost_cancer_progression_model.cbm
PYTHON_VERSION = 3.10.12
```

### 5.2 Enable Auto-Deploy

- Go to Settings → Auto-Deploy
- Select "Yes" to deploy on every git push

### 5.3 Monitor Logs

- Dashboard → Logs tab
- Check for errors or warnings

### 5.4 Scale Configuration

For production:
- Upgrade from Free to Pro tier
- Increase memory if needed
- Enable region selection

---

## Step 6: CI/CD Integration (Optional)

### GitHub Actions for Testing

Create `.github/workflows/test.yml`:

```yaml
name: Test API

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Test API startup
        run: python -c "from main import app; print('✓ API imports successfully')"
      
      - name: Lint with flake8
        run: |
          pip install flake8
          flake8 main.py --count --select=E9,F63,F7,F82 --show-source --statistics
```

---

## Troubleshooting

### Issue: Model file not found

**Solution:**
1. Verify model file is committed to Git
2. Check model path in Render environment: `./catboost_cancer_progression_model.cbm`
3. In Render logs, look for: `✓ Model loaded successfully`

### Issue: Build fails

**Solution:**
1. Check build log for specific error
2. Verify all packages in `requirements.txt` are compatible
3. Try building locally first: `pip install -r requirements.txt`

### Issue: Slow cold starts

**Cause:** Free tier has cold starts (service sleeps after 15 min of inactivity)

**Solution:**
1. Upgrade to Pro tier for always-on service
2. Or implement warm-up requests

### Issue: Out of memory

**Cause:** Free tier has limited RAM (512MB)

**Solution:**
1. Monitor model size
2. Upgrade to Pro tier
3. Reduce batch size for batch predictions

---

## Monitoring

### 5.1 Logs

Access via Render Dashboard:
```
Service → Logs
```

Look for:
- Model loading: `✓ Model loaded successfully`
- Predictions: `✓ Prediction generated`
- Errors: `✗ Error loading model`

### 5.2 Performance

Monitor in Render Dashboard:
- Request rate
- Response times
- CPU/Memory usage
- Error rate

---

## Security Best Practices

1. **API Keys** (if needed):
   ```python
   from fastapi.security import HTTPBearer, HTTPAuthenticationCredentials
   security = HTTPBearer()
   
   @app.post("/predict")
   async def predict(request: PredictionRequest, 
                     credentials: HTTPAuthenticationCredentials = Depends(security)):
       # Verify API key
       ...
   ```

2. **CORS Configuration**:
   - Edit in `main.py` to restrict origins
   - Currently allows all (`allow_origins=["*"]`)

3. **HTTPS**: Automatic on Render

4. **Rate Limiting**:
   ```bash
   pip install slowapi
   ```

---

## Updating Your API

### 1. Make local changes
```bash
git add .
git commit -m "Update prediction logic"
```

### 2. Push to GitHub
```bash
git push origin main
```

### 3. Render auto-deploys
- If auto-deploy enabled, service updates automatically
- Or manually click "Deploy" in Render dashboard

---

## Costs

| Tier | Cost | Features |
|------|------|----------|
| Free | $0 | 0.1 CPU, 512MB RAM, cold starts |
| Starter | $7/mo | 0.5 CPU, 1GB RAM, shared instance |
| Pro | $12/mo | 1 CPU, 2GB RAM, dedicated instance |
| Premium | $19/mo | 2 CPU, 4GB RAM, always on |

For testing/development: **Free tier** is sufficient
For production: **Pro or Premium tier** recommended

---

## Deployment Checklist

- [ ] Repository created on GitHub
- [ ] All files committed (including model)
- [ ] requirements.txt includes all dependencies
- [ ] main.py tested locally
- [ ] render.yaml created (or settings configured in dashboard)
- [ ] Model file path correct
- [ ] Environment variables set
- [ ] Deployment successful (check logs)
- [ ] API responds to /health endpoint
- [ ] Test prediction works
- [ ] Auto-deploy enabled (optional)
- [ ] Custom domain configured (optional)

---

## Custom Domain Setup (Optional)

1. **Buy domain** (GoDaddy, Namecheap, etc.)

2. **Update DNS settings**:
   - Add CNAME record: `api.yourdomain.com` → `cancer-progression-api.onrender.com`

3. **In Render Dashboard**:
   - Settings → Custom Domains
   - Add: `api.yourdomain.com`
   - Verify SSL certificate auto-provisioned

---

## Support & Resources

- **Render Docs**: https://render.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Uvicorn Docs**: https://www.uvicorn.org
- **GitHub LFS**: https://git-lfs.com

---

**Version**: 1.0.0 | **Last Updated**: November 21, 2025

For issues or questions, check the logs in your Render dashboard or consult the documentation links above.
