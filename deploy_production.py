import os
import subprocess
import sys

def setup_production():
    \"\"\"Production setup script\"\"\"
    print("ðŸš€ Setting up SafeRoute.AI for Production...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 8):
        print("âŒ Python 3.8 or higher required")
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
        print(f"âœ… Created directory: {directory}")
    
    # Install production dependencies
    print("ðŸ“¦ Installing production dependencies...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    
    print("\nðŸŽ‰ Production setup completed!")
    print("\nðŸ“‹ Next Steps:")
    print("1. Update .env with your production API keys")
    print("2. Configure your web server (nginx/apache)")
    print("3. Set up SSL certificates")
    print("4. Configure backup schedules")
    print("5. Run: streamlit run app_final.py")

if __name__ == "__main__":
    setup_production()
