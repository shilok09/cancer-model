"""
Local testing script for Cancer Progression Prediction API
Run this to test the API without needing curl or Postman
"""

import requests
import json
from typing import Dict, Any

# Configuration
API_URL = "http://localhost:8000"

# Test data - Low risk patient (based on actual dataset)
LOW_RISK_PATIENT = {
    "cases_disease_type": "Squamous Cell Neoplasms",
    "cases_primary_site": "Tongue",
    "demographic_gender": "female",
    "demographic_race": "white",
    "demographic_ethnicity": "not hispanic or latino",
    "diagnoses_age_at_diagnosis": 24650,
    "diagnoses_primary_diagnosis": "Squamous cell carcinoma",
    "diagnoses_primary_disease": "unknown",
    "diagnoses_last_known_disease_status": "tumor_free",
    "diagnoses_progression_or_recurrence": "no",
    "diagnoses_tumor_grade": "G1",
    "diagnoses_tumor_burden": "low",
    "diagnoses_morphology": "8070/3",
    "diagnoses_laterality": "Right",
    "diagnoses_metastasis_at_diagnosis": "no",
    "diagnoses_days_to_diagnosis": 0,
    "diagnoses_days_to_recurrence": 5000,
    "treatments_treatment_type": "Radiation",
    "treatments_treatment_outcome": "Complete Response",
    "treatments_treatment_intent_type": "curative",
    "treatments_days_to_treatment_start": 109,
    "treatments_days_to_treatment_end": 151,
    "demographic_education_level": "college",
    "demographic_marital_status": "married",
    "demographic_occupation_duration_years": 30,
    "demographic_country_of_residence_at_enrollment": "United States",
    "demographic_population_group": "not_reported",
    "exposures_smoking_frequency": "reformed",
    "exposures_tobacco_smoking_status": "Current Reformed Smoker",
    "exposures_pack_years_smoked": 30,
    "exposures_years_smoked": 40,
    "exposures_cigarettes_per_day": 15,
    "exposures_asbestos_exposure": "no",
    "exposures_radon_exposure": "no",
    "exposures_environmental_tobacco_smoke_exposure": "no",
    "exposures_alcohol_drinks_per_day": 0,
    "exposures_alcohol_intensity": "never",
    "exposures_occupation_duration_years": 30,
    "exposures_occupation_type": "professional",
    "follow_ups_imaging_result": "negative",
    "follow_ups_imaging_result_1": "negative",
    "pathology_details_tumor_burden": "low",
    "pathology_details_greatest_tumor_dimension": 2.5,
    "pathology_details_margin_status": "negative",
    "pathology_details_lymph_node_involvement": "no",
    "pathology_details_lymph_nodes_positive": 0,
    "pathology_details_lymph_nodes_removed": 5,
    "pathology_details_lymphatic_invasion_present": "no",
    "pathology_details_perineural_invasion_present": "no",
    "pathology_details_vascular_invasion_present": "no",
    "pathology_details_residual_tumor": "r0",
    "pathology_details_necrosis_percent": 5,
    "pathology_details_morphologic_architectural_pattern": "No Progression",
    "pathology_details_circumferential_resection_margin": "Low Risk",
    "pathology_details_epithelioid_cell_percent": 80,
    "pathology_details_spindle_cell_percent": 20
}

# Test data - High risk patient
HIGH_RISK_PATIENT = {
    "cases_disease_type": "Epithelial Neoplasms",
    "cases_primary_site": "Lung",
    "demographic_gender": "male",
    "demographic_race": "black",
    "demographic_ethnicity": "not hispanic or latino",
    "diagnoses_age_at_diagnosis": 26280,
    "diagnoses_primary_diagnosis": "Small cell lung cancer",
    "diagnoses_primary_disease": "small_cell_carcinoma",
    "diagnoses_last_known_disease_status": "with_tumor",
    "diagnoses_progression_or_recurrence": "yes",
    "diagnoses_tumor_grade": "G4",
    "diagnoses_tumor_burden": "high",
    "diagnoses_morphology": "8041/3",
    "diagnoses_laterality": "Bilateral",
    "diagnoses_metastasis_at_diagnosis": "m1",
    "diagnoses_days_to_diagnosis": 0,
    "diagnoses_days_to_recurrence": 180,
    "treatments_treatment_type": "Chemotherapy",
    "treatments_treatment_outcome": "Progressive Disease",
    "treatments_treatment_intent_type": "palliative",
    "treatments_days_to_treatment_start": 60,
    "treatments_days_to_treatment_end": 240,
    "demographic_education_level": "high_school",
    "demographic_marital_status": "divorced",
    "demographic_occupation_duration_years": 45,
    "demographic_country_of_residence_at_enrollment": "United States",
    "demographic_population_group": "not_reported",
    "exposures_smoking_frequency": "daily",
    "exposures_tobacco_smoking_status": "Current Smoker",
    "exposures_pack_years_smoked": 60,
    "exposures_years_smoked": 40,
    "exposures_cigarettes_per_day": 40,
    "exposures_asbestos_exposure": "yes",
    "exposures_radon_exposure": "yes",
    "exposures_environmental_tobacco_smoke_exposure": "yes",
    "exposures_alcohol_drinks_per_day": 4,
    "exposures_alcohol_intensity": "daily",
    "exposures_occupation_duration_years": 30,
    "exposures_occupation_type": "industrial_worker",
    "follow_ups_imaging_result": "positive",
    "follow_ups_imaging_result_1": "positive",
    "pathology_details_tumor_burden": "high",
    "pathology_details_greatest_tumor_dimension": 8.5,
    "pathology_details_margin_status": "positive",
    "pathology_details_lymph_node_involvement": "yes",
    "pathology_details_lymph_nodes_positive": 5,
    "pathology_details_lymph_nodes_removed": 12,
    "pathology_details_lymphatic_invasion_present": "yes",
    "pathology_details_perineural_invasion_present": "yes",
    "pathology_details_vascular_invasion_present": "yes",
    "pathology_details_residual_tumor": "r2",
    "pathology_details_necrosis_percent": 45,
    "pathology_details_morphologic_architectural_pattern": "Progression",
    "pathology_details_circumferential_resection_margin": "High Risk",
    "pathology_details_epithelioid_cell_percent": 30,
    "pathology_details_spindle_cell_percent": 70
}

# Test data - Medium risk patient
MEDIUM_RISK_PATIENT = {
    "cases_disease_type": "Adenomas and Adenocarcinomas",
    "cases_primary_site": "Colon",
    "demographic_gender": "male",
    "demographic_race": "white",
    "demographic_ethnicity": "not hispanic or latino",
    "diagnoses_age_at_diagnosis": 23725,
    "diagnoses_primary_diagnosis": "Adenocarcinoma",
    "diagnoses_primary_disease": "colorectal_cancer",
    "diagnoses_last_known_disease_status": "tumor_free",
    "diagnoses_progression_or_recurrence": "no",
    "diagnoses_tumor_grade": "G2",
    "diagnoses_tumor_burden": "medium",
    "diagnoses_morphology": "8140/3",
    "diagnoses_laterality": "Left",
    "diagnoses_metastasis_at_diagnosis": "m0",
    "diagnoses_days_to_diagnosis": 0,
    "diagnoses_days_to_recurrence": 365,
    "treatments_treatment_type": "Surgery",
    "treatments_treatment_outcome": "Partial Response",
    "treatments_treatment_intent_type": "curative",
    "treatments_days_to_treatment_start": 30,
    "treatments_days_to_treatment_end": 60,
    "demographic_education_level": "some_college",
    "demographic_marital_status": "married",
    "demographic_occupation_duration_years": 35,
    "demographic_country_of_residence_at_enrollment": "United States",
    "demographic_population_group": "not_reported",
    "exposures_smoking_frequency": "former",
    "exposures_tobacco_smoking_status": "Former Smoker",
    "exposures_pack_years_smoked": 25,
    "exposures_years_smoked": 30,
    "exposures_cigarettes_per_day": 15,
    "exposures_asbestos_exposure": "no",
    "exposures_radon_exposure": "no",
    "exposures_environmental_tobacco_smoke_exposure": "yes",
    "exposures_alcohol_drinks_per_day": 1,
    "exposures_alcohol_intensity": "weekly",
    "exposures_occupation_duration_years": 28,
    "exposures_occupation_type": "service_industry",
    "follow_ups_imaging_result": "stable",
    "follow_ups_imaging_result_1": "stable",
    "pathology_details_tumor_burden": "medium",
    "pathology_details_greatest_tumor_dimension": 4.5,
    "pathology_details_margin_status": "negative",
    "pathology_details_lymph_node_involvement": "yes",
    "pathology_details_lymph_nodes_positive": 1,
    "pathology_details_lymph_nodes_removed": 10,
    "pathology_details_lymphatic_invasion_present": "no",
    "pathology_details_perineural_invasion_present": "no",
    "pathology_details_vascular_invasion_present": "no",
    "pathology_details_residual_tumor": "r1",
    "pathology_details_necrosis_percent": 15,
    "pathology_details_morphologic_architectural_pattern": "glandular",
    "pathology_details_circumferential_resection_margin": "negative",
    "pathology_details_epithelioid_cell_percent": 100,
    "pathology_details_spindle_cell_percent": 0
}


def print_header(title: str):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_result(result: Dict[str, Any]):
    """Print formatted prediction result"""
    print(f"\n✓ Prediction Generated Successfully\n")
    print(f"  Risk Level:           {result['risk_level']}")
    print(f"  Progression:          {result['progression_label']}")
    print(f"  Probability:          {result['progression_probability']:.1%}")
    print(f"  Model Confidence:     {result['model_confidence']:.1%}")
    print(f"  Timestamp:            {result['timestamp']}")
    print(f"  Model Version:        {result['model_version']}")


def test_health_check():
    """Test API health check endpoint"""
    print_header("TEST 1: Health Check")
    
    try:
        response = requests.get(f"{API_URL}/health")
        result = response.json()
        
        print(f"\n✓ Health check successful")
        print(f"  Status:       {result['status']}")
        print(f"  Model Loaded: {result['model_loaded']}")
        print(f"  Timestamp:    {result['timestamp']}")
        
        return True
    except Exception as e:
        print(f"\n✗ Health check failed: {str(e)}")
        return False


def test_low_risk_prediction():
    """Test prediction for low-risk patient"""
    print_header("TEST 2: Low Risk Patient Prediction")
    
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=LOW_RISK_PATIENT,
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"\n✗ Request failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
        
        result = response.json()
        print_result(result)
        
        # Validate low risk
        if result['risk_level'] == 'Low':
            print(f"\n✓ Correctly predicted LOW RISK")
        else:
            print(f"\n⚠ Expected LOW RISK but got {result['risk_level']}")
        
        return True
    except Exception as e:
        print(f"\n✗ Prediction failed: {str(e)}")
        return False


def test_high_risk_prediction():
    """Test prediction for high-risk patient"""
    print_header("TEST 3: High Risk Patient Prediction")
    
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=HIGH_RISK_PATIENT,
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"\n✗ Request failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
        
        result = response.json()
        print_result(result)
        
        # Validate high risk
        if result['risk_level'] == 'High':
            print(f"\n✓ Correctly predicted HIGH RISK")
        else:
            print(f"\n⚠ Expected HIGH RISK but got {result['risk_level']}")
        
        return True
    except Exception as e:
        print(f"\n✗ Prediction failed: {str(e)}")
        return False


def test_medium_risk_prediction():
    """Test prediction for medium-risk patient"""
    print_header("TEST 4: Medium Risk Patient Prediction")
    
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=MEDIUM_RISK_PATIENT,
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"\n✗ Request failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
        
        result = response.json()
        print_result(result)
        
        # Validate medium risk
        if result['risk_level'] == 'Medium':
            print(f"\n✓ Correctly predicted MEDIUM RISK")
        else:
            print(f"\n⚠ Expected MEDIUM RISK but got {result['risk_level']}")
        
        return True
    except Exception as e:
        print(f"\n✗ Prediction failed: {str(e)}")
        return False


def test_batch_prediction():
    """Test batch prediction for multiple patients"""
    print_header("TEST 5: Batch Prediction (Multiple Patients)")
    
    try:
        response = requests.post(
            f"{API_URL}/batch-predict",
            json=[LOW_RISK_PATIENT, HIGH_RISK_PATIENT, MEDIUM_RISK_PATIENT],
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"\n✗ Request failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
        
        result = response.json()
        
        print(f"\n✓ Batch Predictions Generated Successfully\n")
        print(f"  Total Predictions: {result['count']}")
        print(f"  Timestamp:         {result['timestamp']}")
        print(f"\n  Results:")
        for i, pred in enumerate(result['predictions'], 1):
            print(f"    Patient {i}: {pred['label']} ({pred['probability']:.1%} probability)")
        
        return True
    except Exception as e:
        print(f"\n✗ Batch prediction failed: {str(e)}")
        return False


def test_partial_data():
    """Test prediction with complete data from actual patient example"""
    print_header("TEST 6: Complete Patient Data (Real-World Example)")
    
    # Use a complete patient record - all fields filled
    complete_patient = {
        "cases_disease_type": "Epithelial Neoplasms",
        "cases_primary_site": "Breast",
        "demographic_gender": "female",
        "demographic_race": "white",
        "demographic_ethnicity": "not hispanic or latino",
        "diagnoses_age_at_diagnosis": 20075,
        "diagnoses_primary_diagnosis": "Invasive Lobular Carcinoma",
        "diagnoses_primary_disease": "breast_cancer",
        "diagnoses_last_known_disease_status": "tumor_free",
        "diagnoses_progression_or_recurrence": "no",
        "diagnoses_tumor_grade": "G2",
        "diagnoses_tumor_burden": "medium",
        "diagnoses_morphology": "8520/3",
        "diagnoses_laterality": "Right",
        "diagnoses_metastasis_at_diagnosis": "m0",
        "diagnoses_days_to_diagnosis": 0,
        "diagnoses_days_to_recurrence": 1825,
        "treatments_treatment_type": "Surgery",
        "treatments_treatment_outcome": "Complete Response",
        "treatments_treatment_intent_type": "curative",
        "treatments_days_to_treatment_start": 15,
        "treatments_days_to_treatment_end": 30,
        "demographic_education_level": "college",
        "demographic_marital_status": "married",
        "demographic_occupation_duration_years": 25,
        "demographic_country_of_residence_at_enrollment": "United States",
        "demographic_population_group": "not_reported",
        "exposures_smoking_frequency": "never",
        "exposures_tobacco_smoking_status": "Never Smoker",
        "exposures_pack_years_smoked": 0,
        "exposures_years_smoked": 0,
        "exposures_cigarettes_per_day": 0,
        "exposures_asbestos_exposure": "no",
        "exposures_radon_exposure": "no",
        "exposures_environmental_tobacco_smoke_exposure": "no",
        "exposures_alcohol_drinks_per_day": 0,
        "exposures_alcohol_intensity": "never",
        "exposures_occupation_duration_years": 25,
        "exposures_occupation_type": "professional",
        "follow_ups_imaging_result": "negative",
        "follow_ups_imaging_result_1": "negative",
        "pathology_details_tumor_burden": "low",
        "pathology_details_greatest_tumor_dimension": 2.0,
        "pathology_details_margin_status": "negative",
        "pathology_details_lymph_node_involvement": "no",
        "pathology_details_lymph_nodes_positive": 0,
        "pathology_details_lymph_nodes_removed": 8,
        "pathology_details_lymphatic_invasion_present": "no",
        "pathology_details_perineural_invasion_present": "no",
        "pathology_details_vascular_invasion_present": "no",
        "pathology_details_residual_tumor": "r0",
        "pathology_details_necrosis_percent": 3,
        "pathology_details_morphologic_architectural_pattern": "lobular",
        "pathology_details_circumferential_resection_margin": "negative",
        "pathology_details_epithelioid_cell_percent": 95,
        "pathology_details_spindle_cell_percent": 5
    }
    
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=complete_patient,
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"\n✗ Request failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
        
        result = response.json()
        print_result(result)
        print(f"\n✓ Successfully handled complete patient data")
        
        return True
    except Exception as e:
        print(f"\n✗ Prediction failed: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("  Cancer Progression Prediction API - Test Suite")
    print("=" * 80)
    print(f"\nAPI URL: {API_URL}\n")
    
    tests = [
        ("Health Check", test_health_check),
        ("Low Risk Prediction", test_low_risk_prediction),
        ("High Risk Prediction", test_high_risk_prediction),
        ("Medium Risk Prediction", test_medium_risk_prediction),
        ("Batch Prediction", test_batch_prediction),
        ("Missing Fields", test_partial_data),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            results.append((name, test_func()))
        except Exception as e:
            print(f"\nUnexpected error in {name}: {str(e)}")
            results.append((name, False))
    
    # Print summary
    print("\n" + "=" * 80)
    print("  TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nResults: {passed}/{total} tests passed\n")
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")
    
    if passed < total:
        print(f"\n{'='*80}")
        print(f"⚠ {total - passed} test(s) failed. Check logs above.")
        print(f"{'='*80}\n")
        return 1
    else:
        print(f"\n{'='*80}")
        print(f"✓ All {total} tests passed successfully!")
        print(f"{'='*80}\n")
        return 0


if __name__ == "__main__":
    exit(main())
