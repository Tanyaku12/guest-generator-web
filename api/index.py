import sys
import os

# Add the project root directory to the python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask app instance
from api.generate import app

# Expose app for Vercel
# (Vercel's @vercel/python runtime automatically looks for the 'app' variable)
