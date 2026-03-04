#!/bin/bash
#
# Smart Thermal Security System - Startup Script
# This script installs dependencies and starts the Flask application
#

echo "============================================================"
echo "Smart Thermal Home Security & Emergency Alert System"
echo "Initialization Script"
echo "============================================================"
echo ""

# Change to application directory
cd "$(dirname "$0")"

# Check Python installation
echo "[1/4] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi
echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Install dependencies
echo "[2/4] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed successfully"
echo ""

# Initialize database
echo "[3/4] Initializing database..."
python3 -c "from app import init_db; init_db()"
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to initialize database"
    exit 1
fi
echo "✓ Database initialized"
echo ""

# Start Flask application
echo "[4/4] Starting Flask application..."
echo ""
echo "============================================================"
echo "Access the application at: http://localhost:5000"
echo "Default credentials: admin / admin123"
echo "============================================================"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
