# Sample data file for SafeRoute.AI
# This file contains mock data for demonstration

SAMPLE_HAZARDS = [
    {
        'id': 'HR0001',
        'hazard_type': 'Potholes',
        'severity': 4,
        'confidence': 85,
        'lat': 28.6315,
        'lon': 77.2189,
        'location': 'Connaught Place',
        'description': 'Large pothole near metro station entrance',
        'source': 'Community Report',
        'verified': True
    },
    {
        'id': 'HR0002', 
        'hazard_type': 'Accidents',
        'severity': 5,
        'confidence': 90,
        'lat': 28.6129,
        'lon': 77.2295,
        'location': 'India Gate Circle',
        'description': 'Multi-vehicle collision, road blocked',
        'source': 'Traffic API',
        'verified': True
    }
]
