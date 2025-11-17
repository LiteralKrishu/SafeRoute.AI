import requests
import json
import streamlit as st
from utils.config import Config
import pandas as pd
from geopy.geocoders import Nominatim
import time

class RealMapboxIntegration:
    def __init__(self):
        self.access_token = Config.MAPBOX_ACCESS_TOKEN
        self.base_url = Config.MAPBOX_BASE_URL
        self.geolocator = Nominatim(user_agent="safetroute_ai")
    
    def geocode_address(self, address):
        """Convert address to coordinates using Mapbox Geocoding"""
        if Config.DEBUG and not self.access_token.startswith('pk.'):
            return self._mock_geocode(address)

        url = f"{self.base_url}/geocoding/v5/mapbox.places/{address}.json"
        params = {
            'access_token': self.access_token,
            'limit': 1
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data['features']:
                    coords = data['features'][0]['geometry']['coordinates']
                    return {'lon': coords[0], 'lat': coords[1], 'place_name': data['features'][0]['place_name']}
        except Exception as e:
            st.error(f"Geocoding error: {e}")

        return self._mock_geocode(address)
    
    def get_traffic_incidents(self, bbox):
        """Get real traffic incidents from Mapbox"""
        if Config.DEBUG:
            return self._mock_traffic_incidents(bbox)
        url = f"{self.base_url}/traffic/v5/incidents/{bbox}.json"
        params = {
            'access_token': self.access_token
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            st.error(f"Traffic API error: {e}")

        return self._mock_traffic_incidents(bbox)
    
    def get_route_with_hazards(self, start_coords, end_coords, avoid_hazards=True):
        """Get route considering hazards"""
        if Config.DEBUG:
            return self._mock_route(start_coords, end_coords)
        url = f"{self.base_url}/directions/v5/mapbox/driving/{start_coords['lon']},{start_coords['lat']};{end_coords['lon']},{end_coords['lat']}"
        params = {
            'access_token': self.access_token,
            'alternatives': 'true',
            'steps': 'true',
            'overview': 'full'
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            st.error(f"Routing API error: {e}")

        return self._mock_route(start_coords, end_coords)
    
    def _mock_geocode(self, address):
        """Mock geocoding for demo"""
        mock_locations = {
            'connaught place, delhi': {'lon': 77.2189, 'lat': 28.6315, 'place_name': 'Connaught Place, New Delhi'},
            'india gate, delhi': {'lon': 77.2295, 'lat': 28.6129, 'place_name': 'India Gate, New Delhi'},
            'rajpath, delhi': {'lon': 77.2290, 'lat': 28.6140, 'place_name': 'Rajpath, New Delhi'}
        }
        return mock_locations.get(address.lower(), {'lon': 77.2090, 'lat': 28.6139, 'place_name': address})
    
    def _mock_traffic_incidents(self, bbox):
        """Mock traffic incidents for demo"""
        return {
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {'type': 'Point', 'coordinates': [77.2189, 28.6315]},
                    'properties': {'incident_type': 'accident', 'description': 'Vehicle breakdown'}
                }
            ]
        }
    
    def _mock_route(self, start_coords, end_coords):
        """Mock route for demo"""
        return {
            'routes': [{
                'duration': 1800,
                'distance': 15000,
                'geometry': {'type': 'LineString', 'coordinates': []}
            }]
        }
