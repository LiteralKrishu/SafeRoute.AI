import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import streamlit as st
from datetime import datetime, timedelta

class HazardClustering:
    def __init__(self):
        self.scaler = StandardScaler()
    
    def cluster_hazards(self, hazards_df):
        \"\"\"Cluster hazards using DBSCAN for hotspot detection\"\"\"
        if len(hazards_df) < 5:
            return hazards_df.assign(cluster_id=-1)
        
        # Prepare features for clustering
        coords = hazards_df[['lat', 'lon']].values
        
        # Scale coordinates
        features = self.scaler.fit_transform(coords)
        
        # Apply DBSCAN clustering
        clustering = DBSCAN(eps=0.02, min_samples=3).fit(features)
        
        hazards_df = hazards_df.copy()
        hazards_df['cluster_id'] = clustering.labels_
        hazards_df['is_hotspot'] = hazards_df['cluster_id'] != -1
        
        return hazards_df
    
    def predict_risk_zones(self, hazards_df, weather_data=None):
        \"\"\"Predict high-risk zones based on historical patterns\"\"\"
        # Calculate hazard density
        hazards_df['risk_score'] = self._calculate_risk_score(hazards_df)
        
        # Identify emerging clusters
        recent_hazards = hazards_df[
            pd.to_datetime(hazards_df['timestamp']) > 
            (datetime.now() - timedelta(hours=6))
        ]
        
        if len(recent_hazards) > 0:
            recent_clusters = self.cluster_hazards(recent_hazards)
            emerging_hotspots = recent_clusters[recent_clusters['is_hotspot']]
            
            # Boost risk score for emerging hotspots
            for cluster_id in emerging_hotspots['cluster_id'].unique():
                cluster_mask = hazards_df['cluster_id'] == cluster_id
                hazards_df.loc[cluster_mask, 'risk_score'] *= 1.5
        
        return hazards_df
    
    def _calculate_risk_score(self, hazards_df):
        \"\"\"Calculate comprehensive risk score\"\"\"
        base_score = hazards_df['severity'] * 20
        confidence_boost = hazards_df['confidence'] / 100 * 10
        cluster_boost = np.where(hazards_df['is_hotspot'], 30, 0)
        
        return base_score + confidence_boost + cluster_boost
