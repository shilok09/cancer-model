# Cancer Progression Prediction API - Testing Examples

## 1. Basic Health Check

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2025-01-15T12:00:00.123456"
}
```

---

## 2. Single Prediction - Low Risk Patient

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "demographic_gender": "female",
    "diagnoses_tumor_grade": "1",
    "diagnoses_age_at_diagnosis": 45,
    "demographic_ethnicity": "caucasian",
    "treatments_days_to_treatment_end": 90,
    "exposures_tobacco_smoking_status": "never",
    "pathology_details_margin_status": "negative",
    "pathology_details_perineural_invasion_present": "no",
    "diagnoses_days_to_diagnosis": 15,
    "exposures_pack_years_smoked": 0,
    "demographic_country_of_residence_at_enrollment": "USA",
    "demographic_race": "white",
    "pathology_details_vascular_invasion_present": "no",
    "treatments_treatment_intent_type": "curative",
    "treatments_days_to_treatment_start": 30,
    "cases_primary_site": "breast",
    "exposures_alcohol_drinks_per_day": 0,
    "pathology_details_lymph_nodes_positive": 0,
    "treatments_treatment_type": "surgery",
    "diagnoses_morphology": "infiltrating_ductal_carcinoma"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "prediction": 0,
  "progression_probability": 0.25,
  "progression_label": "No Progression",
  "risk_level": "Low",
  "model_confidence": 0.50,
  "timestamp": "2025-01-15T12:00:00.123456",
  "model_version": "1.0.0"
}
```

---

## 3. Single Prediction - High Risk Patient

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "demographic_gender": "male",
    "diagnoses_tumor_grade": "4",
    "diagnoses_age_at_diagnosis": 72,
    "demographic_ethnicity": "african_american",
    "treatments_days_to_treatment_end": 240,
    "exposures_tobacco_smoking_status": "current",
    "pathology_details_margin_status": "positive",
    "pathology_details_perineural_invasion_present": "yes",
    "diagnoses_days_to_diagnosis": 45,
    "exposures_pack_years_smoked": 60,
    "demographic_country_of_residence_at_enrollment": "USA",
    "demographic_race": "black",
    "pathology_details_vascular_invasion_present": "yes",
    "treatments_treatment_intent_type": "palliative",
    "treatments_days_to_treatment_start": 60,
    "cases_primary_site": "lung",
    "exposures_alcohol_drinks_per_day": 4,
    "pathology_details_lymph_nodes_positive": 5,
    "treatments_treatment_type": "chemotherapy",
    "diagnoses_morphology": "small_cell_carcinoma"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "prediction": 1,
  "progression_probability": 0.85,
  "progression_label": "Progression",
  "risk_level": "High",
  "model_confidence": 0.70,
  "timestamp": "2025-01-15T12:00:00.123456",
  "model_version": "1.0.0"
}
```

---

## 4. Python Test Script

```python
import requests
import json

API_URL = "http://localhost:8000"

# Test data
patient_data = {
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

# Make prediction
response = requests.post(f"{API_URL}/predict", json=patient_data)
result = response.json()

print("=" * 80)
print("CANCER PROGRESSION PREDICTION")
print("=" * 80)
print(f"\nRisk Level: {result['risk_level']}")
print(f"Probability: {result['progression_probability']:.2%}")
print(f"Prediction: {result['progression_label']}")
print(f"Confidence: {result['model_confidence']:.2%}")
print(f"\nTimestamp: {result['timestamp']}")
print("=" * 80)
```

---

## 5. JavaScript/Fetch Test

```javascript
const API_URL = "http://localhost:8000";

const patientData = {
  demographic_gender: "female",
  diagnoses_tumor_grade: "2",
  diagnoses_age_at_diagnosis: 58,
  demographic_ethnicity: "hispanic",
  treatments_days_to_treatment_end: 120,
  exposures_tobacco_smoking_status: "former",
  pathology_details_margin_status: "negative",
  pathology_details_perineural_invasion_present: "no",
  diagnoses_days_to_diagnosis: 20,
  exposures_pack_years_smoked: 15,
  demographic_country_of_residence_at_enrollment: "USA",
  demographic_race: "hispanic",
  pathology_details_vascular_invasion_present: "no",
  treatments_treatment_intent_type: "curative",
  treatments_days_to_treatment_start: 40,
  cases_primary_site: "colon",
  exposures_alcohol_drinks_per_day: 1,
  pathology_details_lymph_nodes_positive: 0,
  treatments_treatment_type: "surgery",
  diagnoses_morphology: "adenocarcinoma"
};

fetch(`${API_URL}/predict`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(patientData)
})
.then(response => response.json())
.then(result => {
  console.log("Prediction Result:");
  console.log(`Risk Level: ${result.risk_level}`);
  console.log(`Probability: ${(result.progression_probability * 100).toFixed(1)}%`);
  console.log(`Prediction: ${result.progression_label}`);
  console.log(`Confidence: ${(result.model_confidence * 100).toFixed(1)}%`);
})
.catch(error => console.error("Error:", error));
```

---

## 6. Batch Prediction

```bash
curl -X POST http://localhost:8000/batch-predict \
  -H "Content-Type: application/json" \
  -d '[
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
    },
    {
      "demographic_gender": "female",
      "diagnoses_tumor_grade": "1",
      "diagnoses_age_at_diagnosis": 52,
      "demographic_ethnicity": "caucasian",
      "treatments_days_to_treatment_end": 90,
      "exposures_tobacco_smoking_status": "never",
      "pathology_details_margin_status": "negative",
      "pathology_details_perineural_invasion_present": "no",
      "diagnoses_days_to_diagnosis": 15,
      "exposures_pack_years_smoked": 0,
      "demographic_country_of_residence_at_enrollment": "USA",
      "demographic_race": "white",
      "pathology_details_vascular_invasion_present": "no",
      "treatments_treatment_intent_type": "curative",
      "treatments_days_to_treatment_start": 30,
      "cases_primary_site": "breast",
      "exposures_alcohol_drinks_per_day": 0,
      "pathology_details_lymph_nodes_positive": 0,
      "treatments_treatment_type": "surgery",
      "diagnoses_morphology": "infiltrating_ductal_carcinoma"
    }
  ]'
```

---

## 7. Interactive API Testing

Use the built-in Swagger UI documentation:

```
http://localhost:8000/docs
```

Or ReDoc:
```
http://localhost:8000/redoc
```

---

## 8. Testing with Postman

1. Import the following as a new request:
   - **Method**: POST
   - **URL**: http://localhost:8000/predict
   - **Headers**: Content-Type: application/json
   - **Body** (raw JSON): Use example from section 2

---

## 9. Response Interpretation

| Field | Meaning | Range |
|-------|---------|-------|
| `prediction` | 0 = No Progression, 1 = Progression | 0 or 1 |
| `progression_probability` | Likelihood of progression | 0.0 - 1.0 |
| `risk_level` | Clinical risk category | Low / Medium / High |
| `model_confidence` | Model prediction certainty | 0.0 - 1.0 |
| `progression_label` | Text description | "Progression" or "No Progression" |

---

## 10. Error Responses

### Model Not Loaded
```json
{
  "detail": "Model not loaded. API temporarily unavailable."
}
```
Status: 503

### Invalid Request
```json
{
  "detail": "Prediction failed: [error message]"
}
```
Status: 400

---

## Quick Start Testing

### 1. Start the API
```bash
python main.py
```

### 2. Check health in another terminal
```bash
curl http://localhost:8000/health
```

### 3. Test prediction
```bash
python test_api.py  # Using the Python script from section 4
```

### 4. View API documentation
Open browser to: http://localhost:8000/docs

---

## Performance Notes

- Single prediction: <200ms
- Batch prediction (100 patients): <5s
- Model loading: ~2-3 seconds on startup
- API startup: ~5 seconds total

---

**Version**: 1.0.0 | **Date**: November 21, 2025
