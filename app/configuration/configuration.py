import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv(dotenv_path=".env")

# Read environment variables
class Settings:
    TITLE: str = "SCMXpertLite"
    DESCRIPTION: str = """SCMXpertLite Developed in FastAPI"""
    PROJECT_VERSION: str = "0.0.1"
    MONGODB_USER = os.getenv("mongodb_user")
    MONGODB_PASSWORD = os.getenv("mongodb_password")
    CLIENT = MongoClient(os.getenv("mongodbUri"))
    DB = CLIENT[os.getenv("db_name")]
    USERS_COLLECTION = DB[os.getenv("user_collection")]
    SHIPMENT_COLLECTION = DB[os.getenv("shipment_collection")]
    DEVICE_DATA_COLLECTION = DB[os.getenv("data_stream_collection")]
    SECRET_KEY: str = "ljzsjsyrkijohprxtpvdhnbokuvasnbc"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30 
    COOKIE_NAME = "access_token"
    HOST = (os.getenv("HOST"))
    PORT = (os.getenv("PORT")) 

SETTING = Settings()