import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';

export interface User {
    id: string;
    email: string;
    name: string;
    profilePicture?: string;
}

interface AuthState {
    user: User | null;
    token: string | null;
    isLoading: boolean;
    isAuthenticated: boolean;
    login: (email: string, password: string) => Promise<void>;
    register: (name: string, email: string, password: string) => Promise<void>;
    logout: () => Promise<void>;
    loadUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
    user: null,
    token: null,
    isLoading: false,
    isAuthenticated: false,

    login: async (email: string, password: string) => {
        set({ isLoading: true });
        try {
            // TODO: Replace with actual API call
            const mockResponse = {
                user: { id: '1', email, name: 'John Doe' },
                token: 'mock-jwt-token'
            };
            
            await AsyncStorage.setItem('auth_token', mockResponse.token);
            await AsyncStorage.setItem('user', JSON.stringify(mockResponse.user));
            
            set({ 
                user: mockResponse.user, 
                token: mockResponse.token, 
                isAuthenticated: true,
                isLoading: false 
            });
        } catch (error) {
            set({ isLoading: false });
            throw error;
        }
    },

    register: async (name: string, email: string, password: string) => {
        set({ isLoading: true });
        try {
            // TODO: Replace with actual API call
            const mockResponse = {
                user: { id: '1', email, name },
                token: 'mock-jwt-token'
            };
            
            await AsyncStorage.setItem('auth_token', mockResponse.token);
            await AsyncStorage.setItem('user', JSON.stringify(mockResponse.user));
            
            set({ 
                user: mockResponse.user, 
                token: mockResponse.token, 
                isAuthenticated: true,
                isLoading: false 
            });
        } catch (error) {
            set({ isLoading: false });
            throw error;
        }
    },

    logout: async () => {
        await AsyncStorage.removeItem('auth_token');
        await AsyncStorage.removeItem('user');
        set({ user: null, token: null, isAuthenticated: false });
    },

    loadUser: async () => {
        try {
            const token = await AsyncStorage.getItem('auth_token');
            const userStr = await AsyncStorage.getItem('user');
            
            if (token && userStr) {
                const user = JSON.parse(userStr);
                set({ user, token, isAuthenticated: true });
            }
        } catch (error) {
            console.error('Failed to load user:', error);
        }
    },
}));