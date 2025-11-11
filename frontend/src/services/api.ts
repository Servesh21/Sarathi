import axios from 'axios';

// Configure API base URL - update this to match your backend
const API_BASE_URL = 'http://localhost:8000/api/v1';

export const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
    // TODO: Get token from auth store
    const token = null; // Replace with actual token from store
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // TODO: Handle unauthorized - logout user
            console.log('Unauthorized request');
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

// Agent interaction endpoints
export const agentAPI = {
    sendMessage: (message: string, conversationId?: string) =>
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