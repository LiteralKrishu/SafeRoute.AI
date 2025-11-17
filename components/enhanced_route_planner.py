import networkx as nx
import pandas as pd
import numpy as np
from geopy.distance import geodesic
import streamlit as st
import random
from utils.error_handling import DataValidator

class EnhancedRoutePlanner:
    def __init__(self):
        self.road_network = self._create_road_network()
    
    def _create_road_network(self):
        """Create a graph representing the road network"""
        G = nx.Graph()
        
        # Add major Delhi locations as nodes
        locations = {
            'Connaught Place': (28.6315, 77.2189),
            'India Gate': (28.6129, 77.2295),
            'Rajiv Chowk': (28.6326, 77.2197),
            'Kashmere Gate': (28.6660, 77.2285),
            'Nehru Place': (28.5480, 77.2522),
            'Hauz Khas': (28.5545, 77.1947)
        }
        
        for name, coords in locations.items():
            G.add_node(name, pos=coords)
        
        # Add edges with approximate distances
        edges = [
            ('Connaught Place', 'India Gate', 2.5),
            ('Connaught Place', 'Rajiv Chowk', 0.5),
            ('India Gate', 'Rajiv Chowk', 2.0),
            ('Connaught Place', 'Kashmere Gate', 4.0),
            ('Rajiv Chowk', 'Nehru Place', 8.0),
            ('Nehru Place', 'Hauz Khas', 3.0)
        ]
        
        for u, v, dist in edges:
            G.add_edge(u, v, weight=dist)
        
        return G
    
    def find_safest_route(self, start, end, hazards_df, preferences=None):
        """Find safest route considering hazards and preferences"""
        # Validate inputs
        DataValidator.validate_route_parameters(start, end)
        
        if preferences is None:
            preferences = {
                'avoid_high_risk': True,
                'minimize_exposure': True,
                'consider_weather': True
            }
        
        try:
            # Validate hazards data
            if not hazards_df.empty:
                required_hazard_cols = ['hazard_type', 'severity', 'lat', 'lon', 'confidence']
                missing_cols = [col for col in required_hazard_cols if col not in hazards_df.columns]
                if missing_cols:
                    st.warning(f"Missing hazard data columns: {missing_cols}")
            
            # For demo purposes, return mock route
            return self._mock_route(start, end, hazards_df)
                
        except Exception as e:
            st.error(f"Route planning error: {e}")
            return self._fallback_route(start, end)
    
    def _mock_route(self, start, end, hazards_df):
        """Mock route calculation for demo with validation"""
        # Validate start and end locations exist in network
        if start not in self.road_network.nodes:
            st.warning(f"Start location '{start}' not in network, using nearest known location")
            start = self._find_nearest_location(start)
        
        if end not in self.road_network.nodes:
            st.warning(f"End location '{end}' not in network, using nearest known location") 
            end = self._find_nearest_location(end)
        
        routes = [
            {
                'route': [start, 'Rajiv Chowk', end],
                'distance_km': 8.5,
                'safety_score': 85,
                'hazards_avoided': ['Major pothole cluster', 'Flooding area'],
                'estimated_time': '25 minutes',
                'details': 'Safest route avoiding high-risk zones',
                'hazard_exposure': 'Low'
            },
            {
                'route': [start, end],
                'distance_km': 6.2, 
                'safety_score': 65,
                'hazards_avoided': ['Minor traffic congestion'],
                'estimated_time': '18 minutes',
                'details': 'Fastest route with moderate safety',
                'hazard_exposure': 'Medium'
            },
            {
                'route': [start, 'Kashmere Gate', end],
                'distance_km': 10.1,
                'safety_score': 92,
                'hazards_avoided': ['All major hazards', 'Construction zones'],
                'estimated_time': '32 minutes',
                'details': 'Maximum safety with longer travel time',
                'hazard_exposure': 'Very Low'
            }
        ]
        
        # Select best route based on hazards and preferences
        high_risk_hazards = len(hazards_df[hazards_df['severity'] >= 4]) if not hazards_df.empty else 0
        
        if high_risk_hazards > 3:
            selected_route = routes[2]  # Safest route
        elif high_risk_hazards > 0:
            selected_route = routes[0]  # Balanced route
        else:
            selected_route = routes[1]  # Fastest route
        
        # Add hazard analysis
        selected_route['hazard_analysis'] = self._analyze_route_hazards(selected_route['route'], hazards_df)
        
        return selected_route
    
    def _find_nearest_location(self, location):
        """Find nearest known location in the network"""
        known_locations = list(self.road_network.nodes.keys())
        
        # Simple matching - in real implementation, use geocoding
        location_lower = location.lower()
        for known_loc in known_locations:
            if location_lower in known_loc.lower() or known_loc.lower() in location_lower:
                return known_loc
        
        # Default fallback
        return 'Connaught Place'
    
    def _analyze_route_hazards(self, route, hazards_df):
        """Analyze hazards along the route"""
        if hazards_df.empty:
            return {"total_hazards": 0, "high_risk_hazards": 0, "risk_level": "Low"}
        
        # Count hazards near route points (simplified)
        total_hazards = len(hazards_df)
        high_risk_hazards = len(hazards_df[hazards_df['severity'] >= 4])

        risk_level = "Low"
        if high_risk_hazards > 5:
            risk_level = "High"
        elif high_risk_hazards > 2:
            risk_level = "Medium"
        
        return {
            "total_hazards": total_hazards,
            "high_risk_hazards": high_risk_hazards,
            "risk_level": risk_level
        }
    
    def _fallback_route(self, start, end):
        """Provide fallback route when main algorithm fails"""
        return {
            'route': [start, end],
            'distance_km': 10.0,
            'safety_score': 50,
            'hazards_avoided': ['Fallback mode active'],
            'estimated_time': '25 minutes',
            'fallback': True,
            'hazard_exposure': 'Unknown',
            'hazard_analysis': {"total_hazards": 0, "high_risk_hazards": 0, "risk_level": "Unknown"}
        }
    
    def validate_route_result(self, route_result):
        """Validate that route result contains all required fields"""
        required_fields = ['route', 'distance_km', 'safety_score', 'estimated_time']
        
        for field in required_fields:
            if field not in route_result:
                raise ValueError(f"Missing required field in route result: {field}")
        
        if not isinstance(route_result['route'], list) or len(route_result['route']) < 2:
            raise ValueError("Invalid route format")
        
        if not (0 <= route_result['safety_score'] <= 100):
            raise ValueError("Safety score must be between 0 and 100")
        
        return True
