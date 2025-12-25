# SafeRoute.AI - Road Safety Intelligence Platform

![Road Safety](https://img.shields.io/badge/Road%20Safety-AI%20Powered-brightgreen)
![Open Source](https://img.shields.io/badge/Open--Source-Yes-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)

## 🎯 Project Overview

**SafeRoute.AI** is an open-source AI-powered road safety management and hazard intelligence platform. Built for comprehensive transportation safety under the mission **"Intelligent Route Planning for Safer Communities."**

The platform provides real-time transparency into road hazards and safety risks using machine learning to detect dangerous patterns and promote accountability in transportation infrastructure.

---

## 🚀 Features

### 🔍 Core Dashboard Features

- **📊 Real-Time Hazard Map**
  - Interactive Folium map with live hazard markers
  - Hazard clustering and hotspot detection
  - Heat map overlay for hazard density
  - Multiple tile providers and filtering options

- **🚨 AI Anomaly Detection**
  - Machine learning for suspicious hazard patterns
  - Isolation Forest algorithm for outlier detection
  - Interactive visualization with hover details

- **🏢 Vendor/Location Analysis**
  - Hotspot identification and risk zones
  - Hazard distribution analysis
  - Temporal trend patterns

- **⏱️ Safety & Efficiency Tracking**
  - Route optimization analysis
  - Processing time monitoring
  - Hazard response tracking

### 🎨 Design Features

- **Modern UI**: Clean, responsive design with Streamlit
- **Brand Consistency**: Professional color scheme and typography
- **Accessibility**: WCAG AA compliant with proper contrast ratios
- **Real-time Data**: Integration with multiple APIs and data sources

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Installation & Setup](#installation--setup)
3. [Configuration Files](#configuration-files)
4. [Features](#features)
5. [API Integration](#api-integration)
6. [Database Schema](#database-schema)
7. [Security](#security)
8. [Performance Monitoring](#performance-monitoring)
9. [Usage Guide](#usage-guide)
10. [Troubleshooting](#troubleshooting)

---

## Project Structure

```
SafeRoute-AI/
├── config/                          # Configuration files
│   ├── __init__.py                 # Package initialization
│   ├── app_config.py               # Application settings
│   ├── api_config.py               # API configurations
│   ├── database_config.py           # Database schema
│   ├── security_config.py           # Security policies
│   ├── performance_config.py        # Performance monitoring
│   └── logging_config.py            # Logging setup
│
├── utils/                           # Utility modules
│   ├── __init__.py
│   ├── config.py                    # Core configuration
│   ├── database.py                  # Database manager
│   ├── error_handling.py            # Error handling & validation
│   ├── performance.py               # Performance utilities
│   └── cache_manager.py             # Caching system
│
├── components/                      # UI/Feature components
│   ├── __init__.py
│   ├── hazard_map.py               # Interactive map
│   ├── enhanced_route_planner.py    # Route planning
│   ├── enhanced_safety_gpt.py       # AI recommendations
│   ├── enhanced_data_ingestion.py   # Data collection
│   ├── community_reporting.py       # User reporting
│   └── real_mapbox_integration.py   # Mapbox API
│
├── models/                          # ML/Data models
│   ├── __init__.py
│   ├── hazard_clustering.py        # DBSCAN clustering
│   └── image_verification.py       # Image analysis
│
├── data/                            # Data storage
│   ├── sample_data.py              # Sample data
│   ├── guidelines/                  # Safety guidelines
│   ├── uploads/                     # User uploads
│   ├── exports/                     # Exported data
│   └── safetroute.db               # SQLite database
│
├── logs/                            # Application logs
│   ├── safetroute.log              # Main log
│   └── errors.log                  # Error log
│
├── backups/                         # Database backups
│
├── app_final.py                     # Main application
├── setup_environment.py             # Environment setup
├── deploy_production.py             # Production deployment
├── run_app.bat                      # Windows runner script
├── requirements.txt                 # Python dependencies
├── .env                             # Environment variables
├── LICENSE                          # License file
└── README.md                        # This documentation
```

---

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Quick Start

1. **Clone or download the project**
```bash
# If using git
git clone <repository-url>
cd SafeRoute-AI

# Or simply extract the project folder
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Environment**
Create `.env` file with your API keys:
```env
OPENAI_API_KEY=your_openai_key_here
MAPBOX_ACCESS_TOKEN=pk.your_mapbox_token_here
WEATHER_API_KEY=your_weather_api_key_here
```

4. **Initialize Database**
```bash
python -c "from config.database_config import DatabaseConfig; DatabaseConfig.initialize_database()"
```

5. **Run the application**
```bash
streamlit run app_final.py
```

Open your browser and navigate to http://localhost:8501

### Automated Setup (Windows/PowerShell)

**Run the setup script**
```powershell
.\run_app.bat
```

This script will automatically:
- Check for Python installation
- Create a virtual environment
- Install all dependencies
- Launch the dashboard

---

## 📊 Data Sources

### Primary Sources
- Mapbox API - Real-time traffic and hazard data
- OpenAI GPT - Safety recommendations and analysis
- OpenWeatherMap - Weather conditions
- User community reports - Crowdsourced hazard data

### Sample Data
- Generated realistic road hazard scenarios
- Includes hazards from multiple categories (potholes, flooding, accidents)
- Temporal data for trend analysis

---

## 🏗️ Project Structure

```text
SafeRoute-AI/
├── config/                          # Configuration Package
│   ├── __init__.py                 # Package initialization
│   ├── app_config.py               # Application settings & feature flags
│   ├── api_config.py               # API endpoints & configurations
│   ├── database_config.py           # Database schema definitions
│   ├── security_config.py           # Security policies & validation
│   ├── performance_config.py        # Performance monitoring settings
│   └── logging_config.py            # Logging configuration
│
├── utils/                           # Utility Modules
│   ├── __init__.py
│   ├── config.py                    # Core configuration loader
│   ├── database.py                  # Enhanced DatabaseManager
│   ├── error_handling.py            # Error handling & validation decorators
│   ├── performance.py               # Performance monitoring utilities
│   └── cache_manager.py             # Redis + memory caching system
│
├── components/                      # Feature Components
│   ├── __init__.py
│   ├── hazard_map.py               # Interactive Folium map
│   ├── enhanced_route_planner.py    # Smart route planning
│   ├── enhanced_safety_gpt.py       # AI-powered recommendations
│   ├── enhanced_data_ingestion.py   # Real-time data aggregation
│   ├── community_reporting.py       # User hazard reporting
│   └── real_mapbox_integration.py   # Mapbox API integration
│
├── models/                          # ML/Data Models
│   ├── __init__.py
│   ├── hazard_clustering.py        # DBSCAN clustering for hotspots
│   └── image_verification.py       # YOLOv8 object detection
│
├── data/                            # Data Storage
│   ├── sample_data.py              # Sample data utilities
│   ├── guidelines/                  # Safety guidelines
│   ├── uploads/                     # User uploads
│   ├── exports/                     # Exported data
│   └── safetroute.db               # SQLite database
│
├── logs/                            # Application Logs
│   ├── safetroute.log              # Main application log
│   └── errors.log                  # Error log
│
├── backups/                         # Database Backups
├── app_final.py                     # Main Streamlit application
├── requirements.txt                 # Python dependencies
├── .env                             # Environment variables
├── .gitignore                       # Git ignore rules
├── LICENSE                          # License file
└── README.md                        # Documentation
```

---

## 🔧 Configuration

### Data Source Selection
The dashboard supports multiple data sources accessible via the sidebar:
- Real-time APIs: Live data from Mapbox, weather services
- Community Reports: Crowdsourced hazard data
- Sample Data: Generated dataset for demonstration

### Customization
Edit `config/` files to modify:
- API endpoints and credentials
- Anomaly detection parameters
- Styling and colors
- Analysis thresholds
- Security policies

**Key Configuration Files:**
```
config/app_config.py        - Feature flags and app settings
config/api_config.py        - API endpoints and keys
config/database_config.py    - Database schema and settings
config/security_config.py    - Authentication and permissions
config/performance_config.py - Monitoring and alerts
config/logging_config.py     - Logging levels and outputs
```

---

## Configuration Files

### app_config.py

**Purpose:** Application-wide settings and feature flags

**Key Settings:**
```python
APP_NAME = "SafeRoute.AI"
APP_VERSION = "1.0.0"
DEBUG = True  # Set to False in production

FEATURES = {
    'community_reporting': True,
    'ai_recommendations': True,
    'image_verification': True,
    'real_time_updates': True,
    'hazard_clustering': True,
    'route_planning': True,
    'admin_dashboard': True
}
```

### api_config.py

**Purpose:** API endpoints and service configurations

**Supported APIs:**
- **Mapbox:** Geocoding, Directions, Traffic, Static Maps
- **OpenAI:** GPT models for recommendations
- **Weather:** OpenWeatherMap for weather data

### database_config.py

**Purpose:** Database schema, indexes, and management

**Tables Created:**
- **hazards:** Road hazard reports
- **users:** User accounts and profiles
- **routes:** Calculated routes
- **recommendations:** AI recommendations

### security_config.py

**Purpose:** Security policies, password handling, and validation

**Security Features:**
- SHA-256 password hashing with salt
- Session timeout management
- Rate limiting configuration
- File upload validation

### performance_config.py

**Purpose:** Performance monitoring and optimization

**Monitoring Features:**
- API response time tracking
- Database query monitoring
- Memory and CPU usage alerts

### logging_config.py

**Purpose:** Comprehensive application logging

**Log Levels:**
- DEBUG, INFO, WARNING, ERROR, CRITICAL

---

## 🤖 Machine Learning Features

### Hazard Clustering
- Algorithm: DBSCAN clustering from scikit-learn
- Features: Location, hazard type, severity
- Output: Hotspot identification and risk zones
- Visualization: Interactive map overlays

### Route Optimization
- Smart route calculation considering hazards
- Multiple route alternatives (safe, fast, balanced)
- Safety score computation (0-100 scale)
- Real-time hazard avoidance

### Anomaly Detection
- Identifies suspicious hazard patterns
- Statistical outlier detection
- Temporal anomaly analysis
- Visual highlighting of suspicious zones

---

## 🎨 Design System

### Color Palette
- Primary: #1f77b4 (Professional Blue)
- Success: #2ca02c (Safety Green)
- Warning: #ff7f0e (Alert Orange)
- Danger: #d62728 (Hazard Red)
- Background: #f8f9fa (Light gray)
- Text: #333333 (Dark gray)

### Layout Principles
- Clean, minimal design
- Ample white space
- Consistent spacing (8px grid)
- Mobile-responsive layouts
- Interactive elements

---

## 📋 API Integration

### Mapbox API
- **Geocoding**: Address to coordinates conversion
- **Directions**: Route calculation and optimization
- **Traffic**: Real-time traffic incident data
- **Static Maps**: Map image generation

### OpenAI API
- **GPT-3.5-turbo**: Fast, cost-effective recommendations
- **Safety Analysis**: IRC and MoRTH compliance checking

### Weather API
- **Current Conditions**: Real-time weather data
- **Forecasts**: Weather predictions for route planning

---

## 💾 Database Schema

### Hazards Table
```sql
CREATE TABLE hazards (
    id TEXT PRIMARY KEY,
    hazard_type TEXT NOT NULL,
    severity INTEGER (1-5),
    confidence REAL (0-100),
    lat REAL, lon REAL,
    location TEXT,
    description TEXT,
    source TEXT,
    verified BOOLEAN,
    timestamp DATETIME
)
```

### Users Table
```sql
CREATE TABLE users (
    username TEXT PRIMARY KEY,
    password_hash TEXT,
    email TEXT,
    role TEXT (user/admin/moderator)
)
```

### Routes Table
```sql
CREATE TABLE routes (
    id TEXT PRIMARY KEY,
    start_lat REAL, start_lon REAL,
    end_lat REAL, end_lon REAL,
    route_data TEXT (JSON),
    safety_score INTEGER (0-100)
)
```

### Recommendations Table
```sql
CREATE TABLE recommendations (
    id TEXT PRIMARY KEY,
    area TEXT,
    recommendation_data TEXT (JSON),
    priority TEXT (Low/Medium/High/Critical)
)
```

---

## 🔒 Security

### Public Access
- SafeRoute.AI is now a **public-access application** with no login required
- All features are available to all users without authentication
- Anyone can report hazards and view real-time safety data

### Data Validation
- All user inputs are validated for safety and correctness
- File uploads are restricted to safe image formats (JPG, JPEG, PNG)
- **Maximum Size:** 10 MB

### Privacy
- Community reports are stored anonymously
- User location data is not personally identifiable
- All data is stored locally in the application database
- **Validation:** MIME type + extension verification

### Data Protection
- Password hashing with salt
- SQL injection prevention
- XSS protection
- HTTPS recommended for production

---

## 📈 Performance Monitoring

### Metrics Tracked

1. **API Response Time** (target < 1000ms)
2. **Database Query Time** (target < 500ms)
3. **Page Load Time** (target < 3000ms)
4. **Memory Usage** (alert > 80%)
5. **CPU Usage** (alert > 85%)
6. **Cache Hit Rate** (target > 70%)

---

## 🎯 Usage Guide

### For End Users

1. **View Hazard Map**
   - Open application
   - Click "Live Hazard Map" tab
   - Use filters to find specific hazards
   - Click markers for detailed information

2. **Report a Hazard**
   - Click "Report Hazard" tab
   - Select hazard type and severity
   - Add description and optional photo
   - Submit report for verification

3. **Plan Safe Route**
   - Click "Safe Route Planner" tab
   - Enter start and end locations
   - Choose route preference (Safe/Fast/Balanced)
   - View recommended route with safety score

### For Administrators

1. **View Analytics**
   - Click "Analytics & Admin" tab
   - Monitor trend analysis
   - Check system performance metrics
   - Review implementation status

2. **Manage Reports**
   - Review pending community reports
   - Verify submissions with image analysis
   - Update recommendation status
   - Monitor verification rates

3. **System Maintenance**
   - Backup database regularly
   - Monitor log files
   - Clean up old data
   - Update configurations and API keys

---

## 🚀 Deployment

### Local Development
```bash
streamlit run app_final.py
```

### Production Deployment
Create `.env` with production values:
```bash
DEBUG=False
export DEBUG=False
streamlit run app_final.py --logger.level=warning
```

**Deployment Platforms:**
- Streamlit Cloud
- Heroku
- AWS/Azure/GCP
- Docker containers
- On-premise servers

---

## 🧠 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Database locked error
**Solution:**
```bash
# Close other database connections
# Or use automatic connection pooling in database.py
```

### Issue: API key not found
**Solution:**
1. Verify `.env` file exists in project root
2. Check all required keys are set
3. Restart application after changes
4. Verify key format is correct

### Issue: "Connection timeout" with APIs
**Solution:**
1. Check internet connection
2. Verify API keys are valid and active
3. Check firewall and proxy settings
4. Verify API rate limits not exceeded

### Issue: High memory usage
**Solution:**
1. Reduce cache size in `config/app_config.py`
2. Enable data cleanup in database settings
3. Reduce log retention period
4. Restart application to free memory

### Issue: Slow response times
**Solution:**
1. Check database indexes are created
2. Monitor query performance using logs
3. Enable caching for frequently accessed data
4. Increase timeout values if needed
5. Check CPU and memory availability

---

## 🔑 Environment Variables

### Required
- `OPENAI_API_KEY` - OpenAI API key
- `MAPBOX_ACCESS_TOKEN` - Mapbox token

### Optional
- `WEATHER_API_KEY` - OpenWeatherMap key
- `GOOGLE_MAPS_API_KEY` - Google Maps key
- `DEBUG` - Debug mode (True/False)
- `CACHE_TIMEOUT` - Cache timeout in seconds
- `HAZARD_UPDATE_INTERVAL` - Update interval in seconds

---

## 🤝 Contributing

This project welcomes contributions. To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

---

## 📄 License

Open Source - See LICENSE file for details

---

## 🙏 Acknowledgments

- Open source community for tools and libraries
- Contributors who help improve road safety
- Communities benefiting from safer transportation

---

## 📞 Support

For technical issues or questions:
- Check troubleshooting section above
- Verify Python environment meets requirements
- Ensure internet connectivity for API features
- Review logs in `logs/` directory
- Check project documentation

---

**Built with ❤️ for Safer Roads and Smarter Communities**

SafeRoute.AI - Intelligent Route Planning for Safer Communities
