import { create } from 'zustand';
import { authAPI, User } from '../api/auth';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface AuthState {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    error: string | null;

    login: (phone_number: string, password: string) => Promise<void>;
    register: (data: any) => Promise<void>;
    logout: () => Promise<void>;
    loadUser: () => Promise<void>;
    updateProfile: (data: Partial<User>) => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
    user: null,
    isAuthenticated: false,
    isLoading: false,
    error: null,

    login: async (phone_number: string, password: string) => {
        set({ isLoading: true, error: null });
        try {
            const user = await authAPI.login({ phone_number, password });
            set({ user, isAuthenticated: true, isLoading: false });
        } catch (error: any) {
            const detail = error.response?.data?.detail;
            const errorMessage = Array.isArray(detail)
                ? detail.map((e: any) => e.msg).join(', ')
                : (typeof detail === 'string' ? detail : 'Login failed');

            set({
                error: errorMessage,
                isLoading: false
            });
            throw error;
        }
    },

    register: async (data: any) => {
        set({ isLoading: true, error: null });
        try {
            await authAPI.register(data);
            set({ isLoading: false });
        } catch (error: any) {
            const detail = error.response?.data?.detail;
            const errorMessage = Array.isArray(detail)
                ? detail.map((e: any) => e.msg).join(', ')
                : (typeof detail === 'string' ? detail : 'Registration failed');

            set({
                error: errorMessage,
                isLoading: false
            });
            throw error;
        }
    },

    logout: async () => {
        await authAPI.logout();
        set({ user: null, isAuthenticated: false });
    },

    loadUser: async () => {
        set({ isLoading: true });
        try {
            const storedUser = await AsyncStorage.getItem('user');
            const token = await AsyncStorage.getItem('authToken');

            if (storedUser && token) {
                // Verify token is still valid
                const user = await authAPI.getCurrentUser();
                set({ user, isAuthenticated: true, isLoading: false });
            } else {
                set({ isLoading: false });
            }
        } catch (error) {
            set({ isLoading: false, isAuthenticated: false, user: null });
        }
    },

    updateProfile: async (data: Partial<User>) => {
        set({ isLoading: true, error: null });
        try {
            const user = await authAPI.updateProfile(data);
            set({ user, isLoading: false });
        } catch (error: any) {
            const detail = error.response?.data?.detail;
            const errorMessage = Array.isArray(detail)
                ? detail.map((e: any) => e.msg).join(', ')
                : (typeof detail === 'string' ? detail : 'Update failed');

            set({
                error: errorMessage,
                isLoading: false
            });
            throw error;
        }
    },
}));
