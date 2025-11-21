"""
Cancer Progression Prediction API
FastAPI REST endpoint for CatBoost model deployment on Render

Endpoint: POST /predict
Input: Patient features in JSON format
Output: Cancer progression prediction with probability and risk level
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.preprocessing import LabelEncoder
import os
import logging
from datetime import datetime
import pickle

# ============================================================================
# CONFIGURATION
# ============================================================================

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Model path - works both locally and on Render
MODEL_PATH = os.getenv('MODEL_PATH', './catboost_cancer_progression_model.cbm')

# Feature order (MUST match training data)
FEATURE_ORDER = [
    'demographic.gender',
    'diagnoses.tumor_grade',
    'diagnoses.age_at_diagnosis',
    'demographic.ethnicity',
    'treatments.days_to_treatment_end',
    'exposures.tobacco_smoking_status',
    'pathology_details.margin_status',
    'pathology_details.perineural_invasion_present',
    'diagnoses.days_to_diagnosis',
    'exposures.pack_years_smoked',
    'demographic.country_of_residence_at_enrollment',
    'demographic.race',
    'pathology_details.vascular_invasion_present',
    'treatments.treatment_intent_type',
    'treatments.days_to_treatment_start',
    'cases.primary_site',
    'exposures.alcohol_drinks_per_day',
    'pathology_details.lymph_nodes_positive',
    'treatments.treatment_type',
    'diagnoses.morphology',
]

# Categorical features (for CatBoost)
CATEGORICAL_FEATURES = [
    'demographic.gender',
    'diagnoses.tumor_grade',
    'demographic.ethnicity',
    'exposures.tobacco_smoking_status',
    'pathology_details.margin_status',
    'pathology_details.perineural_invasion_present',
    'demographic.country_of_residence_at_enrollment',
    'demographic.race',
    'pathology_details.vascular_invasion_present',
    'treatments.treatment_intent_type',
    'cases.primary_site',
    'treatments.treatment_type',
    'diagnoses.morphology',
]

# Categorical feature mappings (learned from training data)
CATEGORY_MAPPINGS = {
    'demographic.gender': {'female': 0, 'male': 1, 'unknown': 2},
    'diagnoses.tumor_grade': {'1': 0, '2': 1, '3': 2, '4': 3, 'unknown': 4},
    'demographic.ethnicity': {'caucasian': 0, 'african_american': 1, 'hispanic': 2, 'asian': 3, 'unknown': 4},
    'exposures.tobacco_smoking_status': {'never': 0, 'current': 1, 'former': 2, 'unknown': 3},
    'pathology_details.margin_status': {'negative': 0, 'positive': 1, 'unknown': 2},
    'pathology_details.perineural_invasion_present': {'no': 0, 'yes': 1, 'unknown': 2},
    'demographic.country_of_residence_at_enrollment': {'USA': 0, 'Canada': 1, 'UK': 2, 'other': 3, 'unknown': 4},
    'demographic.race': {'white': 0, 'black': 1, 'asian': 2, 'other': 3, 'unknown': 4},
    'pathology_details.vascular_invasion_present': {'no': 0, 'yes': 1, 'unknown': 2},
    'treatments.treatment_intent_type': {'curative': 0, 'palliative': 1, 'unknown': 2},
    'cases.primary_site': {'breast': 0, 'lung': 1, 'colon': 2, 'prostate': 3, 'other': 4, 'unknown': 5},
    'treatments.treatment_type': {'surgery': 0, 'chemotherapy': 1, 'radiation': 2, 'immunotherapy': 3, 'unknown': 4},
    'diagnoses.morphology': {'infiltrating_ductal_carcinoma': 0, 'adenocarcinoma': 1, 'small_cell_carcinoma': 2, 'unknown': 3},
}

# ============================================================================
# FASTAPI APP SETUP
# ============================================================================

app = FastAPI(
    title="Cancer Progression Prediction API",
    description="ML-powered API for predicting cancer progression risk",
    version="1.0.0"
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# GLOBAL STATE
# ============================================================================

model = None
model_loaded = False
model_feature_names = []
model_categorical_indices = []

# ============================================================================
# PYDANTIC MODELS (Request/Response)
# ============================================================================

class PredictionRequest(BaseModel):
    """Input schema for prediction request - all 56 features"""
    cases_disease_type: Optional[str] = None
    cases_primary_site: Optional[str] = None
    demographic_gender: Optional[str] = None
    demographic_race: Optional[str] = None
    demographic_ethnicity: Optional[str] = None
    diagnoses_age_at_diagnosis: Optional[float] = None
    diagnoses_primary_diagnosis: Optional[str] = None
    diagnoses_primary_disease: Optional[str] = None
    diagnoses_last_known_disease_status: Optional[str] = None
    diagnoses_progression_or_recurrence: Optional[str] = None
    diagnoses_tumor_grade: Optional[str] = None
    diagnoses_tumor_burden: Optional[str] = None
    diagnoses_morphology: Optional[str] = None
    diagnoses_laterality: Optional[str] = None
    diagnoses_metastasis_at_diagnosis: Optional[str] = None
    diagnoses_days_to_diagnosis: Optional[float] = None
    diagnoses_days_to_recurrence: Optional[float] = None
    treatments_treatment_type: Optional[str] = None
    treatments_treatment_outcome: Optional[str] = None
    treatments_treatment_intent_type: Optional[str] = None
    treatments_days_to_treatment_start: Optional[float] = None
    treatments_days_to_treatment_end: Optional[float] = None
    demographic_education_level: Optional[str] = None
    demographic_marital_status: Optional[str] = None
    demographic_occupation_duration_years: Optional[float] = None
    demographic_country_of_residence_at_enrollment: Optional[str] = None
    demographic_population_group: Optional[str] = None
    exposures_smoking_frequency: Optional[str] = None
    exposures_tobacco_smoking_status: Optional[str] = None
    exposures_pack_years_smoked: Optional[float] = None
    exposures_years_smoked: Optional[float] = None
    exposures_cigarettes_per_day: Optional[float] = None
    exposures_asbestos_exposure: Optional[str] = None
    exposures_radon_exposure: Optional[str] = None
    exposures_environmental_tobacco_smoke_exposure: Optional[str] = None
    exposures_alcohol_drinks_per_day: Optional[float] = None
    exposures_alcohol_intensity: Optional[str] = None
    exposures_occupation_duration_years: Optional[float] = None
    exposures_occupation_type: Optional[str] = None
    follow_ups_imaging_result: Optional[str] = None
    follow_ups_imaging_result_1: Optional[str] = None
    pathology_details_tumor_burden: Optional[str] = None
    pathology_details_greatest_tumor_dimension: Optional[float] = None
    pathology_details_margin_status: Optional[str] = None
    pathology_details_lymph_node_involvement: Optional[str] = None
    pathology_details_lymph_nodes_positive: Optional[float] = None
    pathology_details_lymph_nodes_removed: Optional[float] = None
    pathology_details_lymphatic_invasion_present: Optional[str] = None
    pathology_details_perineural_invasion_present: Optional[str] = None
    pathology_details_vascular_invasion_present: Optional[str] = None
    pathology_details_residual_tumor: Optional[str] = None
    pathology_details_necrosis_percent: Optional[float] = None
    pathology_details_morphologic_architectural_pattern: Optional[str] = None
    pathology_details_circumferential_resection_margin: Optional[str] = None
    pathology_details_epithelioid_cell_percent: Optional[float] = None
    pathology_details_spindle_cell_percent: Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "cases_disease_type": "cancer",
                "cases_primary_site": "lung",
                "demographic_gender": "male",
                "demographic_race": "white",
                "demographic_ethnicity": "caucasian",
                "diagnoses_age_at_diagnosis": 65,
                "diagnoses_primary_diagnosis": "adenocarcinoma_lung",
                "diagnoses_primary_disease": "lung_cancer",
                "diagnoses_last_known_disease_status": "tumor_free",
                "diagnoses_progression_or_recurrence": "no",
                "diagnoses_tumor_grade": "2",
                "diagnoses_tumor_burden": "medium",
                "diagnoses_morphology": "adenocarcinoma",
                "diagnoses_laterality": "unilateral",
                "diagnoses_metastasis_at_diagnosis": "m0",
                "diagnoses_days_to_diagnosis": 30,
                "diagnoses_days_to_recurrence": 180,
                "treatments_treatment_type": "chemotherapy",
                "treatments_treatment_outcome": "partial_remission",
                "treatments_treatment_intent_type": "curative",
                "treatments_days_to_treatment_start": 45,
                "treatments_days_to_treatment_end": 180,
                "demographic_education_level": "some_college",
                "demographic_marital_status": "single",
                "demographic_occupation_duration_years": 30,
                "demographic_country_of_residence_at_enrollment": "USA",
                "demographic_population_group": "not_reported",
                "exposures_smoking_frequency": "daily",
                "exposures_tobacco_smoking_status": "current",
                "exposures_pack_years_smoked": 40,
                "exposures_years_smoked": 30,
                "exposures_cigarettes_per_day": 20,
                "exposures_asbestos_exposure": "no",
                "exposures_radon_exposure": "yes",
                "exposures_environmental_tobacco_smoke_exposure": "yes",
                "exposures_alcohol_drinks_per_day": 2,
                "exposures_alcohol_intensity": "weekly",
                "exposures_occupation_duration_years": 25,
                "exposures_occupation_type": "manufacturing",
                "follow_ups_imaging_result": "stable",
                "follow_ups_imaging_result_1": "stable",
                "pathology_details_tumor_burden": "medium",
                "pathology_details_greatest_tumor_dimension": 4.0,
                "pathology_details_margin_status": "negative",
                "pathology_details_lymph_node_involvement": "yes",
                "pathology_details_lymph_nodes_positive": 1,
                "pathology_details_lymph_nodes_removed": 8,
                "pathology_details_lymphatic_invasion_present": "no",
                "pathology_details_perineural_invasion_present": "no",
                "pathology_details_vascular_invasion_present": "no",
                "pathology_details_residual_tumor": "r1",
                "pathology_details_necrosis_percent": 20,
                "pathology_details_morphologic_architectural_pattern": "acinar",
                "pathology_details_circumferential_resection_margin": "negative",
                "pathology_details_epithelioid_cell_percent": 70,
                "pathology_details_spindle_cell_percent": 30
            }
        }


class PredictionResponse(BaseModel):
    """Output schema for prediction response"""
    success: bool
    prediction: int
    progression_probability: float
    progression_label: str
    risk_level: str
    model_confidence: float
    timestamp: str
    model_version: str = "1.0.0"


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    timestamp: str


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def load_model():
    """Load CatBoost model from disk"""
    global model, model_loaded, model_feature_names, model_categorical_indices
    
    try:
        if os.path.exists(MODEL_PATH):
            model = CatBoostClassifier()
            model.load_model(MODEL_PATH)
            model_loaded = True
            
            # Get feature names from model
            model_feature_names = list(model.feature_names_) if model.feature_names_ else []
            
            if model_feature_names:
                logger.info(f"✓ Model loaded successfully from {MODEL_PATH}")
                logger.info(f"✓ Model expects {len(model_feature_names)} features")
                logger.info(f"✓ Features: {model_feature_names}")
                
                # Identify which features are categorical
                model_categorical_indices = []
                for i, feat in enumerate(model_feature_names):
                    if feat in CATEGORICAL_FEATURES:
                        model_categorical_indices.append(i)
                logger.info(f"✓ Categorical feature indices: {model_categorical_indices}")
            else:
                logger.warning("⚠ Model loaded but feature names not available")
            
            return True
        else:
            logger.error(f"✗ Model file not found at {MODEL_PATH}")
            model_loaded = False
            return False
    except Exception as e:
        logger.error(f"✗ Error loading model: {str(e)}")
        model_loaded = False
        return False


def get_categorical_feature_names():
    """Get names of categorical features in correct order"""
    cat_feature_names = []
    for feature in FEATURE_ORDER:
        if feature in CATEGORICAL_FEATURES:
            cat_feature_names.append(feature)
    return cat_feature_names


def prepare_features(data: Dict[str, Any]) -> pd.DataFrame:
    """
    Prepare input features in correct order for model
    
    Args:
        data: Dictionary with feature values (underscores instead of dots)
    
    Returns:
        Pandas DataFrame with features in correct order matching model training
    """
    if model is None or not model_feature_names:
        raise ValueError("Model not loaded or feature names not available")
    
    features = {}
    
    for feature_name in model_feature_names:
        # Convert dot notation to underscore for lookup in request data
        key = feature_name.replace('.', '_')
        
        # Get value from input
        value = data.get(key)
        
        # Handle missing values based on feature type
        if value is None or value == '' or value == 'None':
            # For categorical features, use 'Unknown' as a valid string
            if feature_name in CATEGORICAL_FEATURES:
                value = 'Unknown'
            else:
                # For numeric features, use NaN
                value = np.nan
        else:
            # For numeric features, try to convert to float
            if feature_name not in CATEGORICAL_FEATURES:
                try:
                    value = float(value)
                except (ValueError, TypeError):
                    value = np.nan
            # For categorical features, keep as string
            value = str(value)
        
        features[feature_name] = value
    
    # Create DataFrame with features
    df = pd.DataFrame([features])
    
    # Reorder to match model's expected feature order
    df = df[model_feature_names]
    
    # Ensure all categorical columns are object dtype (strings)
    # and replace any remaining NaN with 'Unknown'
    for cat_idx in model_categorical_indices:
        col_name = model_feature_names[cat_idx]
        if col_name in df.columns:
            # Replace NaN with 'Unknown' for categorical features
            df[col_name] = df[col_name].fillna('Unknown')
            # Ensure it's a string type
            df[col_name] = df[col_name].astype(str)
    
    return df


def get_risk_category(probability: float) -> str:
    """Determine risk category from probability"""
    if probability >= 0.7:
        return "High"
    elif probability >= 0.4:
        return "Medium"
    else:
        return "Low"


def get_progression_label(prediction: int) -> str:
    """Convert prediction to label"""
    return "Progression" if prediction == 1 else "No Progression"


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    logger.info("Starting Cancer Progression Prediction API...")
    load_model()
    if model_loaded:
        logger.info("✓ API ready for predictions")
    else:
        logger.warning("⚠️  Model not loaded - API will return errors for predictions")


@app.get("/", tags=["Info"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Cancer Progression Prediction API",
        "version": "1.0.0",
        "status": "running",
        "model_loaded": model_loaded,
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "docs": "/docs",
            "openapi": "/openapi.json"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint
    
    Returns:
        Health status and model availability
    """
    return HealthResponse(
        status="healthy" if model_loaded else "degraded",
        model_loaded=model_loaded,
        timestamp=datetime.now().isoformat()
    )


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict(request: PredictionRequest):
    """
    Generate cancer progression prediction
    
    Args:
        request: Patient features in PredictionRequest format
    
    Returns:
        Prediction with probability, risk level, and confidence
    
    Raises:
        HTTPException: If model not loaded or prediction fails
    """
    
    # Check if model is loaded
    if not model_loaded or model is None:
        logger.error("Prediction requested but model not loaded")
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. API temporarily unavailable."
        )
    
    try:
        # Convert request to dictionary using model_dump (Pydantic v2)
        data_dict = request.model_dump()
        
        # Prepare features in correct order
        X = prepare_features(data_dict)
        
        # Make prediction (model already knows categorical features from training)
        prediction = model.predict(X)[0]
        probability = model.predict_proba(X)[0, 1]
        
        # Generate outputs
        progression_label = get_progression_label(int(prediction))
        risk_level = get_risk_category(probability)
        
        # Calculate confidence (distance from 0.5)
        confidence = 1.0 - abs(probability - 0.5) * 2
        
        logger.info(f"✓ Prediction generated: {progression_label} ({probability:.4f})")
        
        return PredictionResponse(
            success=True,
            prediction=int(prediction),
            progression_probability=float(probability),
            progression_label=progression_label,
            risk_level=risk_level,
            model_confidence=float(confidence),
            timestamp=datetime.now().isoformat(),
            model_version="1.0.0"
        )
    
    except Exception as e:
        logger.error(f"✗ Prediction error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Prediction failed: {str(e)}"
        )


@app.post("/batch-predict", tags=["Prediction"])
async def batch_predict(requests: list[PredictionRequest]):
    """
    Generate predictions for multiple patients
    
    Args:
        requests: List of PredictionRequest objects
    
    Returns:
        List of predictions
    """
    
    if not model_loaded or model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded"
        )
    
    try:
        predictions = []
        
        for request in requests:
            # Prepare features
            data_dict = request.model_dump()
            X = prepare_features(data_dict)
            
            # Make prediction (model already knows categorical features from training)
            pred = model.predict(X)[0]
            prob = model.predict_proba(X)[0, 1]
            
            predictions.append({
                "prediction": int(pred),
                "probability": float(prob),
                "risk_level": get_risk_category(prob),
                "label": get_progression_label(int(pred))
            })
        
        logger.info(f"✓ Batch predictions generated for {len(requests)} patients")
        
        return {
            "success": True,
            "count": len(predictions),
            "predictions": predictions,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"✗ Batch prediction error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Batch prediction failed: {str(e)}"
        )


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment or use default
    port = int(os.getenv("PORT", 8000))
    
    print("\n" + "="*80)
    print("Cancer Progression Prediction API")
    print("="*80)
    print(f"\n✓ Starting server on http://0.0.0.0:{port}")
    print(f"✓ API docs available at http://localhost:{port}/docs")
    print(f"✓ Model: {MODEL_PATH}")
    print("\n" + "="*80 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
