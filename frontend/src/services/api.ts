import axios from 'axios';
import Constants from 'expo-constants';

// Configure API base URL - handles different environments
const getBaseURL = () => {
    // 1) Prefer Expo public env var if provided
    const envUrl = (process.env.EXPO_PUBLIC_API_URL || Constants.expoConfig?.extra?.API_URL) as string | undefined;
    if (envUrl) return envUrl.replace(/\/$/, '');

    // 2) Dev mode sensible defaults
    if (__DEV__) {
        // For physical device testing with Expo Go, set EXPO_PUBLIC_API_URL to your machine IP:
        //   EXPO_PUBLIC_API_URL=http://192.168.x.x:8000/api/v1
        // Fallback to dev tunnel or localhost
        return 'http://localhost:8000/api/v1';
    }

    // 3) Production URL (when deployed)
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

// Helpers
export const getWsUrl = (userId: string) => {
    // Convert http(s)://host[:port]/api/v1 -> ws(s)://host[:port]/api/v1
    const base = API_BASE_URL.replace(/\/$/, '');
    const wsProto = base.startsWith('https') ? 'wss' : 'ws';
    const wsBase = base.replace(/^http(s)?:/, `${wsProto}:`);
    return `${wsBase}/events/ws/${encodeURIComponent(userId)}`;
};

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

// Events and Alerts endpoints
export const eventsAPI = {
    // Emit a generic event
    emitEvent: (payload: {
        event_type: string;
        severity: 'low' | 'medium' | 'high' | 'critical';
        user_id: string;
        data?: Record<string, any>;
        context?: Record<string, any>;
    }) => api.post('/events/emit', payload),

    // Monitoring controls
    startMonitoring: (userId: string, config?: {
        check_interval_seconds?: number;
        vehicle_health_threshold?: number;
        burnout_consecutive_days?: number;
        financial_emergency_ratio?: number;
    }) => api.post(`/events/monitoring/${encodeURIComponent(userId)}/start`, config ?? {}),

    stopMonitoring: (userId: string) =>
        api.post(`/events/monitoring/${encodeURIComponent(userId)}/stop`),

    // Alerts
    getAlerts: (userId: string, opts?: { status?: string; limit?: number }) =>
        api.get(`/events/alerts/${encodeURIComponent(userId)}`, { params: opts ?? {} }),

    acknowledgeAlert: (alertId: string, userId: string) =>
        api.post(`/events/alerts/${encodeURIComponent(alertId)}/acknowledge`, null, { params: { user_id: userId } }),

    dismissAlert: (alertId: string, userId: string) =>
        api.post(`/events/alerts/${encodeURIComponent(alertId)}/dismiss`, null, { params: { user_id: userId } }),
};