# 🛡️ Sarathi Guardian System - Testing & Deployment Guide

## 🚀 Quick Start

### 1. Setup the System
```bash
cd backend
python quick_start.py --setup
```

### 2. Start the Server
```bash
python quick_start.py --start
```

### 3. Test the System
```bash
python quick_start.py --test
```

## 🧪 Testing Strategy

### Phase 1: Basic Component Tests (Offline)
```bash
# Test core components without server
cd backend
python test_guardian_system.py --offline
```
**Tests:**
- ✅ ML imports (RAG, predictive models)
- ✅ Database models structure
- ✅ Core guardian components

### Phase 2: API Integration Tests (Online)
```bash
# Start server first
python quick_start.py --start

# In another terminal, run full tests
python test_guardian_system.py
```
**Tests:**
- ✅ API health endpoints
- ✅ Event emission and processing
- ✅ Alert management system
- ✅ Monitoring endpoints
- ✅ Agent interaction endpoints

### Phase 3: Real-time Features Test
```bash
# Test WebSocket connections
curl -X POST "http://localhost:8000/api/v1/events/monitoring/test_user/start"

# Test event emission
curl -X POST "http://localhost:8000/api/v1/events/emit" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "surge_detected",
    "severity": "medium",
    "user_id": "test_user",
    "data": {"multiplier": 1.5, "area": "Downtown"}
  }'

# Test alerts
curl "http://localhost:8000/api/v1/events/alerts/test_user"
```

## 🔧 Manual Testing Scenarios

### Scenario 1: Vehicle Health Crisis
```json
POST /api/v1/events/emit
{
  "event_type": "vehicle_critical",
  "severity": "critical",
  "user_id": "test_driver",
  "data": {
    "issue_description": "Engine overheating detected",
    "health_score": 25,
    "location": "Highway NH1"
  }
}
```
**Expected:** Critical alert, emergency service recommendations

### Scenario 2: Earnings Opportunity
```json
POST /api/v1/events/emit
{
  "event_type": "surge_detected", 
  "severity": "medium",
  "user_id": "test_driver",
  "data": {
    "multiplier": 2.0,
    "area": "Airport",
    "duration_estimate": 45
  }
}
```
**Expected:** Push notification, navigation suggestions

### Scenario 3: Burnout Warning
```json
POST /api/v1/events/emit
{
  "event_type": "burnout_warning",
  "severity": "high", 
  "user_id": "test_driver",
  "data": {
    "consecutive_days": 12,
    "daily_hours_avg": 14,
    "sleep_hours": 4
  }
}
```
**Expected:** Rest recommendations, wellness alerts

## 📱 Frontend Integration Testing

### Mobile App Connection
```javascript
// Test WebSocket connection
const ws = new WebSocket('ws://localhost:8000/api/v1/events/ws/test_user');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Guardian alert:', data);
};

// Test API calls
fetch('http://localhost:8000/api/v1/events/alerts/test_user')
  .then(response => response.json())
  .then(alerts => console.log('User alerts:', alerts));
```

## 🔍 Performance Testing

### Load Testing with Artillery
```bash
# Install Artillery
npm install -g artillery

# Create load test config
cat > load-test.yml << EOF
config:
  target: 'http://localhost:8000'
  phases:
    - duration: 60
      arrivalRate: 10

scenarios:
  - name: "API Health Check"
    requests:
      - get:
          url: "/health"
  - name: "Event Emission"
    requests:
      - post:
          url: "/api/v1/events/emit"
          json:
            event_type: "trip_completed"
            severity: "low"
            user_id: "load_test_user"
            data:
              earnings: 150
EOF

# Run load test
artillery run load-test.yml
```

## ⚡ System Monitoring

### Real-time System Health
```bash
# Monitor API logs
tail -f app.log

# Check memory usage
python -c "
import psutil
print(f'Memory: {psutil.virtual_memory().percent}%')
print(f'CPU: {psutil.cpu_percent()}%')
"

# Monitor Redis (if installed)
redis-cli monitor
```

## 🐛 Troubleshooting

### Common Issues & Solutions

1. **Import Errors**
   ```bash
   # Missing dependencies
   pip install -r requirements.txt
   
   # Path issues
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

2. **Database Issues**
   ```bash
   # Recreate database
   rm sarathi.db
   python -c "from app.db.database import init_db; init_db()"
   ```

3. **Port Conflicts**
   ```bash
   # Check what's using port 8000
   netstat -tulpn | grep :8000
   
   # Use different port
   uvicorn app.main:app --port 8001
   ```

4. **Redis Connection Issues**
   ```bash
   # Start Redis (if available)
   redis-server
   
   # Or disable Redis in config
   export REDIS_URL=""
   ```

## 📊 Expected Test Results

### Successful Test Output
```
🚀 Starting Sarathi Guardian System Tests...
==================================================

🔍 Testing API Health...
✅ Root endpoint working
✅ Health endpoint working

🧠 Testing ML Components...
✅ ML imports successful
✅ ML components can process test data

⚡ Testing Event System...
✅ Event emission working

📱 Testing Monitoring Endpoints...
✅ Monitoring start endpoint working
✅ Get alerts endpoint working
✅ Monitoring stop endpoint working

🤖 Testing Agent Endpoints...
✅ Agent interaction endpoint working

🗄️ Testing Database Models...
✅ Database models import successfully
✅ Database models are properly defined

==================================================
📊 TEST RESULTS SUMMARY
==================================================

API_TESTS:
  ✅ health: PASS

ML_TESTS:
  ✅ components: PASS

EVENT_TESTS:
  ✅ emission: PASS
  ✅ monitoring: PASS

AGENT_TESTS:
  ✅ interaction: PASS

INTEGRATION_TESTS:
  ✅ database: PASS

==================================================
OVERALL RESULTS: 6/6 tests passed (100.0%)
🎉 System is ready for deployment!
```

## 🚀 Deployment Checklist

- [ ] All tests passing (>80% success rate)
- [ ] API endpoints responding correctly
- [ ] Database schema created successfully
- [ ] Event system processing correctly
- [ ] Alert system sending notifications
- [ ] WebSocket connections working
- [ ] ML components loading without errors
- [ ] Error handling functioning properly
- [ ] Environment variables configured
- [ ] Security measures in place

## 🔧 Production Configuration

### Environment Variables (.env)
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/sarathi_guardian

# APIs
OPENAI_API_KEY=your-openai-key
GOOGLE_MAPS_API_KEY=your-maps-key
SMS_API_KEY=your-sms-provider-key

# Redis
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-super-secret-key-here
ALLOWED_ORIGINS=your-frontend-domain.com

# Production
DEBUG=False
LOG_LEVEL=INFO
```

### Docker Deployment
```bash
# Build container
docker build -t sarathi-guardian .

# Run with environment
docker run -p 8000:8000 --env-file .env sarathi-guardian
```

## 📈 Success Metrics

The system is considered ready when:

1. **API Health**: 100% uptime, <200ms response time
2. **Event Processing**: <1 second event-to-alert time
3. **Guardian Interventions**: >95% accuracy in crisis detection
4. **Real-time Features**: WebSocket connections stable
5. **Database Performance**: Query times <100ms
6. **ML Predictions**: >85% accuracy in predictions
7. **Alert Delivery**: >99% alert delivery success rate

## 🎯 Next Steps

After successful testing:

1. **Frontend Integration**: Connect React Native app
2. **Real API Keys**: Configure production API keys
3. **Production Database**: Set up PostgreSQL
4. **Monitoring Setup**: Add APM tools
5. **Security Audit**: Review security measures
6. **Load Testing**: Test with realistic traffic
7. **User Acceptance**: Beta testing with real drivers