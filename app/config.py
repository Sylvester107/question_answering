class BaseConfig:
    # Common configuration settings
    DEBUG = False
    SECRET_KEY = ''

class DevelopmentConfig(BaseConfig):
    # Development-specific settings
    DEBUG = True

class ProductionConfig(BaseConfig):
    # Production-specific settings
    DEBUG = False
    # Add Waitress-specific settings
    SERVER_NAME = '0.0.0.0:8000'  # Listen on all available network interfaces
    PREFERRED_URL_SCHEME = 'http'  # Use 'http' for production

class TestingConfig(BaseConfig):
    # Testing-specific settings
    TESTING = True
    # Add other testing settings as needed
