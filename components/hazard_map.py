import folium
import pandas as pd
from folium.plugins import MarkerCluster, HeatMap
import streamlit as st

class HazardMap:
    def __init__(self):
        self.default_location = [28.6139, 77.2090]  # Delhi coordinates
        self.zoom_level = 10
    
    def get_hazard_icon(self, hazard_type, severity):
        """Get appropriate icon and color for hazard type"""
        color_map = {
            1: 'green',   # Low
            2: 'orange',  # Medium
            3: 'red',     # High
            4: 'darkred', # Critical
            5: 'black'    # Extreme
        }
        
        icon_map = {
            'Potholes': 'info-sign',
            'Flooding': 'tint',
            'Accidents': 'flash',
            'Road Closures': 'remove-sign',
            'Construction': 'wrench',
            'Debris': 'tree-deciduous',
            'Landslides': 'certificate',
            'Traffic': 'road'
        }
        
        return icon_map.get(hazard_type, 'info-sign'), color_map.get(severity, 'blue')
    
    def create_map(self, hazards_df):
        """Create interactive Folium map with hazards"""
        # Create base map
        m = folium.Map(
            location=self.default_location,
            zoom_start=self.zoom_level,
            tiles='OpenStreetMap'
        )
        
        # Create marker cluster
        marker_cluster = MarkerCluster().add_to(m)
        
        # Add hazards to map
        for _, hazard in hazards_df.iterrows():
            icon_type, color = self.get_hazard_icon(hazard['hazard_type'], hazard['severity'])
            
            # Create popup content
            popup_content = f\"\"\"
            <div style="width: 200px;">
                <h4>ðŸš¨ {hazard['hazard_type']}</h4>
                <p><strong>Severity:</strong> {hazard['severity']}/5</p>
                <p><strong>Confidence:</strong> {hazard['confidence']}%</p>
                <p><strong>Location:</strong> {hazard['location']}</p>
                <p><strong>Reported:</strong> {hazard['timestamp']}</p>
                <p><strong>Description:</strong> {hazard['description']}</p>
            </div>
            \"\"\"
            
            # Add marker to cluster
            folium.Marker(
                location=[hazard['lat'], hazard['lon']],
                popup=folium.Popup(popup_content, max_width=300),
                tooltip=f"{hazard['hazard_type']} (Severity: {hazard['severity']})",
                icon=folium.Icon(
                    color=color,
                    icon=icon_type,
                    prefix='glyphicon'
                )
            ).add_to(marker_cluster)
        
        # Add heatmap layer for hazard density
        heat_data = [[row['lat'], row['lon'], row['severity']] for _, row in hazards_df.iterrows()]
        if heat_data:
            HeatMap(heat_data, name="Hazard Density").add_to(m)
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        return m
