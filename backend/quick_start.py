#!/usr/bin/env python3
"""
Quick Start Guide for Sarathi Guardian System
Step-by-step instructions for testing and running the system
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🛡️ SARATHI GUARDIAN - {title.upper()}")
    print(f"{'='*60}")

def print_step(step, description):
    print(f"\n📋 STEP {step}: {description}")
    print("-" * 40)

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.8+")
        return False

def check_files():
    """Check if required files exist"""
    required_files = [
        'requirements.txt',
        'app/main.py',
        'app/agent_core/events/__init__.py',
        'app/agent_core/analytics/predictive_engine.py',
        'app/agent_core/knowledge/rag_system.py',
        'app/agent_core/guardian/resilience_system.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print("\n❌ Missing files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("\n✅ All required files present")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        # Check if virtual environment exists
        if os.path.exists('.venv'):
            print("✅ Virtual environment found")
        else:
            print("🔧 Creating virtual environment...")
            subprocess.run([sys.executable, '-m', 'venv', '.venv'], check=True)
        
        # Install requirements
        if os.name == 'nt':  # Windows
            pip_cmd = ['.venv\\Scripts\\pip.exe']
        else:  # Unix/Linux/MacOS
            pip_cmd = ['.venv/bin/pip']
        
        subprocess.run(pip_cmd + ['install', '-r', 'requirements.txt'], check=True)
        print("✅ Dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        print("🔧 Creating .env file...")
        
        env_content = '''# Sarathi Guardian Environment Configuration
DATABASE_URL=sqlite:///./sarathi.db
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
REDIS_URL=redis://localhost:6379

# Development settings
DEBUG=True
HOST=0.0.0.0
PORT=8000
'''
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ .env file created")
        print("⚠️ Please update API keys in .env file")
    else:
        print("✅ .env file already exists")

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting Sarathi Guardian API server...")
    print("📍 URL: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("\n🔧 To stop the server, press Ctrl+C")
    
    try:
        if os.name == 'nt':  # Windows
            python_cmd = ['.venv\\Scripts\\python.exe']
        else:  # Unix/Linux/MacOS
            python_cmd = ['.venv/bin/python']
        
        subprocess.run(python_cmd + ['-m', 'uvicorn', 'app.main:app', '--reload', '--host', '0.0.0.0', '--port', '8000'])
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")

def run_tests():
    """Run the test suite"""
    print("🧪 Running Sarathi Guardian test suite...")
    
    try:
        if os.name == 'nt':  # Windows
            python_cmd = ['.venv\\Scripts\\python.exe']
        else:  # Unix/Linux/MacOS
            python_cmd = ['.venv/bin/python']
        
        subprocess.run(python_cmd + ['test_guardian_system.py'], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed: {e}")

def cleanup_files():
    """Remove unnecessary files"""
    print("🧹 Cleaning up unnecessary files...")
    
    files_to_remove = [
        '../test_state_validation.py',  # Old test file
        'earnings_data.json',  # Sample data file
    ]
    
    directories_to_clean = [
        '__pycache__',
        'app/__pycache__',
        'app/agent_core/__pycache__',
        'app/api/__pycache__',
        'app/core/__pycache__',
        'app/db/__pycache__'
    ]
    
    removed_count = 0
    
    # Remove specific files
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"🗑️ Removed: {file_path}")
                removed_count += 1
            except Exception as e:
                print(f"⚠️ Could not remove {file_path}: {e}")
    
    # Clean pycache directories
    import shutil
    for dir_path in directories_to_clean:
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
                print(f"🗑️ Cleaned: {dir_path}")
                removed_count += 1
            except Exception as e:
                print(f"⚠️ Could not clean {dir_path}: {e}")
    
    print(f"\n✅ Cleanup complete - {removed_count} items removed")

def show_usage_guide():
    """Show how to use the system"""
    print_header("USAGE GUIDE")
    
    print("""
🔧 BASIC USAGE:

1. Start the API server:
   python quick_start.py --start

2. Run tests:
   python quick_start.py --test

3. Clean up files:
   python quick_start.py --cleanup

4. Full setup:
   python quick_start.py --setup

📱 API ENDPOINTS:

• Health Check: GET /health
• Root Info: GET /
• API Docs: GET /docs

• Events: POST /api/v1/events/emit
• Monitoring: POST /api/v1/events/monitoring/{user_id}/start
• Alerts: GET /api/v1/events/alerts/{user_id}
• Agents: POST /api/v1/agents/interact

🧪 TESTING:

• Run offline tests: python test_guardian_system.py --offline
• Run full tests: python test_guardian_system.py (server must be running)

🛡️ GUARDIAN FEATURES:

• Real-time monitoring of driver health, vehicle condition, and finances
• Automatic alert system with multi-channel notifications
• Predictive analytics for earnings optimization and maintenance
• Autonomous interventions for critical situations
• RAG-powered knowledge system for gig worker expertise

🔗 WebSocket: ws://localhost:8000/api/v1/events/ws/{user_id}
""")

def main():
    """Main quick start function"""
    print_header("QUICK START GUIDE")
    
    if len(sys.argv) < 2:
        show_usage_guide()
        return
    
    command = sys.argv[1]
    
    if command == "--setup":
        print_step(1, "Checking System Requirements")
        if not check_python_version():
            return
        
        print_step(2, "Checking Required Files")
        if not check_files():
            return
        
        print_step(3, "Installing Dependencies")
        if not install_dependencies():
            return
        
        print_step(4, "Creating Configuration")
        create_env_file()
        
        print_step(5, "Cleaning Up")
        cleanup_files()
        
        print_header("SETUP COMPLETE")
        print("🎉 Sarathi Guardian is ready!")
        print("\n🚀 To start the server: python quick_start.py --start")
        print("🧪 To run tests: python quick_start.py --test")
    
    elif command == "--start":
        print_header("STARTING SERVER")
        start_server()
    
    elif command == "--test":
        print_header("RUNNING TESTS")
        run_tests()
    
    elif command == "--cleanup":
        print_header("CLEANING UP")
        cleanup_files()
    
    else:
        print(f"❌ Unknown command: {command}")
        show_usage_guide()

if __name__ == "__main__":
    main()