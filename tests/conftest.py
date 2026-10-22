"""
Pytest configuration for wisdom-lite tests
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set test environment variables before any imports
os.environ['TESTING'] = 'True'
os.environ['SECRET_KEY'] = 'test-secret-key'
os.environ['TWILIO_ACCOUNT_SID'] = 'test-sid'
os.environ['TWILIO_AUTH_TOKEN'] = 'test-token'
os.environ['TWILIO_PHONE_NUMBER'] = '+15555555555'
