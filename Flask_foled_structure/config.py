import os

class Config:
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgresql:postgresql@localhost:5432/db')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost:5432/db_name'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Configuration
    SECRET_KEY = 'your-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = 900  # Access token expires in 15 minutes (900 seconds)
    JWT_REFRESH_TOKEN_EXPIRES = 2592000  # Refresh token expires in 30 days (2592000 seconds)
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_IDENTITY_CLAIM = "user_uid"  #default is sub

    """
    import secrets
    api_key = secrets.token_hex(32)  # 64-character (32 bytes) hex string
    print("Generated API Secret Key:", api_key)
    """