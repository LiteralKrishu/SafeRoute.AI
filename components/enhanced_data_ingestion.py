import requests
import pandas as pd
from datetime import datetime, timedelta
import random
import streamlit as st
from utils.config import Config
from utils.database import DatabaseManager

class EnhancedDataIngestion:
    def __init__(self):
        self.db = DatabaseManager()
        self.hazard_types = [
            'Potholes', 'Flooding', 'Accidents', 'Road Closures',
            'Construction', 'Debris', 'Landslides', 'Traffic'
        ]
        self.locations = [
            'Connaught Place', 'India Gate', 'Rajpath', 'Janpath', 
            'Barakhamba Road', 'Kasturba Gandhi Marg', 'Parliament Street',
            'Ashoka Road', 'Mandir Marg', 'Bangla Sahib Road'
        ]
    
    def get_real_time_hazards(self, bbox="77.2090,28.6139,77.2290,28.6339"):
        """Get real-time hazards from multiple sources"""
        hazards = []
        
        # Get from database first
        db_hazards = self.db.get_recent_hazards(hours=24)
        if not db_hazards.empty:
            hazards.extend(db_hazards.to_dict('records'))
        else:
            # Generate mock data if no database entries
            hazards.extend(self.generate_mock_hazards(30))
        
        # Add real API data (mock for now)
        traffic_incidents = self._get_traffic_incidents(bbox)
        hazards.extend(traffic_incidents)
        
        weather_hazards = self._get_weather_hazards(bbox)
        hazards.extend(weather_hazards)
        
        return pd.DataFrame(hazards)
    
    def generate_mock_hazards(self, count=50):
        """Generate mock hazard data for demonstration"""
        hazards = []
        
        for i in range(count):
            hazard_type = random.choice(self.hazard_types)
            severity = random.randint(1, 5)
            confidence = random.randint(60, 95)
            
            # Base coordinates around Delhi
            base_lat, base_lon = 28.6139, 77.2090
            lat = base_lat + random.uniform(-0.1, 0.1)
            lon = base_lon + random.uniform(-0.1, 0.1)
            
            hazard = {
                'id': f"HR{i:04d}",
                'hazard_type': hazard_type,
                'severity': severity,
                'confidence': confidence,
                'lat': lat,
                'lon': lon,
                'location': random.choice(self.locations),
                'timestamp': (datetime.now() - timedelta(hours=random.randint(0, 72))).strftime('%Y-%m-%d %H:%M'),
                'description': f"{hazard_type} reported in {random.choice(self.locations)} area",
                'source': random.choice(['User Report', 'Govt API', 'Traffic Cam', 'Weather Feed']),
                'verified': confidence > 70
            }
            hazards.append(hazard)
            
            # Save to database
            self.db.save_hazard(hazard)
        
        return hazards
    
    def _get_traffic_incidents(self, bbox):
        """Get traffic incidents (mock implementation)"""
        incidents = []
        for i in range(5):
            incidents.append({
                'id': f"TRAFFIC_{i}",
                'hazard_type': random.choice(['Accidents', 'Traffic', 'Road Closures']),
                'severity': random.randint(2, 4),
                'confidence': 85,
                'lat': 28.6139 + random.uniform(-0.05, 0.05),
                'lon': 77.2090 + random.uniform(-0.05, 0.05),
                'location': 'Road Incident',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'description': 'Traffic incident reported',
                'source': 'Traffic API',
                'verified': True
            })
        return incidents
    
    def _get_weather_hazards(self, bbox):
        """Get weather-related hazards (mock implementation)"""
        return [{
            'id': 'WEATHER_001',
            'hazard_type': 'Flooding',
            'severity': 3,
            'confidence': 75,
            'lat': 28.6250,
            'lon': 77.2150,
            'location': 'Connaught Place Area',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'description': 'Heavy rainfall causing waterlogging',
            'source': 'Weather API',
            'verified': True
        }]
