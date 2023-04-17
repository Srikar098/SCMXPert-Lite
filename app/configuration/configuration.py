import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

class Settings:
    TITLE: str = "SCMXpertLite"
    DESCRIPTION: str = """SCMXpertLite Developed in FastAPI"""
    PROJECT_VERSION: str = "0.0.1"
    MONGODB_USER = os.getenv("mongodb_user")
    MONGODB_PASSWORD = os.getenv("mongodb_password")
    CLIENT = MongoClient(os.getenv("mongodbUri"))
    DB = CLIENT['scmxpertlite']
    USERS_COLLECTION = DB['Users']
    SHIPMENT_COLLECTION = DB['Shipments']
    SECRET_KEY: str = "ljzsjsyrkijohprxtpvdhnbokuvasnbc"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30 
    COOKIE_NAME = "access_token"

SETTING = Settings()