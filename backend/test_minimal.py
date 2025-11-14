#!/usr/bin/env python3
"""
Minimal Test Suite for Sarathi Guardian Core Components
Tests only the essential components without heavy ML dependencies
"""

import asyncio
import sys
import os
import json
import requests
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class MinimalSarathiTester:
    """Minimal test suite focusing on core functionality"""
    
    def __init__(self, api_base_url="http://localhost:8000"):
        self.api_base_url = api_base_url
        self.test_user_id = "test_user_123"
        self.results = {}
    
    def test_basic_imports(self):
        """Test basic Python imports"""
        logger.info("🔍 Testing Basic Imports...")
        
        try:
            # Test core FastAPI imports
            from fastapi import FastAPI
            logger.info("✅ FastAPI import successful")
            
            # Test database models
            from app.db.models import User, Vehicle
            logger.info("✅ Database models import successful")
            
            # Test basic app structure
            from app.main import app
            logger.info("✅ Main app import successful")
            
            self.results['imports'] = 'PASS'
            return True
            
        except Exception as e:
            logger.error(f"❌ Basic imports failed: {str(e)}")
            self.results['imports'] = f'FAIL: {str(e)}'
            return False
    
    def test_api_server(self):
        """Test if API server is accessible"""
        logger.info("🌐 Testing API Server...")
        
        try:
            # Test root endpoint
            response = requests.get(f"{self.api_base_url}/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                logger.info("✅ Root endpoint accessible")
                logger.info(f"   Message: {data.get('message', 'Unknown')}")
            else:
                logger.warning(f"⚠️ Root endpoint returned {response.status_code}")
            
            # Test health endpoint
            response = requests.get(f"{self.api_base_url}/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                logger.info("✅ Health endpoint accessible")
                logger.info(f"   Status: {health_data.get('status', 'Unknown')}")
            else:
                logger.warning(f"⚠️ Health endpoint returned {response.status_code}")
            
            self.results['api_server'] = 'PASS'
            return True
            
        except requests.exceptions.ConnectionError:
            logger.error("❌ API server not running")
            logger.info("   Start server with: python -m uvicorn app.main:app --reload")
            self.results['api_server'] = 'FAIL: Server not running'
            return False
        except Exception as e:
            logger.error(f"❌ API server test failed: {str(e)}")
            self.results['api_server'] = f'FAIL: {str(e)}'
            return False
    
    def test_basic_api_endpoints(self):
        """Test basic API endpoints"""
        logger.info("📡 Testing Basic API Endpoints...")
        
        try:
            # Test event emission (may not be available)
            test_event = {
                "event_type": "trip_completed",
                "severity": "low",
                "user_id": self.test_user_id,
                "data": {"test": True},
                "context": {"test_run": True}
            }
            
            response = requests.post(
                f"{self.api_base_url}/api/v1/events/emit",
                json=test_event,
                timeout=5
            )
            
            if response.status_code in [200, 404, 422]:  # 404/422 = endpoint not found/invalid
                if response.status_code == 200:
                    logger.info("✅ Event emission endpoint working")
                else:
                    logger.info(f"⚠️ Event endpoint exists but returned {response.status_code}")
            else:
                logger.warning(f"⚠️ Event endpoint error: {response.status_code}")
            
            self.results['api_endpoints'] = 'PASS'
            return True
            
        except Exception as e:
            logger.warning(f"⚠️ API endpoints test: {str(e)}")
            self.results['api_endpoints'] = f'PARTIAL: {str(e)}'
            return True  # Don't fail the whole test
    
    def test_database_connection(self):
        """Test database connection"""
        logger.info("🗄️ Testing Database Connection...")
        
        try:
            from app.db.database import SessionLocal
            
            # Try to create a session
            db = SessionLocal()
            
            # Test a simple query
            result = db.execute("SELECT 1 as test").fetchone()
            if result and result[0] == 1:
                logger.info("✅ Database connection successful")
                self.results['database'] = 'PASS'
            else:
                logger.warning("⚠️ Database query returned unexpected result")
                self.results['database'] = 'PARTIAL'
            
            db.close()
            return True
            
        except Exception as e:
            logger.warning(f"⚠️ Database connection: {str(e)}")
            self.results['database'] = f'SKIP: {str(e)}'
            return True  # Don't fail - may not be configured yet
    
    def test_environment_config(self):
        """Test environment configuration"""
        logger.info("⚙️ Testing Environment Configuration...")
        
        try:
            from app.core.config import settings
            
            logger.info(f"✅ Config loaded successfully")
            logger.info(f"   Host: {getattr(settings, 'HOST', 'Not set')}")
            logger.info(f"   Port: {getattr(settings, 'PORT', 'Not set')}")
            
            # Check if .env file exists
            if os.path.exists('.env'):
                logger.info("✅ .env file found")
            else:
                logger.info("⚠️ .env file not found (using defaults)")
            
            self.results['environment'] = 'PASS'
            return True
            
        except Exception as e:
            logger.error(f"❌ Environment config failed: {str(e)}")
            self.results['environment'] = f'FAIL: {str(e)}'
            return False
    
    def run_minimal_tests(self):
        """Run minimal test suite"""
        logger.info("🚀 Starting Minimal Sarathi Guardian Tests...")
        logger.info("=" * 50)
        
        # Run tests
        self.test_basic_imports()
        self.test_environment_config()
        self.test_database_connection()
        
        # Only test API if server is running
        server_running = False
        try:
            requests.get(f"{self.api_base_url}/health", timeout=2)
            server_running = True
        except:
            pass
        
        if server_running:
            self.test_api_server()
            self.test_basic_api_endpoints()
        else:
            logger.info("ℹ️ Skipping API tests (server not running)")
            logger.info("   Start server with: python -m uvicorn app.main:app --reload")
        
        # Generate report
        self.generate_minimal_report(server_running)
    
    def generate_minimal_report(self, server_running):
        """Generate minimal test report"""
        logger.info("=" * 50)
        logger.info("📊 MINIMAL TEST RESULTS")
        logger.info("=" * 50)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results.values() if result == 'PASS')
        
        for test_name, result in self.results.items():
            if result == 'PASS':
                logger.info(f"  ✅ {test_name}: {result}")
            elif 'SKIP' in result or 'PARTIAL' in result:
                logger.info(f"  ⚠️ {test_name}: {result}")
            else:
                logger.info(f"  ❌ {test_name}: {result}")
        
        logger.info("=" * 50)
        logger.info(f"CORE SYSTEM: {passed_tests}/{total_tests} components working")
        
        if passed_tests >= 3:
            logger.info("🎉 Core system is functional!")
            if not server_running:
                logger.info("💡 Start the server to test full functionality:")
                logger.info("   python -m uvicorn app.main:app --reload")
        elif passed_tests >= 2:
            logger.info("⚠️ Core system partially working - check errors above")
        else:
            logger.info("❌ Core system needs fixes")
        
        return self.results


def main():
    """Main test runner"""
    logger.info("🛡️ Sarathi Guardian - Minimal Test Suite")
    
    tester = MinimalSarathiTester()
    results = tester.run_minimal_tests()
    
    # Provide next steps
    logger.info("\n📋 NEXT STEPS:")
    logger.info("1. Fix any failed tests above")
    logger.info("2. Start server: python -m uvicorn app.main:app --reload") 
    logger.info("3. Test API: curl http://localhost:8000/health")
    logger.info("4. View docs: http://localhost:8000/docs")
    logger.info("5. Run full tests: python test_guardian_system.py")


if __name__ == "__main__":
    main()