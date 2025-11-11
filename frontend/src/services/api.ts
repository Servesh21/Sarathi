import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// API base URL - change this for production
const API_BASE_URL = 'http://localhost:8000';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
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

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid, clear storage
      await AsyncStorage.removeItem('authToken');
      // You can trigger a logout action here
    }
    return Promise.reject(error);
  }
);

// Auth API calls
export const authAPI = {
  register: async (email: string, password: string, fullName: string) => {
    const response = await apiClient.post('/api/v1/auth/register', {
      email,
      password,
      full_name: fullName,
    });
    return response.data;
  },

  login: async (email: string, password: string) => {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await apiClient.post('/api/v1/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },

  getProfile: async () => {
    const response = await apiClient.get('/api/v1/auth/me');
    return response.data;
  },
};

// Agent API calls
export const agentAPI = {
  chat: async (query: string, context?: any) => {
    const response = await apiClient.post('/api/v1/agent/chat', {
      query,
      context,
    });
    return response.data;
  },

  getConversationHistory: async (limit: number = 50) => {
    const response = await apiClient.get('/api/v1/agent/conversation-history', {
      params: { limit },
    });
    return response.data;
  },
};

// User profile API calls
export const userAPI = {
  getProfile: async () => {
    const response = await apiClient.get('/api/v1/users/profile');
    return response.data;
  },

  updateProfile: async (data: { full_name?: string }) => {
    const response = await apiClient.put('/api/v1/users/profile', data);
    return response.data;
  },

  getVehicles: async () => {
    const response = await apiClient.get('/api/v1/users/vehicles');
    return response.data;
  },

  addVehicle: async (vehicle: {
    make: string;
    model: string;
    year: number;
    license_plate: string;
    vehicle_type?: string;
  }) => {
    const response = await apiClient.post('/api/v1/users/vehicles', vehicle);
    return response.data;
  },

  getTrips: async (limit: number = 50) => {
    const response = await apiClient.get('/api/v1/users/trips', {
      params: { limit },
    });
    return response.data;
  },

  addTrip: async (trip: {
    vehicle_id: number;
    start_location: string;
    end_location: string;
    distance_km: number;
    earnings?: number;
  }) => {
    const response = await apiClient.post('/api/v1/users/trips', trip);
    return response.data;
  },
};

export default apiClient;
