import api from './client';
import AsyncStorage from '@react-native-async-storage/async-storage';

export interface LoginCredentials {
    phone_number: string;
    password: string;
}

export interface RegisterData {
    phone_number: string;
    password: string;
    name: string;
    email?: string;
    vehicle_type?: string;
    city?: string;
    preferred_language?: string;
}

export interface User {
    id: number;
    phone_number: string;
    name: string;
    email?: string;
    vehicle_type?: string;
    city?: string;
    preferred_language: string;
    monthly_income_target: number;
    monthly_expense_average: number;
    created_at: string;
    last_login?: string;
}

export interface AuthResponse {
    access_token: string;
    token_type: string;
}

export const authAPI = {
    login: async (credentials: LoginCredentials): Promise<User> => {
        const response = await api.post<AuthResponse>('/auth/login', credentials);
        const { access_token } = response.data;

        // Store token
        await AsyncStorage.setItem('authToken', access_token);

        // Get user info
        const userResponse = await api.get<User>('/auth/me');
        await AsyncStorage.setItem('user', JSON.stringify(userResponse.data));

        return userResponse.data;
    },

    register: async (data: RegisterData): Promise<User> => {
        const response = await api.post<User>('/auth/register', data);
        return response.data;
    },

    getCurrentUser: async (): Promise<User> => {
        const response = await api.get<User>('/auth/me');
        return response.data;
    },

    updateProfile: async (data: Partial<User>): Promise<User> => {
        const response = await api.patch<User>('/auth/me', data);
        return response.data;
    },

    logout: async (): Promise<void> => {
        await AsyncStorage.removeItem('authToken');
        await AsyncStorage.removeItem('user');
    },
};
