import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Use your machine's LAN IP address here instead of localhost
const API_URL = process.env.EXPO_PUBLIC_API_URL || 'http://192.168.29.61:8000';

const api = axios.create({
    baseURL: API_URL,
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor
api.interceptors.request.use(
    async (config) => {
        const token = await AsyncStorage.getItem('authToken');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        if (error.response?.status === 401) {
            // Token expired or invalid
            await AsyncStorage.removeItem('authToken');
            await AsyncStorage.removeItem('user');
            // Navigate to login screen
        }
        return Promise.reject(error);
    }
);

export default api;
