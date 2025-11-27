import './global.css';
import 'react-native-gesture-handler';
import React from 'react';
import { StatusBar } from 'expo-status-bar';
import AppNavigator from './src/navigation/AppNavigator';
// frontend/App.tsx
import { SafeAreaProvider } from 'react-native-safe-area-context';

export default function App() {
    return (
        <SafeAreaProvider>
            <StatusBar style="auto" />
            <AppNavigator />
        </SafeAreaProvider>
    );
}

