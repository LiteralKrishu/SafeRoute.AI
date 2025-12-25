import streamlit as st
import traceback
from functools import wraps
import pandas as pd
import numpy as np
from datetime import datetime

class ErrorHandler:
    @staticmethod
    def handle_errors(func):
        """Decorator to handle errors gracefully"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                st.error(f"Error in {func.__name__}: {str(e)}")
                # Provide fallback based on function type
                return ErrorHandler._get_fallback_result(func.__name__)
        return wrapper
    
    @staticmethod
    def _get_fallback_result(operation_name):
        """Provide appropriate fallback results for different operations"""
        fallbacks = {
            'get_hazards': pd.DataFrame(),
            'generate_recommendations': [
                {
                    "title": "Fallback Recommendation",
                    "priority": "Medium",
                    "issue": "System temporarily unavailable",
                    "intervention": "Please try again shortly",
                    "references": "System fallback",
                    "impact": "N/A",
                    "estimated_cost": "N/A",
                    "timeline": "N/A",
                    "implementation_status": 0
                }
            ],
            'find_safe_route': {
                'origin': 'Unknown',
                'destination': 'Unknown', 
                'duration': 'N/A',
                'distance': 'N/A',
                'safety_score': 0,
                'avoided_hazards': ['System temporarily unavailable'],
                'alternative_routes': []
            },
            'cluster_hazards': pd.DataFrame(),
            'verify_hazard_image': {
                'verified': False,
                'detected_hazards': [],
                'matches_reported': False,
                'overall_confidence': 0
            }
        }
        return fallbacks.get(operation_name, None)

class DataValidator:
    @staticmethod
    def validate_hazard_data(hazard_data):
        """Validate hazard data integrity"""
        required_fields = ['id', 'hazard_type', 'lat', 'lon', 'severity']
        
        for field in required_fields:
            if field not in hazard_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate coordinates
        if not (-90 <= hazard_data['lat'] <= 90):
            raise ValueError(f"Invalid latitude: {hazard_data['lat']}")
        if not (-180 <= hazard_data['lon'] <= 180):
            raise ValueError(f"Invalid longitude: {hazard_data['lon']}")
        
        # Validate severity
        if not (1 <= hazard_data['severity'] <= 5):
            raise ValueError(f"Invalid severity: {hazard_data['severity']}")
        
        # Validate hazard type
        valid_hazard_types = ['Potholes', 'Flooding', 'Accidents', 'Road Closures', 
                             'Construction', 'Debris', 'Landslides', 'Traffic']
        if hazard_data['hazard_type'] not in valid_hazard_types:
            raise ValueError(f"Invalid hazard type: {hazard_data['hazard_type']}")
        
        return True
    
    @staticmethod
    def validate_user_input(username, password, email=None):
        """Validate user input for registration/login"""
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        
        if email and '@' not in email:
            raise ValueError("Invalid email format")
        
        # Check for SQL injection patterns
        sql_injection_patterns = [';', '--', '/*', '*/', 'xp_']
        for pattern in sql_injection_patterns:
            if pattern in username or pattern in password:
                raise ValueError("Invalid characters in input")
        
        return True
    
    @staticmethod
    def validate_route_parameters(start, end):
        """Validate route planning parameters"""
        if not start or not end:
            raise ValueError("Start and end locations are required")
        
        if len(start) < 2 or len(end) < 2:
            raise ValueError("Location names too short")
        
        return True
    
    @staticmethod
    def validate_image_file(image_file):
        """Validate uploaded image file"""
        if image_file is None:
            return True  # Image is optional
        
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png']
        max_size = 10 * 1024 * 1024  # 10MB
        
        if image_file.type not in allowed_types:
            raise ValueError(f"Invalid image type. Allowed: {', '.join(allowed_types)}")
        
        if image_file.size > max_size:
            raise ValueError(f"Image too large. Maximum size: {max_size//1024//1024}MB")
        
        return True

class PerformanceValidator:
    @staticmethod
    def validate_response_time(start_time, operation_name, max_time=5.0):
        """Validate that operation doesn't take too long"""
        import time
        end_time = time.time()
        duration = end_time - start_time
        
        if duration > max_time:
            st.warning(f"Operation {operation_name} took {duration:.2f}s (slow)")
            return False
        return True
    
    @staticmethod
    def validate_data_size(data, max_size_mb=50):
        """Validate that data isn't too large"""
        import sys
        size = sys.getsizeof(data) / 1024 / 1024  # Convert to MB
        
        if size > max_size_mb:
            raise ValueError(f"Data too large: {size:.2f}MB (max: {max_size_mb}MB)")
        return True
