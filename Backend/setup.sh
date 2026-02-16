#!/bin/bash

# Backend Quick Start Script
# This script sets up and runs the Django backend

echo "=================================="
echo "Backend Setup"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "Python 3 found: $(python3 --version)"
echo ""

# Navigate to backend directory
cd backend

# Install dependencies
echo "Installing dependencies..."
pip install -r ../requirements.txt

echo ""
echo "Setting up database..."

# Run migrations
python manage.py makemigrations
python manage.py migrate

echo ""
echo "Create a superuser account for admin access"
python manage.py createsuperuser

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "To start the server, run:"
echo "  cd backend"
echo "  python manage.py runserver"
echo ""
echo "API will be available at: http://localhost:8000/"
echo "Admin panel: http://localhost:8000/admin/"
echo ""
echo "See README.md for API documentation"
echo "=================================="