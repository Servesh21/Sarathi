# Sarathi: The Autonomous Resilience Agent

A complete full-stack production system designed for ride-sharing drivers to optimize earnings, maintain vehicle health, and build financial resilience through AI-powered insights.

## 🎯 Core Features

### 1. Earnings Engine (Daily Survival)
- **Voice Trip Logging**: Speak naturally to log trip details via WhatsApp or mobile app
- **AI Trip Extraction**: Gemini AI automatically extracts pickup, drop, fare, distance from voice
- **High-Demand Zone Recommendations**: Real-time Google Maps API integration for optimal ride zones
- **Earnings Analytics**: Track daily/weekly/monthly performance with trend analysis

### 2. Resilience Shield (Vehicle Health)
- **AI-Powered Diagnostics**: Upload vehicle images for Gemini vision AI analysis
- **Multi-Modal Health Checks**: Analyze engine, tires, body condition from photos
- **Predictive Alerts**: Proactive notifications for maintenance needs
- **WhatsApp Integration**: Instant critical alerts via WhatsApp

### 3. Growth Engine (Wealth Creation)
- **Surplus Analysis**: Automatic calculation of monthly savings potential
- **Real Financial Data**: Live integration with Alpha Vantage for FD rates, mutual funds, gold prices
- **AI Investment Recommendations**: Personalized suggestions based on risk profile and surplus
- **Goal Tracking**: Monitor progress towards financial milestones

### 4. Agentic AI System (LangGraph Orchestration)
- **ReAct-Style Agent Graph**: 5 specialized agents with tool-calling capabilities
- **User State Evaluator**: Routes queries to appropriate specialized agents
- **Pattern Recognition**: ChromaDB vector storage for learning from historical patterns
- **Conversational Interface**: Natural language chat for financial guidance

## 🏗️ Architecture

### Backend Stack
- **Framework**: FastAPI 0.115.0 (Python 3.12)
- **Database**: PostgreSQL 16 with asyncpg + SQLAlchemy 2.0 (async ORM)
- **Vector Store**: ChromaDB 0.5.15 for semantic search
- **AI Orchestration**: LangGraph 0.2.45 + LangChain 0.3.7
- **AI Model**: Google Gemini gemini-2.0-flash-exp (text, audio, vision)
- **Task Queue**: Celery 5.4.0 + Redis 5.2.0
- **Authentication**: JWT with bcrypt password hashing

### Frontend Stack
- **Framework**: React Native 0.74.0 with Expo ~51.0.0
- **Styling**: NativeWind 4.0.1 + TailwindCSS 3.4.0
- **State Management**: Zustand 4.5.5
- **HTTP Client**: Axios 1.7.7 with interceptors
- **Navigation**: React Navigation 6.x
- **Media**: expo-image-picker, expo-av (audio recording)

### External Integrations
- **Google Maps API 4.10.0**: Zone recommendations, geocoding
- **Twilio 9.3.7**: WhatsApp webhook for voice messages
- **Alpha Vantage**: Real-time financial market data

## 📦 Project Structure

```
sarathi_new/
├── backend/
│   ├── app/
│   │   ├── agents/               # LangGraph agentic system
│   │   │   ├── nodes/           # 5 specialized agent nodes
│   │   │   ├── tools/           # Database, Maps, Financial, Chroma tools
│   │   │   ├── state.py         # Agent state TypedDict
│   │   │   └── sarathi_agent.py # Main orchestrator
│   │   ├── models/              # SQLAlchemy database models
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   ├── routers/             # FastAPI route handlers (7 routers)
│   │   ├── services/            # External API integrations
│   │   ├── config.py            # Settings with BaseSettings
│   │   ├── database.py          # Async DB engine + ChromaDB client
│   │   ├── auth.py              # JWT authentication
│   │   └── main.py              # FastAPI app entry point
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── api/                 # Axios API client + modules
│   │   ├── store/               # Zustand state stores
│   │   ├── screens/             # React Native screens
│   │   ├── navigation/          # React Navigation setup
│   │   └── components/          # Reusable UI components
│   ├── App.tsx
│   ├── package.json
│   ├── app.json                 # Expo configuration
│   └── tailwind.config.js
│
├── docker-compose.yml           # Multi-container orchestration
└── README.md
```

## 🚀 Setup & Installation

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.12+ (for backend development)
- API Keys:
  - Google Gemini API key ([Get here](https://ai.google.dev/))
  - Google Maps API key ([Get here](https://developers.google.com/maps))
  - Alpha Vantage API key ([Get here](https://www.alphavantage.co/support/#api-key))
  - Twilio Account SID & Auth Token ([Get here](https://www.twilio.com/))

### Backend Setup (Docker)

1. **Clone and navigate to project**:
   ```bash
   cd sarathi_new
   ```

2. **Create environment file**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your API keys:
   ```env
   GEMINI_API_KEY=your_actual_key_here
   GOOGLE_MAPS_API_KEY=your_actual_key_here
   ALPHA_VANTAGE_API_KEY=your_actual_key_here
   TWILIO_ACCOUNT_SID=your_actual_sid_here
   TWILIO_AUTH_TOKEN=your_actual_token_here
   ```

3. **Start all services**:
   ```bash
   docker-compose up -d
   ```
   This will start:
   - PostgreSQL (port 5432)
   - Redis (port 6379)
   - ChromaDB (port 8000)
   - FastAPI backend (port 8080)
   - Celery worker

4. **Verify services**:
   ```bash
   docker-compose ps
   ```

5. **Create database tables**:
   ```bash
   docker-compose exec backend python -c "from app.database import engine, Base; Base.metadata.create_all(bind=engine)"
   ```

6. **View logs**:
   ```bash
   docker-compose logs -f backend
   ```

7. **API Documentation** (Swagger):
   Open http://localhost:8080/docs

### Frontend Setup (React Native/Expo)

1. **Navigate to frontend**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Create environment file**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env`:
   ```env
   API_URL=http://localhost:8080
   ```
   For physical device testing, replace `localhost` with your machine's IP address.

4. **Start Expo development server**:
   ```bash
   npx expo start
   ```

5. **Run on device/emulator**:
   - Press `i` for iOS simulator
   - Press `a` for Android emulator
   - Scan QR code with Expo Go app for physical device

## 🔧 Development Workflow

### Backend Development

**Run locally without Docker**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

**Database migrations** (Alembic):
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

**Run tests**:
```bash
pytest
```

### Frontend Development

**Type checking**:
```bash
npx tsc --noEmit
```

**Lint code**:
```bash
npm run lint
```

**Clear cache**:
```bash
npx expo start -c
```

## 📱 Usage Guide

### For Drivers

1. **Register Account**: 
   - Open app → Register with phone number, name, city
   - Login with credentials

2. **Log Trips (Voice)**:
   - Navigate to "Earnings" tab
   - Tap "Log New Trip"
   - Hold microphone button and speak: "I went from Andheri to Bandra, fare was 250 rupees, distance 8 km"
   - AI extracts all details automatically

3. **Get Zone Recommendations**:
   - Check "High Demand Zones" card on Earnings screen
   - See live demand scores and average fares
   - Navigate to recommended zones

4. **Check Vehicle Health**:
   - Navigate to "Health" tab
   - Tap "Select Images" → Choose photos of engine, tires, body
   - Tap "Analyze Vehicle" → AI provides diagnostic report
   - Receive WhatsApp alerts for critical issues

5. **Plan Investments**:
   - Navigate to "Growth" tab
   - View monthly surplus analysis
   - See AI-recommended investment options (FDs, mutual funds, gold)
   - Track active investments and returns

6. **Chat with AI Agent**:
   - Tap "Chat with Sarathi AI" from dashboard
   - Ask questions like:
     - "What zones should I target today?"
     - "When should I service my vehicle?"
     - "Where should I invest my surplus this month?"

## 🔑 API Endpoints

### Authentication
- `POST /auth/register` - Create new user account
- `POST /auth/token` - Login and get JWT token
- `GET /auth/me` - Get current user profile
- `PUT /auth/me` - Update user profile

### Trips (Earnings Engine)
- `GET /trips` - List trips with filtering
- `POST /trips` - Create trip manually
- `POST /trips/voice` - Upload audio file for trip extraction
- `GET /trips/stats` - Get earnings analytics
- `GET /trips/recommendations/zones` - Get high-demand zones

### Vehicles (Resilience Shield)
- `GET /vehicles` - List user vehicles
- `GET /vehicles/{id}/health-checks` - Get health check history
- `POST /vehicles/{id}/health-check` - Upload images for AI diagnostics

### Goals
- `GET /goals` - List financial goals
- `POST /goals` - Create new goal
- `POST /goals/{id}/progress` - Add progress to goal

### Investments (Growth Engine)
- `GET /investments` - List investments
- `GET /investments/portfolio` - Get portfolio summary
- `GET /investments/surplus-analysis` - Calculate monthly surplus
- `GET /investments/recommendations` - Get AI investment suggestions

### Alerts
- `GET /alerts` - List user alerts
- `POST /alerts/{id}/mark-read` - Mark alert as read

### AI Agent
- `POST /agent/chat` - Chat with Sarathi AI agent

## 🤖 Agentic AI System Details

### Agent Nodes

1. **User State Evaluator** (`user_state_evaluator.py`):
   - Entry point for all queries
   - Routes to specialized agents based on intent
   - Uses LangChain for query classification

2. **Earnings Advisor** (`earnings_advisor.py`):
   - Analyzes trip patterns from database
   - Calls Google Maps API for zone recommendations
   - Suggests optimal working hours and routes

3. **Diagnostic Agent** (`diagnostic_agent.py`):
   - Processes vehicle health check data
   - Generates maintenance schedules
   - Predicts failure risks

4. **Surplus Planner** (`surplus_planner.py`):
   - Calculates income vs expenses
   - Applies 50-30-20 budgeting rule
   - Checks emergency fund status

5. **Investment Advisor** (`investment_advisor.py`):
   - Fetches live financial data (FDs, mutual funds, gold)
   - Matches risk profile with investment options
   - Generates personalized recommendations

### Tools

- **DatabaseTool**: Queries PostgreSQL for trip/vehicle/goal data
- **MapsTool**: Calls Google Maps Geocoding + Places API
- **FinancialTool**: Fetches Alpha Vantage market data
- **ChromaTool**: Semantic search for pattern matching

### LangGraph Workflow

```
User Query → User State Evaluator
    ├→ "earnings" → Earnings Advisor → Maps Tool + Database Tool
    ├→ "vehicle" → Diagnostic Agent → Database Tool
    ├→ "financial" → Surplus Planner → Database Tool
    │                     ↓
    │               Investment Advisor → Financial Tool + Chroma Tool
    └→ Response with recommendations + action items
```

## 🔐 Security Features

- JWT token-based authentication with 7-day expiry
- Bcrypt password hashing with salt rounds
- AsyncStorage encrypted token storage (frontend)
- CORS middleware configured for production
- Environment variable isolation for secrets
- Input validation with Pydantic schemas
- SQL injection protection via SQLAlchemy ORM

## 📊 Database Schema

**Core Tables**:
- `users`: User accounts with authentication
- `trips`: Trip records with earnings data
- `vehicles`: Vehicle information
- `vehicle_health_checks`: AI diagnostic results
- `alerts`: Notification system
- `goals`: Financial goal tracking
- `goal_progress`: Goal milestone updates
- `investments`: Investment portfolio
- `investment_recommendations`: AI suggestions

**Relationships**:
- User → Trips (one-to-many)
- User → Vehicles (one-to-many)
- Vehicle → Health Checks (one-to-many)
- User → Goals (one-to-many)
- Goal → Progress (one-to-many)
- User → Investments (one-to-many)

## 🌐 Production Deployment

### Backend (Railway/Render/AWS)

1. **Build Docker image**:
   ```bash
   docker build -t sarathi-backend ./backend
   ```

2. **Push to container registry**:
   ```bash
   docker tag sarathi-backend your-registry/sarathi-backend
   docker push your-registry/sarathi-backend
   ```

3. **Set environment variables** in hosting platform

4. **Deploy** with health check endpoint `/docs`

### Frontend (Expo EAS Build)

1. **Install EAS CLI**:
   ```bash
   npm install -g eas-cli
   ```

2. **Configure EAS**:
   ```bash
   eas build:configure
   ```

3. **Build for production**:
   ```bash
   eas build --platform android
   eas build --platform ios
   ```

4. **Submit to stores**:
   ```bash
   eas submit -p android
   eas submit -p ios
   ```

## 🐛 Troubleshooting

### Backend Issues

**Database connection error**:
```bash
docker-compose down
docker volume rm sarathi_new_postgres_data
docker-compose up -d
```

**ChromaDB not responding**:
```bash
docker-compose restart chromadb
```

**Port already in use**:
```bash
# Kill process on port 8080
lsof -ti:8080 | xargs kill -9
```

### Frontend Issues

**Metro bundler cache issues**:
```bash
npx expo start -c
rm -rf node_modules
npm install
```

**AsyncStorage errors**:
```bash
npx expo install @react-native-async-storage/async-storage
```

**Network request failed**:
- Check API_URL in `.env` matches backend URL
- Use machine IP instead of localhost for physical devices
- Ensure backend is running on correct port

## 📝 License

MIT License - See LICENSE file for details

## 👥 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 🙏 Acknowledgments

- Google Gemini AI for multimodal capabilities
- LangChain/LangGraph for agent orchestration framework
- FastAPI for high-performance async backend
- Expo for React Native development experience
- Alpha Vantage for financial market data

## 📧 Support

For issues, questions, or contributions, please open a GitHub issue or contact the development team.

---

Built with ❤️ for ride-sharing drivers to achieve financial resilience
