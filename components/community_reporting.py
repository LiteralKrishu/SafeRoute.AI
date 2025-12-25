import streamlit as st
from datetime import datetime
import json
import os
import random

class CommunityReporting:
    def __init__(self):
        self.reports_file = "data/community_reports.json"
        self._ensure_reports_file()
    
    def _ensure_reports_file(self):
        """Create reports file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.reports_file), exist_ok=True)
        if not os.path.exists(self.reports_file):
            with open(self.reports_file, 'w') as f:
                json.dump([], f)
    
    def render_report_form(self):
        """Render community hazard reporting form"""
        st.subheader("Report a Hazard")
        
        with st.form("hazard_report_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                hazard_type = st.selectbox(
                    "Hazard Type",
                    ["Potholes", "Flooding", "Accidents", "Road Closures", 
                     "Construction", "Debris", "Landslides", "Traffic", "Other"]
                )
                
                severity = st.slider("Severity Level", 1, 5, 3,
                                   help="1 = Low risk, 5 = Critical risk")
                
                location_description = st.text_input(
                    "Location Description",
                    placeholder="e.g., Near India Gate circle, opposite building..."
                )
            
            with col2:
                description = st.text_area(
                    "Detailed Description",
                    placeholder="Describe the hazard in detail...",
                    height=100
                )
                
                uploaded_image = st.file_uploader(
                    "Upload Photo (Optional)",
                    type=['jpg', 'jpeg', 'png'],
                    help="Upload a clear photo of the hazard for verification"
                )
            
            # Location options
            st.subheader("Location")
            location_method = st.radio(
                "Location Method:",
                ["Use Current Location", "Select on Map", "Enter Address"]
            )
            
            if location_method == "Enter Address":
                address = st.text_input("Enter Address")
                lat, lon = 28.6139, 77.2090  # Would geocode in real implementation
            else:
                lat, lon = 28.6139, 77.2090  # Default Delhi coordinates
            
            submitted = st.form_submit_button("Submit Report", type="primary")
            
            if submitted:
                report_data = self._submit_report(
                    hazard_type, severity, description, location_description,
                    lat, lon, uploaded_image
                )
                return report_data
        
        return None
    
    def _submit_report(self, hazard_type, severity, description, location_desc, lat, lon, image_file):
        """Process and store hazard report"""
        report_id = f"COMM_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        report_data = {
            "id": report_id,
            "hazard_type": hazard_type,
            "severity": severity,
            "description": description,
            "location_description": location_desc,
            "lat": lat,
            "lon": lon,
            "timestamp": datetime.now().isoformat(),
            "reporter": "community_user",
            "status": "pending_verification"
        }
        
        # Image verification if image provided
        if image_file is not None:
            # Simulate image verification
            verification_result = {
                'verified': True,
                'detected_hazards': [{'type': hazard_type, 'confidence': random.randint(70, 95)}],
                'matches_reported': True,
                'overall_confidence': random.randint(75, 90),
                'demo_mode': True
            }
            report_data["image_verification"] = verification_result
            report_data["has_image"] = True
            
            if verification_result.get('verified', False):
                report_data["confidence"] = verification_result.get('overall_confidence', 50)
                if verification_result.get('matches_reported', False):
                    report_data["status"] = "verified"
                    report_data["confidence"] = min(100, report_data["confidence"] + 20)
            else:
                report_data["confidence"] = 30
        else:
            report_data["has_image"] = False
            report_data["confidence"] = 40  # Lower confidence for text-only reports
        
        # Save report
        self._save_report(report_data)
        
        # Show confirmation
        st.success("Hazard report submitted successfully!")
        st.info(f"Report ID: {report_id} | Status: {report_data['status'].replace('_', ' ').title()}")

        return report_data
    
    def _save_report(self, report_data):
        """Save report to JSON file"""
        try:
            with open(self.reports_file, 'r') as f:
                reports = json.load(f)
            
            reports.append(report_data)
            
            with open(self.reports_file, 'w') as f:
                json.dump(reports, f, indent=2)
                
        except Exception as e:
            st.error(f"Failed to save report: {e}")
    
    def get_pending_reports(self):
        """Get reports pending verification"""
        try:
            with open(self.reports_file, 'r') as f:
                reports = json.load(f)
            
            return [r for r in reports if r.get('status') == 'pending_verification']
        except:
            return []
    
    def update_report_status(self, report_id, status, notes=""):
        """Update report verification status"""
        try:
            with open(self.reports_file, 'r') as f:
                reports = json.load(f)
            
            for report in reports:
                if report['id'] == report_id:
                    report['status'] = status
                    report['verified_at'] = datetime.now().isoformat()
                    report['verified_by'] = "admin_user"
                    if notes:
                        report['verification_notes'] = notes
                    break
            
            with open(self.reports_file, 'w') as f:
                json.dump(reports, f, indent=2)
                
            return True
        except Exception as e:
            st.error(f"Failed to update report: {e}")
            return False
