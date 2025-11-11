# 🚗 Sarathi - Your Intelligent Driving Companion

[![CI Status](https://github.com/yourusername/sarathi/workflows/Backend%20CI/badge.svg)](https://github.com/yourusername/sarathi/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> An AI-powered driving companion that helps drivers optimize earnings, navigate efficiently, and stay safe on the road.

## 📋 Overview

Sarathi is a comprehensive platform designed for drivers, combining the power of AI agents with practical tools for managing vehicles, tracking earnings, and making informed decisions. The application features a React Native mobile frontend and a FastAPI backend with LangGraph-powered intelligent agents.

## ✨ Features

### 🤖 AI Agent Capabilities
- **Earnings Agent**: Financial insights, profitability analysis, and earnings tracking
- **Resilience Agent**: Weather conditions, route optimization, and traffic updates
- **Multi-modal Interaction**: Voice and text-based communication

### 📱 Mobile App Features
- **Dashboard**: Real-time earnings, trip stats, and driver health metrics
- **Garage Management**: Track and manage multiple vehicles
- **Goal Setting**: Set and monitor financial goals
- **Voice Input**: Hands-free interaction with AI agent
- **Beautiful UI**: Modern design with Tailwind CSS v4

### 🔧 Backend Features
- RESTful API with FastAPI
- PostgreSQL database for data persistence
- Redis for caching and task queuing
- JWT-based authentication
- Modular agent architecture with LangGraph

## 🛠️ Tech Stack

### Frontend
- **Framework**: React Native with Expo
- **Navigation**: React Navigation
- **Styling**: Tailwind CSS v4 (NativeWind)
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Language**: TypeScript

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis
- **ORM**: SQLAlchemy
- **Agent Framework**: LangGraph, LangChain
- **AI**: Google Gemini API
- **Authentication**: JWT (python-jose)
- **Language**: Python 3.11

### DevOps
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Cloud Ready**: Designed for Google Cloud Run deployment

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)
- API Keys:
  - Google Maps API Key
  - OpenWeather API Key
  - Google Gemini API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/sarathi.git
   cd sarathi
   ```

2. **Set up environment variables**
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your API keys and configuration
   ```

3. **Start the services using Docker Compose**
   ```bash
   docker-compose up --build
   ```

   This will start:
   - PostgreSQL database on port 5432
   - Redis on port 6379
   - FastAPI backend on port 8000

4. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   npm start
   ```

5. **Access the application**
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Mobile App: Use Expo Go app to scan QR code

## 📁 Project Structure

```
sarathi/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/  # API route handlers
│   │   │       └── api.py      # Main API router
│   │   ├── agent_core/
│   │   │   ├── tools/          # Agent tools (maps, weather, financial)
│   │   │   └── graphs/         # LangGraph orchestrators
│   │   ├── core/
│   │   │   └── config.py       # App configuration
│   │   ├── db/
│   │   │   ├── models.py       # Database models
│   │   │   └── database.py     # DB session management
│   │   └── main.py             # FastAPI app entry point
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── screens/            # App screens
│   │   ├── components/         # Reusable components
│   │   ├── navigation/         # Navigation setup
│   │   ├── services/           # API client
│   │   └── hooks/              # Custom hooks
│   ├── package.json
│   └── tailwind.config.js
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 🔑 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user

### Agent Interactions
- `POST /api/v1/agent/chat` - Chat with AI agent
- `GET /api/v1/agent/conversation-history` - Get chat history

### User Profile
- `GET /api/v1/users/profile` - Get user profile
- `PUT /api/v1/users/profile` - Update profile
- `GET /api/v1/users/vehicles` - Get user vehicles
- `POST /api/v1/users/vehicles` - Add vehicle
- `GET /api/v1/users/trips` - Get trip history
- `POST /api/v1/users/trips` - Log new trip

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest --cov=app tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📊 Database Schema

- **users**: User accounts and authentication
- **vehicles**: Vehicle information in user's garage
- **trips**: Trip history and earnings data
- **conversations**: Agent chat history
- **goals**: User financial goals

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Google Gemini for AI capabilities
- OpenWeather API for weather data
- Google Maps API for navigation features
- FastAPI and React Native communities

## 📞 Support

For support, email support@sarathi.app or open an issue on GitHub.

---

Made with ❤️ for drivers everywhere
