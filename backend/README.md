# 🚗 Sarathi Backend

FastAPI backend for the Sarathi driving companion application.

## Quick Start

### Local Development with Docker

1. Make sure you have Docker and Docker Compose installed
2. From the project root, run:
   ```bash
   docker-compose up --build
   ```

### Local Development without Docker

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── api/              # API routes
│   ├── agent_core/       # AI agent logic
│   ├── core/             # Configuration
│   ├── db/               # Database models
│   └── main.py           # Entry point
├── Dockerfile
└── requirements.txt
```

## Environment Variables

See `.env.example` for all required environment variables.

Key variables:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `GOOGLE_MAPS_API_KEY`: For maps functionality
- `OPENWEATHER_API_KEY`: For weather data
- `GEMINI_API_KEY`: For AI agent capabilities
