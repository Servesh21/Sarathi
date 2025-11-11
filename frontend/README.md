# 📱 Sarathi Frontend

React Native mobile application for the Sarathi driving companion.

## Quick Start

### Prerequisites

- Node.js 18+
- npm or yarn
- Expo CLI (installed globally): `npm install -g expo-cli`
- Expo Go app on your mobile device (iOS/Android)

### Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

3. Scan the QR code with:
   - **iOS**: Camera app
   - **Android**: Expo Go app

### Running on Specific Platforms

```bash
# iOS Simulator (macOS only)
npm run ios

# Android Emulator
npm run android

# Web browser
npm run web
```

## Features

### Screens
- **Login/Register**: User authentication
- **Dashboard**: Main screen with earnings, stats, and AI chat
- **Garage**: Vehicle management
- **Goals**: Financial goal tracking

### Components
- **VoiceInputButton**: Voice-to-text input (placeholder)
- **HealthMeter**: Driver health score visualization

### Styling

This app uses **Tailwind CSS v4** via NativeWind for styling:
- Utility-first CSS framework
- Easy responsive design
- Consistent theming

Example:
```tsx
<View className="flex-1 bg-gray-50 p-4">
  <Text className="text-2xl font-bold text-primary-600">
    Hello Sarathi
  </Text>
</View>
```

## Project Structure

```
frontend/
├── src/
│   ├── screens/        # App screens
│   ├── components/     # Reusable components
│   ├── navigation/     # Navigation config
│   ├── services/       # API client
│   └── hooks/          # Custom React hooks
├── App.tsx             # Root component
├── package.json
└── tailwind.config.js  # Tailwind configuration
```

## Configuration

### API Endpoint

Update the API URL in `src/services/api.ts`:
```typescript
const API_BASE_URL = 'http://localhost:8000';  // For local dev
// const API_BASE_URL = 'https://your-api.com';  // For production
```

### Environment Variables

Create a `.env` file (if needed):
```
API_URL=http://localhost:8000
```

## State Management

Uses **Zustand** for lightweight state management:
- Auth state in `src/hooks/useAuth.ts`
- Easy to extend for other stores

## Testing

```bash
npm test
```

## Build for Production

```bash
# iOS
expo build:ios

# Android
expo build:android
```

## Troubleshooting

### Metro bundler issues
```bash
npm start -- --clear
```

### Node modules issues
```bash
rm -rf node_modules
npm install
```

### Expo cache issues
```bash
expo start -c
```
