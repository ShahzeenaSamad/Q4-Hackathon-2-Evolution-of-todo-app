"""
Initialize Database Tables
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from db import engine, init_db

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")
