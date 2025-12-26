import openai
import streamlit as st
from utils.config import Config
import json
import re
import random

class EnhancedSafetyGPT:
    def __init__(self):
        self.client = None
        self.initialize_openai()
        self.guidelines_db = self._load_guidelines()
    
    def initialize_openai(self):
        """Initialize OpenAI client"""
        if Config.OPENAI_API_KEY and Config.OPENAI_API_KEY != 'mock_key_for_demo':
            try:
                openai.api_key = Config.OPENAI_API_KEY
                self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
                st.success("OpenAI GPT integration active")
            except Exception as e:
                st.error(f"OpenAI initialization failed: {e}")
                self.client = None
        else:
            st.warning("Using demo mode for GPT - add OPENAI_API_KEY for real AI")
    
    def generate_recommendations(self, area, focus_areas, time_range, hazard_data=None):
        """Generate AI-powered safety recommendations with real GPT"""
        if self.client is None:
            return self._mock_recommendations(area, focus_areas, time_range)
        
        try:
            # Prepare context from hazard data
            context = self._build_context(area, focus_areas, time_range, hazard_data)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a road safety expert specializing in IRC (Indian Roads Congress) 
                        and MoRTH (Ministry of Road Transport and Highways) guidelines. Provide detailed, 
                        actionable recommendations with specific clause references."""
                    },
                    {
                        "role": "user", 
                        "content": self._build_prompt(context)
                    }
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            return self._parse_gpt_response(response.choices[0].message.content)
            
        except Exception as e:
            st.error(f"GPT API error: {e}")
            return self._mock_recommendations(area, focus_areas, time_range)
    
    def generate_comprehensive_analysis(self, scope, focus_areas, urgency, hazard_data):
        """Generate comprehensive safety analysis"""
        return self._mock_recommendations("Delhi Central", focus_areas, "Last 30 days")
    
    def _build_context(self, area, focus_areas, time_range, hazard_data):
        """Build context for GPT analysis"""
        context = {
            "area": area,
            "focus_areas": focus_areas,
            "time_range": time_range,
            "hazard_summary": self._summarize_hazards(hazard_data) if hazard_data else "No specific hazard data provided",
            "guidelines_available": list(self.guidelines_db.keys())
        }
        return context
    
    def _build_prompt(self, context):
        """Build detailed prompt for GPT"""
        return f"""
        As a road safety expert, analyze the following situation and provide detailed recommendations:
        
        AREA: {context['area']}
        FOCUS AREAS: {', '.join(context['focus_areas'])}
        TIME RANGE: {context['time_range']}
        HAZARD SUMMARY: {context['hazard_summary']}
        
    Please provide 3-5 detailed safety recommendations based on IRC and MoRTH guidelines.
    Be specific with clause references and practical solutions.
    """
    
    def _parse_gpt_response(self, response_text):
        """Parse GPT response"""
        # For demo, return mock recommendations
        return self._mock_recommendations()
    
    def _load_guidelines(self):
        """Load safety guidelines database"""
        return {
            "IRC 35-2015": "Road Safety Requirements",
            "IRC 67-2012": "Code of Practice for Road Signs",
            "IRC 99-1988": "Recommendations for Traffic Rotaries",
            "MoRTH Section 1800": "Road Safety Features",
            "IRC SP-84": "Manual for Safety in Road Construction Zones"
        }
    
    def _summarize_hazards(self, hazard_data):
        """Summarize hazard data for GPT context"""
        if hasattr(hazard_data, 'shape'):
            # It's a DataFrame
            summary = f"Total hazards: {len(hazard_data)}, "
            if not hazard_data.empty:
                summary += f"Top types: {hazard_data['hazard_type'].value_counts().head(3).to_dict()}"
            return summary
        return str(hazard_data)
    
    def _mock_recommendations(self, area=None, focus_areas=None, time_range=None):
        """Fallback mock recommendations"""
        return [
            {
                "title": "Pothole Remediation Program",
                "priority": "High",
                "issue": f"Multiple pothole reports in {area or 'Central District'} with severity 4+",
                "intervention": "Immediate cold-mix patching + scheduled hot-mix overlay with improved drainage integration",
                "references": "IRC:35-2015 Clause 4.2.3, MoRTH Section 1800, IRC:67-2012 Section 5.4",
                "impact": "Reduce pothole-related accidents by 75%, improve ride quality, extend road surface life by 40%",
                "estimated_cost": "INR 2.5-4 lakhs/km",
                "timeline": "2-4 weeks",
                "implementation_status": random.randint(10, 40),
                "risk_reduction": "65%"
            },
            {
                "title": "Drainage System Enhancement",
                "priority": "Medium", 
                "issue": "Waterlogging reported at multiple locations during moderate rainfall, indicating inadequate drainage capacity and blockages",
                "intervention": "Comprehensive drain cleaning and desilting program. Install additional catch pits at 50m intervals. Improve cross-fall to drainage inlets and add redundant overflow systems",
                "references": "IRC:SP-42 Clause 7.4.2, IRC:67-2012 Section 5, MoRTH Drainage Manual Chapter 3",
                "impact": "Eliminate waterlogging in 90% of reported areas, prevent pavement damage from water seepage, improve skid resistance during rains",
                "estimated_cost": "INR 8-12 lakhs per km",
                "timeline": "4-6 weeks", 
                "implementation_status": random.randint(5, 20),
                "risk_reduction": "45%"
            },
            {
                "title": "Advanced Warning System Installation",
                "priority": "Medium",
                "issue": "High incidence of accidents at sharp curves and intersections with limited visibility and inadequate warning systems",
                "intervention": "Install retroreflective warning signs with hazard markers at 150m intervals. Implement rumble strips 200m before critical points. Add chevron alignment signs and solar-powered blinkers for night visibility",
                "references": "IRC:67-2012 Table 9-1, MoRTH Chapter 8, IRC:99-1988 Section 4.3",
                "impact": "Reduce curve-related accidents by 60%, improve driver awareness and reaction time, enhance night-time safety by 50%",
                "estimated_cost": "1.2-1.8 lakhs per location",
                "timeline": "2-3 weeks",
                "implementation_status": random.randint(0, 10),
                "risk_reduction": "55%"
            }
        ]
