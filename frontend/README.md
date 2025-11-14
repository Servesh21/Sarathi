# Welcome to your Expo app 👋

This is an [Expo](https://expo.dev) project created with [`create-expo-app`](https://www.npmjs.com/package/create-expo-app).

## Get started

1. Install dependencies

   ```bash
   npm install
   ```

2. Configure API URL (optional but recommended)

   Create a .env file at the project root (frontend/) and set your backend URL:

   ```bash
   EXPO_PUBLIC_API_URL=http://YOUR_COMPUTER_IP:8000/api/v1
   ```

   You can also use an HTTPS dev tunnel URL. The app will auto-fallback to `http://localhost:8000/api/v1` when running on web or emulator.

3. Start the app

   ```bash
   npx expo start
   ```

In the output, you'll find options to open the app in a

- [development build](https://docs.expo.dev/develop/development-builds/introduction/)
- [Android emulator](https://docs.expo.dev/workflow/android-studio-emulator/)
- [iOS simulator](https://docs.expo.dev/workflow/ios-simulator/)
- [Expo Go](https://expo.dev/go), a limited sandbox for trying out app development with Expo

You can start developing by editing the files inside the **app** directory. This project uses [file-based routing](https://docs.expo.dev/router/introduction).

## Backend integration cheatsheet

- Real-time alerts WebSocket: `/api/v1/events/ws/{userId}`
- Start monitoring: `POST /api/v1/events/monitoring/{userId}/start`
- Stop monitoring: `POST /api/v1/events/monitoring/{userId}/stop`
- Emit event: `POST /api/v1/events/emit`
- Get alerts: `GET /api/v1/events/alerts/{userId}`

In-app, use the Alerts tab (bell icon) to:
- Connect to live WebSocket
- Start/Stop monitoring
- Emit a test event and see alerts arrive

## Get a fresh project

When you're ready, run:

```bash
npm run reset-project
```

This command will move the starter code to the **app-example** directory and create a blank **app** directory where you can start developing.

## Learn more

To learn more about developing your project with Expo, look at the following resources:

- [Expo documentation](https://docs.expo.dev/): Learn fundamentals, or go into advanced topics with our [guides](https://docs.expo.dev/guides).
- [Learn Expo tutorial](https://docs.expo.dev/tutorial/introduction/): Follow a step-by-step tutorial where you'll create a project that runs on Android, iOS, and the web.

## Join the community

Join our community of developers creating universal apps.

- [Expo on GitHub](https://github.com/expo/expo): View our open source platform and contribute.
- [Discord community](https://chat.expo.dev): Chat with Expo users and ask questions.
