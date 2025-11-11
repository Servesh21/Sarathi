import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { authAPI } from '../services/api';

interface User {
  id: number;
  email: string;
  full_name: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName: string) => Promise<void>;
  logout: () => Promise<void>;
  loadUser: () => Promise<void>;
}

export const useAuth = create<AuthState>((set) => ({
  user: null,
  token: null,
  isLoading: false,
  isAuthenticated: false,

  login: async (email: string, password: string) => {
    try {
      set({ isLoading: true });
      const data = await authAPI.login(email, password);
      await AsyncStorage.setItem('authToken', data.access_token);
      
      // Fetch user profile
      const user = await authAPI.getProfile();
      
      set({
        user,
        token: data.access_token,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },

  register: async (email: string, password: string, fullName: string) => {
    try {
      set({ isLoading: true });
      const data = await authAPI.register(email, password, fullName);
      await AsyncStorage.setItem('authToken', data.access_token);
      
      // Fetch user profile
      const user = await authAPI.getProfile();
      
      set({
        user,
        token: data.access_token,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },

  logout: async () => {
    await AsyncStorage.removeItem('authToken');
    set({
      user: null,
      token: null,
      isAuthenticated: false,
    });
  },

  loadUser: async () => {
    try {
      const token = await AsyncStorage.getItem('authToken');
      if (token) {
        const user = await authAPI.getProfile();
        set({
          user,
          token,
          isAuthenticated: true,
        });
      }
    } catch (error) {
      // Token invalid, clear storage
      await AsyncStorage.removeItem('authToken');
    }
  },
}));
