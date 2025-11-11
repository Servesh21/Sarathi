hwo # 🚀 Quick Start Guide - Sarathi

Get Sarathi up and running in minutes!

## Prerequisites Checklist

- [ ] Docker Desktop installed and running
- [ ] Node.js 18+ installed
- [ ] Git installed
- [ ] Code editor (VS Code recommended)
- [ ] Mobile device with Expo Go app (or iOS Simulator/Android Emulator)

## 📦 Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/sarathi.git
cd sarathi
```

### 2. Set Up API Keys

You'll need API keys from:
- **Google Maps API**: https://developers.google.com/maps/documentation/javascript/get-api-key
- **OpenWeather API**: https://openweathermap.org/api
- **Google Gemini API**: https://ai.google.dev/

Create the environment file:
```bash
cd backend
cp .env.example .env
```

Edit `backend/.env` and add your API keys:
```env
GOOGLE_MAPS_API_KEY=your-google-maps-key
OPENWEATHER_API_KEY=your-openweather-key
GEMINI_API_KEY=your-gemini-key
```

### 3. Start the Backend Services

From the project root:
```bash
docker-compose up --build
```

This will start:
- ✅ PostgreSQL database (port 5432)
- ✅ Redis cache (port 6379)
- ✅ FastAPI backend (port 8000)

Wait until you see:
```
sarathi_backend | INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 4. Verify Backend is Running

Open your browser and visit:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

You should see the Swagger UI documentation.

### 5. Set Up the Mobile App

Open a new terminal window:

```bash
cd frontend
npm install
```

Wait for all dependencies to install (this may take a few minutes).

### 6. Start the Mobile App

```bash
npm start
```

You'll see a QR code in the terminal.

### 7. Run on Your Device

**Option A: Physical Device**
1. Install "Expo Go" app from App Store (iOS) or Play Store (Android)
2. Scan the QR code with:
   - iOS: Camera app
   - Android: Expo Go app

**Option B: Simulator/Emulator**
- iOS (Mac only): Press `i` in the terminal
- Android: Press `a` in the terminal

### 8. Test the App

1. **Register a new account**:
   - Email: test@example.com
   - Password: password123
   - Name: Test Driver

2. **Explore features**:
   - Chat with the AI agent
   - Add vehicles to garage
   - Set financial goals

## 🎉 You're All Set!

### Quick Commands Reference

**Backend (with Docker)**
```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up --build
```

**Frontend**
```bash
# Start development server
npm start

# Clear cache and restart
npm start -- --clear

# Run on iOS simulator
npm run ios

# Run on Android emulator
npm run android
```

**Database**
```bash
# Access PostgreSQL
docker exec -it sarathi_db psql -U sarathi -d sarathi_db

# View all tables
\dt

# Exit
\q
```

## 🐛 Troubleshooting

### Backend won't start
1. Make sure Docker Desktop is running
2. Check if ports 5432, 6379, 8000 are available
3. Try `docker-compose down` then `docker-compose up --build`

### Frontend shows network error
1. Update API URL in `frontend/src/services/api.ts`:
   - For Android emulator: use `http://10.0.2.2:8000`
   - For iOS simulator: use `http://localhost:8000`
   - For physical device: use your computer's IP (e.g., `http://192.168.1.100:8000`)

### Expo QR code not working
1. Make sure phone and computer are on same WiFi network
2. Try running `npm start -- --tunnel`

### Database connection error
1. Wait 10-15 seconds for PostgreSQL to fully start
2. Check `docker-compose logs db` for errors

## 📚 Next Steps

- **Customize the app**: Edit screens in `frontend/src/screens/`
- **Add API endpoints**: Create new endpoints in `backend/app/api/v1/endpoints/`
- **Enhance AI agents**: Modify graphs in `backend/app/agent_core/graphs/`
- **Read the docs**: Check out `README.md` for detailed information

## 💡 Development Tips

1. **Auto-reload**: Both frontend and backend support hot reload
2. **API Testing**: Use the Swagger UI at http://localhost:8000/docs
3. **Debugging**: Use VS Code with the debugger for backend Python code
4. **Git branches**: Create feature branches for new work

## 📞 Need Help?

- Check `CONTRIBUTING.md` for development guidelines
- Review `README.md` for detailed documentation
- Open an issue on GitHub
- Check existing issues for solutions

Happy coding! 🚗💨
