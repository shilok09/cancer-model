@echo off
REM Cancer Progression Prediction API - Quick Setup Script for Windows

setlocal enabledelayedexpansion

echo.
echo ==============================================================================
echo   Cancer Progression Prediction API - Setup and Test
echo ==============================================================================
echo.

REM Check Python
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found! Install Python 3.10+
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do echo ✓ %%i

REM Install dependencies
echo.
echo [2/5] Installing dependencies...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo Installation failed!
    pause
    exit /b 1
)
echo ✓ Dependencies installed

REM Verify model file
echo.
echo [3/5] Verifying model file...
if exist "catboost_cancer_progression_model.cbm" (
    echo ✓ Model file found
) else (
    echo ✗ Model file not found: catboost_cancer_progression_model.cbm
    pause
    exit /b 1
)

REM Start API
echo.
echo [4/5] Starting API server...
echo.
start "Cancer Progression API" python main.py

REM Wait for server to start
timeout /t 3 /nobreak >nul

REM Test API
echo.
echo [5/5] Testing API...

for /f "delims=" %%A in ('curl -s http://localhost:8000/health') do set response=%%A

if "%response%"=="" (
    echo ✗ Failed to connect to API
    pause
    exit /b 1
)

echo ✓ API is running successfully!
echo.
echo ==============================================================================
echo   API is ready!
echo ==============================================================================
echo.
echo.
echo 📍 API Base URL:      http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/docs
echo 🧪 Run tests:         python test_api.py
echo.
echo Keep this window open. Press Ctrl+C to stop.
echo.
pause
