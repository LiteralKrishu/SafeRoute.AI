import os
import subprocess
import sys

def setup_production():
    \"\"\"Production setup script\"\"\"
    print("[INFO] Setting up SafeRoute.AI for Production...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 8):
        print("[ERROR] Python 3.8 or higher required")
        sys.exit(1)
    
    # Create production directory structure
    directories = [
        'data',
        'models',
        'logs',
        'uploads',
        'exports',
        'backups',
        'config'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"[OK] Created directory: {directory}")
    
    # Install production dependencies
    print("[INFO] Installing production dependencies (requirements.txt)...")
    result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    if result.returncode != 0:
        print("[WARN] pip install returned a non-zero status. Please check the output above for errors.")
    
    print("\n[INFO] Production setup completed!")
    print("\nNext Steps:")
    print("1. Update .env with your production API keys")
    print("2. Configure your web server (nginx/apache)")
    print("3. Set up SSL certificates")
    print("4. Configure backup schedules")
    print("5. Run: streamlit run app_final.py")

if __name__ == "__main__":
    setup_production()
