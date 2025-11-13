import axios from 'axios';

// Configure API base URL - handles different environments
const getBaseURL = () => {
    // For Expo development
    if (__DEV__) {
        // For physical device testing with Expo Go, use your computer's IP
        // Your computer's IP addresses found: 192.168.29.61, 192.168.10.1

        // Try this IP first (most likely to work):
        return 'https://pbjpfwlj-8000.inc1.devtunnels.ms/api/v1';

        // Fallback options if above doesn't work:
        // return 'http://192.168.10.1:8000/api/v1';
        // return 'http://localhost:8000/api/v1'; // For simulator/web only
    }
    // Production URL (when deployed)
    return 'https://your-production-api.com/api/v1';
};

const API_BASE_URL = getBaseURL();

export const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 10000, // 10 second timeout
});

// Add logging for debugging
console.log('🔧 API Base URL:', API_BASE_URL);

// Request interceptor to add auth token and logging
api.interceptors.request.use((config) => {
    console.log('📤 API Request:', config.method?.toUpperCase(), config.url);

    // TODO: Get token from auth store
    const token = null; // Replace with actual token from store
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Response interceptor for error handling and logging
api.interceptors.response.use(
    (response) => {
        console.log('📥 API Response:', response.status, response.config.url);
        return response;
    },
    (error) => {
        console.error('❌ API Error:', error.message);
        console.error('❌ API Error Details:', {
            url: error.config?.url,
            method: error.config?.method,
            status: error.response?.status,
            statusText: error.response?.statusText,
            baseURL: error.config?.baseURL,
        });

        if (error.response?.status === 401) {
            // TODO: Handle unauthorized - logout user
            console.log('Unauthorized request');
        } else if (error.code === 'NETWORK_ERROR' || !error.response) {
            console.error('🔌 Network Error - Check if backend is running at:', API_BASE_URL);
        }

        return Promise.reject(error);
    }
);

// Auth endpoints
export const authAPI = {
    login: (email: string, password: string) =>
        api.post('/auth/login', { email, password }),

    register: (name: string, email: string, password: string) =>
        api.post('/auth/register', { name, email, password }),

    refreshToken: (refreshToken: string) =>
        api.post('/auth/refresh', { refresh_token: refreshToken }),
};

// Agent interaction endpoints - OPTIMIZED AI AGENTS
export const agentAPI = {
    // Main chat endpoint - auto-detects intent and routes to appropriate agent
    sendMessage: (message: string, userId?: string) =>
        api.post('/agents/chat', {
            message,
            user_id: userId || 'mobile_user'
        }),

    // Direct earnings queries for specialized financial analysis
    getEarnings: (message: string, userId?: string) =>
        api.post('/agents/earnings', {
            message,
            user_id: userId || 'mobile_user'
        }),

    // Health check to verify agents are operational
    checkHealth: () =>
        api.get('/agents/health'),

    // Test individual tools (for debugging)
    testWeather: (city: string) =>
        api.get(`/agents/test/weather/${city}`),

    testMechanics: (city: string) =>
        api.get(`/agents/test/mechanics/${city}`),

    // Legacy endpoint for backward compatibility
    sendMessageLegacy: (message: string, conversationId?: string) =>
        api.post('/agent/message', { message, conversation_id: conversationId }),

    getConversations: () =>
        api.get('/agent/conversations'),

    getConversation: (conversationId: string) =>
        api.get(`/agent/conversations/${conversationId}`),
};

// User profile endpoints
export const userAPI = {
    getProfile: () =>
        api.get('/user/profile'),

    updateProfile: (data: any) =>
        api.put('/user/profile', data),

    getVehicles: () =>
        api.get('/user/vehicles'),

    addVehicle: (vehicleData: any) =>
        api.post('/user/vehicles', vehicleData),
};