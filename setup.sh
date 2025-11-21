#!/bin/bash
# Cancer Progression Prediction API - Quick Setup Script

echo ""
echo "=============================================================================="
echo "  Cancer Progression Prediction API - Setup & Test"
echo "=============================================================================="
echo ""

# Check Python
echo "[1/5] Checking Python installation..."
python --version || { echo "Python not found! Install Python 3.10+"; exit 1; }

# Install dependencies
echo ""
echo "[2/5] Installing dependencies..."
pip install -r requirements.txt -q || { echo "Installation failed!"; exit 1; }

# Verify model file
echo ""
echo "[3/5] Verifying model file..."
if [ -f "catboost_cancer_progression_model.cbm" ]; then
    echo "✓ Model file found"
else
    echo "✗ Model file not found: catboost_cancer_progression_model.cbm"
    exit 1
fi

# Start API
echo ""
echo "[4/5] Starting API server..."
echo ""
python main.py &
API_PID=$!

# Wait for server to start
sleep 3

# Test API
echo ""
echo "[5/5] Testing API..."
HEALTH=$(curl -s http://localhost:8000/health)

if echo "$HEALTH" | grep -q "healthy"; then
    echo "✓ API is running successfully!"
    echo ""
    echo "=============================================================================="
    echo "  API is ready!"
    echo "=============================================================================="
    echo ""
    echo "📍 API Base URL:      http://localhost:8000"
    echo "📚 API Documentation: http://localhost:8000/docs"
    echo "🧪 Run tests:         python test_api.py"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    
    # Wait for server to be stopped
    wait $API_PID
else
    echo "✗ API failed to start"
    kill $API_PID 2>/dev/null
    exit 1
fi
