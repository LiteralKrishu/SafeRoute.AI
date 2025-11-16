import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    MAPBOX_ACCESS_TOKEN = os.getenv('MAPBOX_ACCESS_TOKEN', 'pk.eyJ1IjoiZXhhbXBsZSIsImEiOiJjbGV4YW1wbGUifQ.dummy')
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')
    
    # API Endpoints
    MAPBOX_BASE_URL = "https://api.mapbox.com"
    OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5"
    
    # App Settings
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    CACHE_TIMEOUT = int(os.getenv('CACHE_TIMEOUT', '300'))
    HAZARD_UPDATE_INTERVAL = int(os.getenv('HAZARD_UPDATE_INTERVAL', '300'))
    
    # Model Paths
    YOLO_MODEL_PATH = os.getenv('YOLO_MODEL_PATH', 'models/yolov8_road_hazards.pt')
    
    @staticmethod
    def validate_config():
        """Validate that required API keys are present"""
        missing_keys = []
        if not Config.OPENAI_API_KEY:
            missing_keys.append("OPENAI_API_KEY")
        if not Config.MAPBOX_ACCESS_TOKEN:
            missing_keys.append("MAPBOX_ACCESS_TOKEN")
        
        if missing_keys and not Config.DEBUG:
            st.error(f"Missing required API keys: {', '.join(missing_keys)}")
            st.stop()
        elif missing_keys:
            st.warning(f"Demo mode: Missing API keys - {', '.join(missing_keys)}")
