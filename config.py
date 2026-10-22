import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    TESTING = os.environ.get('TESTING', 'False').lower() == 'true'
    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY and not TESTING:
        raise ValueError("No SECRET_KEY set for Flask application. Set SECRET_KEY environment variable.")
    elif not SECRET_KEY:
        # Use a default key for testing only
        SECRET_KEY = 'test-secret-key-do-not-use-in-production'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Twilio Configuration
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
    
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER]) and not TESTING:
        raise ValueError("Missing Twilio configuration. Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER environment variables.")
    elif not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER]):
        # Use default values for testing only
        TWILIO_ACCOUNT_SID = 'test-sid'
        TWILIO_AUTH_TOKEN = 'test-token'
        TWILIO_PHONE_NUMBER = '+15555555555'