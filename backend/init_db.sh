#!/bin/bash

# Database Initialization Script for Todo App
# This script initializes the database schema with users and tasks tables

echo "=================================="
echo "Todo App Database Initialization"
echo "=================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found!"
    echo "Please create .env file with DATABASE_URL configured"
    exit 1
fi

# Source environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "ERROR: DATABASE_URL not set in .env file"
    exit 1
fi

echo "Database URL: ${DATABASE_URL:0:30}..."
echo ""

# Run database initialization
echo "Initializing database tables..."
python init_db.py

echo ""
echo "=================================="
echo "Initialization Complete!"
echo "=================================="
