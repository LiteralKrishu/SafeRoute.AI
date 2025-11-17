import os
import subprocess
import sys

def setup_environment():
    """Setup script for SafeRoute.AI environment"""
    print("Setting up SafeRoute.AI Environment...")
    
    # Create necessary directories
    directories = [
        'data',
        'models', 
        'logs',
        'uploads',
        'exports'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    print("\nNext Steps:")
    print("1. Update .env file with your API keys")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run the app: streamlit run app_final.py")
    print("4. Default login: admin/admin123 or user/user123")

if __name__ == "__main__":
    setup_environment()
