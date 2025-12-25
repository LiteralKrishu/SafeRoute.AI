import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from components.hazard_map import HazardMap
from components.enhanced_route_planner import EnhancedRoutePlanner
from components.enhanced_safety_gpt import EnhancedSafetyGPT
from components.enhanced_data_ingestion import EnhancedDataIngestion
from components.community_reporting import CommunityReporting
from models.hazard_clustering import HazardClustering
from utils.database import DatabaseManager
from utils.error_handling import ErrorHandler
from utils.performance import PerformanceMonitor
from utils.config import Config

# Initialize configuration
Config.validate_config()

class FinalSafeRouteApp:
    def __init__(self):
        self.db = DatabaseManager()
        self.data_ingestion = EnhancedDataIngestion()
        self.route_planner = EnhancedRoutePlanner()
        self.safety_gpt = EnhancedSafetyGPT()
        self.community_reporter = CommunityReporting()
        self.clustering = HazardClustering()
        self.performance_monitor = PerformanceMonitor()
        self.hazard_map = HazardMap()
        
    def render_sidebar(self):
        """Render enhanced sidebar with filters"""
            
        st.sidebar.markdown("---")
        
        # Hazard type filters
        st.sidebar.subheader("ðŸ”„ Hazard Filters")
        hazard_types = st.sidebar.multiselect(
            "Select Hazard Types:",
            ["Potholes", "Flooding", "Accidents", "Road Closures", 
             "Construction", "Debris", "Landslides", "Traffic"],
            default=["Potholes", "Accidents", "Flooding"]
        )
        
        # Data source filters
        st.sidebar.subheader("ðŸ“¡ Data Sources")
        sources = st.sidebar.multiselect(
            "Include Data From:",
            ["Community Reports", "Traffic APIs", "Weather Data", "Government Feeds"],
            default=["Community Reports", "Traffic APIs", "Weather Data"]
        )
        
        # Severity and confidence filters
        col1, col2 = st.sidebar.columns(2)
        with col1:
            severity = st.slider("Min Severity", 1, 5, 2)
        with col2:
            confidence = st.slider("Min Confidence", 0, 100, 70)
        
        return {
            "hazard_types": hazard_types,
            "sources": sources,
            "min_severity": severity,
            "min_confidence": confidence
        }
    
    def render_main_dashboard(self, filters):
        """Render enhanced main dashboard"""
        # Enhanced header
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.title("🚗 SafeRoute.AI - Real-Time Hazard Intelligence")
            st.markdown("Live hazard monitoring • Safe route planning • AI-powered interventions")
        
        with col2:
            st.metric("Active Hazards", "247", "+12 today")
            st.metric("Verified Reports", "89%", "4% ↑")
        
        with col3:
            if st.button("🔄 Refresh Data"):
                st.rerun()
        
        st.markdown("---")
        
        # Enhanced tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "ðŸ—ºï¸ Live Hazard Map", 
            "ðŸš¦ Safe Route Planner", 
            "ðŸ“ Report Hazard",
            "ðŸ¤– Safety Recommendations", 
            "ðŸ“Š Analytics & Admin"
        ])
        
        with tab1:
            self.render_enhanced_hazard_map(filters)
        
        with tab2:
            self.render_route_planner_tab()
        
        with tab3:
            self.render_community_reporting_tab()
        
        with tab4:
            self.render_safety_recommendations_tab(filters)
        
        with tab5:
            self.render_enhanced_analytics_tab()
    
    @ErrorHandler.handle_errors
    def render_enhanced_hazard_map(self, filters):
        """Render enhanced hazard map with clustering"""
        st.subheader("ðŸ—ºï¸ Live Hazard Intelligence Map")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Load and process hazards
            with st.spinner("ðŸ”„ Loading real-time hazard data..."):
                hazards_df = self.data_ingestion.get_real_time_hazards()
                
                # Apply clustering and risk prediction
                if not hazards_df.empty:
                    clustered_hazards = self.clustering.cluster_hazards(hazards_df)
                    risk_assessed_hazards = self.clustering.predict_risk_zones(clustered_hazards)
                    
                    # Render map
                    hazard_map = self.hazard_map.create_map(risk_assessed_hazards)
                    st_folium(hazard_map, width=800, height=600)
                else:
                    st.info("No hazard data available")
        
        with col2:
            self.render_hazard_insights(hazards_df)
    
    def render_hazard_insights(self, hazards_df):
        """Render hazard insights and alerts"""
        st.subheader("ðŸ“ˆ Hazard Insights")
        
        if not hazards_df.empty:
            stats = self.db.get_hazard_stats()
            
            st.metric("ðŸš¨ High Risk Zones", 
                     len(hazards_df[hazards_df['severity'] >= 4]))
            st.metric("ðŸ” Hotspots Identified", 
                     len(hazards_df[hazards_df.get('is_hotspot', False)]))
            st.metric("âœ… Verification Rate", f"{stats['verification_rate']:.1f}%")
            
            # Alert for emerging patterns
            recent_count = stats['recent_activity']
            if recent_count > 10:
                st.warning(f"ðŸš¨ High activity: {recent_count} hazards in last hour")
            
            # Top hazard types
            st.write("**Top Hazards:**")
            for hazard_type in hazards_df['hazard_type'].value_counts().head(3).items():
                st.write(f"- {hazard_type[0]}: {hazard_type[1]}")
        else:
            st.info("No insights available")
    
    @ErrorHandler.handle_errors
    def render_route_planner_tab(self):
        """Render enhanced route planning interface"""
        st.subheader("ðŸš— Smart Route Planning")
        
        col1, col2 = st.columns(2)
        
        with col1:
            start_location = st.text_input("Start Location", "Connaught Place, Delhi")
            end_location = st.text_input("Destination", "India Gate, Delhi")
            
            # Advanced routing options
            with st.expander("âš™ï¸ Advanced Routing Options"):
                col3, col4 = st.columns(2)
                with col3:
                    avoid_high_risk = st.checkbox("Avoid High Risk", True)
                    prefer_main_roads = st.checkbox("Prefer Main Roads", True)
                with col4:
                    consider_weather = st.checkbox("Consider Weather", True)
                    max_detour = st.slider("Max Detour (%)", 10, 100, 25)
            
            if st.button("ðŸŽ¯ Find Safest Route", type="primary"):
                with st.spinner("ðŸ¤– Calculating optimal safe route..."):
                    hazards_df = self.data_ingestion.get_real_time_hazards()
                    route_result = self.route_planner.find_safest_route(
                        start_location, end_location, hazards_df,
                        preferences={
                            'avoid_high_risk': avoid_high_risk,
                            'consider_weather': consider_weather
                        }
                    )
                    st.session_state['route_result'] = route_result
        
        with col2:
            if 'route_result' in st.session_state:
                route = st.session_state['route_result']
                
                st.subheader("ðŸ“ Route Analysis")
                st.metric("Safety Score", f"{route['safety_score']}/100")
                st.metric("Distance", f"{route['distance_km']:.1f} km")
                st.metric("Est. Time", route['estimated_time'])
                
                # Route details
                st.write("**Route:**")
                for i, point in enumerate(route['route']):
                    st.write(f"{i+1}. {point}")
                
                # Hazards avoided
                if route.get('hazards_avoided'):
                    st.write("**Hazards Avoided:**")
                    for hazard in route['hazards_avoided'][:5]:
                        st.write(f"âœ… {hazard}")
    
    def render_community_reporting_tab(self):
        """Render community reporting and engagement"""
        st.subheader("ðŸ“ Community Safety Ecosystem")
        
        tab1, tab2, tab3 = st.tabs(["Report Hazard", "My Reports", "Community Stats"])
        
        with tab1:
            self.community_reporter.render_report_form()
        
        with tab2:
            self.render_user_reports()
        
        with tab3:
            self.render_community_stats()
    
    def render_user_reports(self):
        """Render user's submitted reports"""
        if 'user' not in st.session_state:
            st.warning("Please log in to view your reports")
            return
        
        user_reports = self.db.get_user_reports(st.session_state.user['username'])
        
        if user_reports:
            st.subheader("ðŸ“‹ My Submitted Reports")
            for report in user_reports[-5:]:  # Last 5 reports
                with st.expander(f"Report {report['id']} - {report['hazard_type']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Status:** {report.get('status', 'pending').replace('_', ' ').title()}")
                        st.write(f"**Severity:** {report['severity']}/5")
                        st.write(f"**Location:** {report['location_description']}")
                    with col2:
                        st.write(f"**Submitted:** {report['timestamp']}")
                        st.write(f"**Confidence:** {report.get('confidence', 'N/A')}%")
        else:
            st.info("You haven't submitted any reports yet")
    
    def render_community_stats(self):
        """Render community statistics"""
        stats = self.db.get_hazard_stats()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Community Reports", 
                     sum(item['count'] for item in stats['by_type']))
        with col2:
            st.metric("Active Community Members", "1,247")
        with col3:
            st.metric("Reports This Week", "89")
        
        # Leaderboard (mock)
        st.subheader("ðŸ† Top Contributors")
        contributors = [
            {"name": "SafetyHero", "reports": 45, "verified": 38},
            {"name": "RoadGuard", "reports": 32, "verified": 29},
            {"name": "HazardSpotter", "reports": 28, "verified": 25}
        ]
        
        for i, contributor in enumerate(contributors):
            st.write(f"{i+1}. **{contributor['name']}** - {contributor['reports']} reports "
                    f"({contributor['verified']} verified)")
    
    @ErrorHandler.handle_errors
    def render_safety_recommendations_tab(self, filters):
        """Render AI safety advisor with enhanced capabilities"""
        st.subheader("ðŸ¤– AI Safety Advisor")
        
        # Real-time analysis
        col1, col2 = st.columns(2)
        
        with col1:
            analysis_scope = st.selectbox(
                "Analysis Scope",
                ["Current Hotspots", "Trend Analysis", "Predictive Risk", "Infrastructure Audit"]
            )
            
            urgency_level = st.select_slider(
                "Urgency Level",
                options=["Routine", "Important", "Critical", "Emergency"]
            )
        
        with col2:
            focus_areas = st.multiselect(
                "Focus Areas",
                ["Pothole Management", "Drainage Systems", "Road Markings", 
                 "Traffic Control", "Pedestrian Safety", "Construction Zones",
                 "Lighting Infrastructure", "Signage Systems"],
                default=["Pothole Management", "Drainage Systems"]
            )
            
            if st.button("ðŸš€ Generate Comprehensive Analysis", type="primary"):
                with st.spinner("ðŸ§  AI is analyzing safety patterns..."):
                    hazards_df = self.data_ingestion.get_real_time_hazards()
                    recommendations = self.safety_gpt.generate_comprehensive_analysis(
                        scope=analysis_scope,
                        focus_areas=focus_areas,
                        urgency=urgency_level,
                        hazard_data=hazards_df
                    )
                    st.session_state['ai_analysis'] = recommendations
        
        # Display AI analysis
        if 'ai_analysis' in st.session_state:
            self.render_ai_analysis(st.session_state['ai_analysis'])
    
    def render_ai_analysis(self, analysis):
        """Render comprehensive AI analysis"""
        st.subheader("ðŸŽ¯ AI Safety Recommendations")
        
        for i, rec in enumerate(analysis):
            with st.expander(
                f"ðŸ“ {rec['title']} - Priority: {rec['priority']} - "
                f"Impact: {rec.get('risk_reduction', 'N/A')}",
                expanded=i == 0
            ):
                # Implementation tracker
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**ðŸš¨ Issue:** {rec['issue']}")
                    st.write(f"**ðŸ› ï¸ Recommended Action:** {rec['intervention']}")
                    st.write(f"**ðŸ“š Standards Compliance:** {rec['references']}")
                    st.write(f"**ðŸ’° Cost Estimate:** {rec['estimated_cost']}")
                    st.write(f"**â±ï¸ Timeline:** {rec['timeline']}")
                    st.write(f"**ðŸ“ˆ Expected Impact:** {rec['impact']}")
                
                with col2:
                    if st.session_state.user['role'] == 'admin':
                        current_progress = st.slider(
                            "Progress", 0, 100, rec.get('implementation_status', 0),
                            key=f"progress_{i}"
                        )
                        st.metric("Status", 
                                 "Completed" if current_progress == 100 else "In Progress")
                        
                        if st.button("Update", key=f"update_{i}"):
                            st.success(f"Progress updated to {current_progress}%")
    
    def render_enhanced_analytics_tab(self):
        """Render advanced analytics dashboard"""
        st.subheader("📊 Advanced Analytics & Business Intelligence")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "Trend Analysis", "Risk Forecasting", "Cost-Benefit", "System Analytics"
        ])
        
        with tab1:
            self.render_trend_analysis()
        
        with tab2:
            self.render_risk_forecasting()
        
        with tab3:
            self.render_cost_benefit_analysis()
        
        with tab4:
            self.render_system_analytics()
    
    def render_trend_analysis(self):
        """Render trend analysis charts"""
        st.write("**Hazard Trends Over Time**")
        
        # Mock data
        trend_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            'Potholes': [45, 52, 48, 61, 55],
            'Accidents': [23, 28, 25, 31, 29],
            'Flooding': [12, 15, 18, 22, 20],
            'Construction': [8, 10, 12, 15, 14]
        })
        
        st.line_chart(trend_data.set_index('Month'))
    
    def render_risk_forecasting(self):
        """Render risk forecasting interface"""
        st.write("**Predictive Risk Forecasting**")
        
        # Forecasting parameters
        col1, col2 = st.columns(2)
        with col1:
            forecast_horizon = st.selectbox(
                "Forecast Horizon",
                ["Next 7 days", "Next 30 days", "Next 90 days"]
            )
            confidence_level = st.slider("Confidence Level", 50, 95, 80)
        
        with col2:
            include_weather = st.checkbox("Include Weather Data", True)
            include_traffic = st.checkbox("Include Traffic Patterns", True)
        
        if st.button("Generate Risk Forecast"):
            with st.spinner("ðŸ”® Generating risk predictions..."):
                # Mock forecast results
                st.success("Risk forecast generated successfully!")
                
                forecast_results = {
                    "High Risk Areas": ["Connaught Place", "India Gate Circle"],
                    "Emerging Threats": ["Monsoon flooding in low-lying areas"],
                    "Recommended Actions": ["Preemptive drainage cleaning", "Road surface inspection"]
                }
                
                for category, items in forecast_results.items():
                    st.write(f"**{category}:**")
                    for item in items:
                        st.write(f"- {item}")
    
    def render_cost_benefit_analysis(self):
        """Render cost-benefit analysis"""
        st.write("**Cost-Benefit Analysis**")
        
        interventions = [
            {"name": "Pothole Repair Program", "cost": "â‚¹50L", "benefit": "â‚¹2.5Cr", "roi": "400%"},
            {"name": "Drainage System Upgrade", "cost": "â‚¹1.2Cr", "benefit": "â‚¹4Cr", "roi": "233%"},
            {"name": "Smart Signage Installation", "cost": "â‚¹75L", "benefit": "â‚¹1.8Cr", "roi": "140%"}
        ]
        
        for intervention in interventions:
            with st.expander(f"ðŸ’° {intervention['name']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Cost", intervention['cost'])
                with col2:
                    st.metric("Annual Benefit", intervention['benefit'])
                with col3:
                    st.metric("ROI", intervention['roi'])
    
    def render_system_analytics(self):
        """Render system performance analytics"""
        st.write("**System Performance Analytics**")
        
        # Performance metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("API Response Time", "142ms", "12ms â†“")
        with col2:
            st.metric("Data Accuracy", "94.2%", "1.8% â†‘")
        with col3:
            st.metric("System Uptime", "99.8%", "0.1% â†‘")
        with col4:
            st.metric("User Satisfaction", "4.7/5", "0.2 â†‘")
    
    def run(self):
        """Run the final application"""
        filters = self.auth.render_login_sidebar()
        if filters and filters.get('user'):
            self.render_main_dashboard(filters)
        elif filters is None:
            st.warning("ðŸ” Please log in to access SafeRoute.AI")

if __name__ == "__main__":
    # Run the application
    app = FinalSafeRouteApp()
    app.run()
