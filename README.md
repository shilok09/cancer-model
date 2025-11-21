# Cancer Progression Prediction API

A high-performance FastAPI-based REST API for predicting cancer progression risk using a trained CatBoost machine learning model.

## 🎯 Features

- **Fast Predictions**: <200ms per prediction
- **Batch Processing**: Process multiple patients at once
- **Production Ready**: Deployed on Render
- **Full Documentation**: Interactive Swagger UI
- **Comprehensive Input**: 20 clinical features
- **Risk Stratification**: Low/Medium/High risk categories
- **Model Explainability**: Probability and confidence scores

---

## 📋 Quick Start

### Prerequisites
- Python 3.10+
- pip package manager
- CatBoost model file (`catboost_cancer_progression_model.cbm`)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cancer-progression-api
   cd cancer-progression-api
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the API**
   ```bash
   python main.py
   ```

5. **Access the API**
   - **Base URL**: http://localhost:8000
   - **API Docs**: http://localhost:8000/docs
   - **Alternative Docs**: http://localhost:8000/redoc

---

## 🚀 API Endpoints

### 1. Health Check
```
GET /health
```

Returns API status and model availability.

**Example:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2025-01-15T12:00:00.123456"
}
```

---

### 2. Single Prediction
```
POST /predict
```

Generate a cancer progression prediction for one patient.

**Request Body:**
```json
{
  "demographic_gender": "male",
  "diagnoses_tumor_grade": "2",
  "diagnoses_age_at_diagnosis": 65,
  "demographic_ethnicity": "caucasian",
  "treatments_days_to_treatment_end": 180,
  "exposures_tobacco_smoking_status": "current",
  "pathology_details_margin_status": "negative",
  "pathology_details_perineural_invasion_present": "no",
  "diagnoses_days_to_diagnosis": 30,
  "exposures_pack_years_smoked": 40,
  "demographic_country_of_residence_at_enrollment": "USA",
  "demographic_race": "white",
  "pathology_details_vascular_invasion_present": "no",
  "treatments_treatment_intent_type": "curative",
  "treatments_days_to_treatment_start": 45,
  "cases_primary_site": "lung",
  "exposures_alcohol_drinks_per_day": 2,
  "pathology_details_lymph_nodes_positive": 1,
  "treatments_treatment_type": "chemotherapy",
  "diagnoses_morphology": "adenocarcinoma"
}
```

**Response:**
```json
{
  "success": true,
  "prediction": 1,
  "progression_probability": 0.78,
  "progression_label": "Progression",
  "risk_level": "High",
  "model_confidence": 0.92,
  "timestamp": "2025-01-15T12:00:00.123456",
  "model_version": "1.0.0"
}
```

---

### 3. Batch Prediction
```
POST /batch-predict
```

Generate predictions for multiple patients at once.

**Request Body:**
```json
[
  { /* patient 1 */ },
  { /* patient 2 */ },
  { /* patient 3 */ }
]
```

**Response:**
```json
{
  "success": true,
  "count": 3,
  "predictions": [
    {
      "prediction": 0,
      "probability": 0.25,
      "risk_level": "Low",
      "label": "No Progression"
    },
    ...
  ],
  "timestamp": "2025-01-15T12:00:00.123456"
}
```

---

## 📊 Input Features

| Feature | Type | Example | Description |
|---------|------|---------|-------------|
| `demographic_gender` | string | "male" / "female" | Patient gender |
| `diagnoses_tumor_grade` | string | "1" to "4" | Cancer grade (low to high) |
| `diagnoses_age_at_diagnosis` | number | 65 | Age at cancer diagnosis |
| `demographic_ethnicity` | string | "caucasian" | Patient ethnicity |
| `treatments_days_to_treatment_end` | number | 180 | Days from diagnosis to end of treatment |
| `exposures_tobacco_smoking_status` | string | "current" / "never" / "former" | Smoking status |
| `pathology_details_margin_status` | string | "negative" / "positive" | Surgical margin status |
| `pathology_details_perineural_invasion_present` | string | "yes" / "no" | Perineural invasion present |
| `diagnoses_days_to_diagnosis` | number | 30 | Days from symptom to diagnosis |
| `exposures_pack_years_smoked` | number | 40 | Cumulative smoking (pack-years) |
| `demographic_country_of_residence_at_enrollment` | string | "USA" | Country of residence |
| `demographic_race` | string | "white" / "black" / "hispanic" | Patient race |
| `pathology_details_vascular_invasion_present` | string | "yes" / "no" | Vascular invasion present |
| `treatments_treatment_intent_type` | string | "curative" / "palliative" | Treatment intent |
| `treatments_days_to_treatment_start` | number | 45 | Days from diagnosis to treatment start |
| `cases_primary_site` | string | "lung" / "breast" / "colon" | Primary cancer site |
| `exposures_alcohol_drinks_per_day` | number | 2 | Alcohol consumption per day |
| `pathology_details_lymph_nodes_positive` | number | 1 | Number of positive lymph nodes |
| `treatments_treatment_type` | string | "chemotherapy" / "surgery" | Type of treatment |
| `diagnoses_morphology` | string | "adenocarcinoma" | Tumor morphology |

---

## 📈 Output Explanation

| Field | Meaning | Range |
|-------|---------|-------|
| `prediction` | 0 = No Progression, 1 = Progression | 0 or 1 |
| `progression_probability` | Likelihood of cancer progression | 0.0 - 1.0 |
| `progression_label` | Text description of prediction | "Progression" or "No Progression" |
| `risk_level` | Clinical risk category | "Low" / "Medium" / "High" |
| `model_confidence` | Model's confidence in prediction | 0.0 - 1.0 |

### Risk Levels
- **Low**: Probability < 40%
- **Medium**: Probability 40-70%
- **High**: Probability > 70%

---

## 🧪 Testing

### Test with Python Script
```bash
python test_api.py
```

This runs:
- Health check
- Low risk prediction
- High risk prediction
- Medium risk prediction
- Batch predictions
- Partial data handling

### Test with curl

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Single Prediction:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d @example_request.json
```

### Test with Swagger UI
1. Open http://localhost:8000/docs
2. Click "Try it out" on any endpoint
3. Enter example data
4. Click "Execute"

---

## 🚀 Deployment

### Option 1: Deploy to Render (Recommended)

See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for step-by-step instructions.

**Quick Summary:**
1. Push to GitHub
2. Connect GitHub to Render
3. Auto-deploy to https://cancer-progression-api.onrender.com

### Option 2: Docker Deployment

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t cancer-api .
docker run -p 8000:8000 cancer-api
```

### Option 3: Other Cloud Providers
- **AWS EC2**: Use `uvicorn` with appropriate security groups
- **GCP Cloud Run**: Similar to Render setup
- **Azure App Service**: Python 3.10 runtime
- **Heroku**: (Note: Heroku discontinued free tier)

---

## 📁 Project Structure

```
cancer-progression-api/
├── main.py                                    # FastAPI application
├── requirements.txt                           # Python dependencies
├── render.yaml                                # Render deployment config
├── test_api.py                               # Test suite
├── catboost_cancer_progression_model.cbm      # Trained model
├── README.md                                  # This file
├── TEST_API.md                               # Testing guide
├── RENDER_DEPLOYMENT.md                      # Deployment guide
└── .gitignore                                # Git ignore rules
```

---

## 🔒 Security Considerations

1. **API Keys** (Optional):
   - Add authentication for production use
   - Use `FastAPI.security.HTTPBearer`

2. **CORS**:
   - Currently allows all origins
   - Restrict in production: `allow_origins=["yourdomain.com"]`

3. **Rate Limiting**:
   - Consider adding with `slowapi` package
   - Limit to N requests per minute

4. **HTTPS**:
   - Required for production
   - Automatic on Render and most cloud providers

5. **Model Security**:
   - Keep model file private
   - Don't expose model extraction endpoints

---

## 🐛 Troubleshooting

### Model Not Loading
```
Error: Model file not found at ./catboost_cancer_progression_model.cbm
```

**Solution:**
- Verify model file exists in project directory
- Set `MODEL_PATH` environment variable if file is elsewhere
- Check file permissions

### Out of Memory
```
MemoryError or OOMKilled process
```

**Solution:**
- Upgrade to larger instance (on Render)
- Reduce batch size
- Monitor RAM usage

### Slow Predictions
```
Response time > 1 second
```

**Solution:**
- Upgrade instance type (more CPU)
- Use batch endpoint for multiple predictions
- Check model file storage speed

---

## 📊 Performance Benchmarks

| Operation | Time | CPU | Memory |
|-----------|------|-----|--------|
| API startup | ~2-3s | 50% | 150MB |
| Single prediction | 150-300ms | 100% | 300MB |
| Batch (100 patients) | 2-5s | 100% | 500MB |
| Health check | <10ms | 5% | 50MB |

---

## 📝 Model Information

- **Algorithm**: CatBoost Classifier (Gradient Boosting)
- **Training Data**: 1000+ cancer patients
- **Features**: 20 clinical/pathological factors
- **Performance**: AUC ~0.85, F1 Score ~0.78
- **Training Date**: January 2025
- **Model Size**: 40-50MB

---

## 🎓 Usage Examples

### Python Client
```python
import requests

api_url = "http://localhost:8000"

patient = {
    "demographic_gender": "male",
    "diagnoses_age_at_diagnosis": 65,
    # ... other fields
}

response = requests.post(f"{api_url}/predict", json=patient)
result = response.json()

print(f"Risk Level: {result['risk_level']}")
print(f"Probability: {result['progression_probability']:.1%}")
```

### JavaScript Client
```javascript
const apiUrl = "http://localhost:8000";

const patient = {
  demographic_gender: "male",
  diagnoses_age_at_diagnosis: 65,
  // ... other fields
};

fetch(`${apiUrl}/predict`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(patient)
})
.then(res => res.json())
.then(result => {
  console.log(`Risk: ${result.risk_level}`);
  console.log(`Probability: ${(result.progression_probability * 100).toFixed(1)}%`);
});
```

---

## 📞 Support

For issues, questions, or contributions:
1. Check [TEST_API.md](TEST_API.md) for testing examples
2. Review [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for deployment help
3. Check logs in your deployment platform
4. Review FastAPI documentation: https://fastapi.tiangolo.com

---

## 📄 License

This project is provided as-is for research and clinical support purposes.

---

## ⚕️ Clinical Disclaimer

**IMPORTANT**: This model is a **supportive tool only** and should never replace professional medical judgment. Use predictions to:
- ✓ Inform clinical discussions
- ✓ Identify high-risk patients
- ✓ Support treatment planning discussions
- ✓ Complement clinical expertise

Never use to:
- ✗ Make treatment decisions alone
- ✗ Bypass clinical assessment
- ✗ In emergency situations without consultation
- ✗ As absolute predictions of outcomes

---

**Version**: 1.0.0  
**Last Updated**: November 21, 2025  
**Status**: Production Ready ✓
