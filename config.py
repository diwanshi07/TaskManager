import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///task_manager.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-jwt-secret-key')  
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    PORT = int(os.getenv('PORT', 8009)) 
    JWT_EXPIRATION_TIME = int(os.getenv('JWT_EXPIRATION_TIME', 6))  
