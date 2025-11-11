import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
  Alert,
} from 'react-native';
import { useAuth } from '../hooks/useAuth';
import { useNavigation } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import type { RootStackParamList } from '../navigation/AppNavigator';

type LoginScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'Login'>;

export default function LoginScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [isRegister, setIsRegister] = useState(false);
  
  const { login, register, isLoading } = useAuth();
  const navigation = useNavigation<LoginScreenNavigationProp>();

  const handleSubmit = async () => {
    if (!email || !password || (isRegister && !fullName)) {
      Alert.alert('Error', 'Please fill in all fields');
      return;
    }

    try {
      if (isRegister) {
        await register(email, password, fullName);
      } else {
        await login(email, password);
      }
      navigation.replace('Main');
    } catch (error: any) {
      Alert.alert('Error', error.response?.data?.detail || 'Authentication failed');
    }
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      className="flex-1 bg-gradient-to-br from-primary-500 to-primary-700"
    >
      <View className="flex-1 justify-center px-6">
        {/* Logo/Title */}
        <View className="items-center mb-10">
          <Text className="text-5xl mb-2">🚗</Text>
          <Text className="text-4xl font-bold text-white mb-2">Sarathi</Text>
          <Text className="text-lg text-white/80">Your Driving Companion</Text>
        </View>

        {/* Form */}
        <View className="bg-white rounded-3xl p-6 shadow-2xl">
          <Text className="text-2xl font-bold text-gray-800 mb-6 text-center">
            {isRegister ? 'Create Account' : 'Welcome Back'}
          </Text>

          {isRegister && (
            <View className="mb-4">
              <Text className="text-sm font-medium text-gray-700 mb-2">Full Name</Text>
              <TextInput
                className="bg-gray-100 rounded-xl px-4 py-3 text-base"
                placeholder="Enter your full name"
                value={fullName}
                onChangeText={setFullName}
                autoCapitalize="words"
              />
            </View>
          )}

          <View className="mb-4">
            <Text className="text-sm font-medium text-gray-700 mb-2">Email</Text>
            <TextInput
              className="bg-gray-100 rounded-xl px-4 py-3 text-base"
              placeholder="Enter your email"
              value={email}
              onChangeText={setEmail}
              keyboardType="email-address"
              autoCapitalize="none"
            />
          </View>

          <View className="mb-6">
            <Text className="text-sm font-medium text-gray-700 mb-2">Password</Text>
            <TextInput
              className="bg-gray-100 rounded-xl px-4 py-3 text-base"
              placeholder="Enter your password"
              value={password}
              onChangeText={setPassword}
              secureTextEntry
            />
          </View>

          <TouchableOpacity
            className="bg-primary-500 rounded-xl py-4 mb-4 active:bg-primary-600"
            onPress={handleSubmit}
            disabled={isLoading}
          >
            <Text className="text-white text-center text-lg font-bold">
              {isLoading ? 'Loading...' : isRegister ? 'Sign Up' : 'Sign In'}
            </Text>
          </TouchableOpacity>

          <TouchableOpacity onPress={() => setIsRegister(!isRegister)}>
            <Text className="text-center text-primary-600 text-sm">
              {isRegister ? 'Already have an account? Sign In' : "Don't have an account? Sign Up"}
            </Text>
          </TouchableOpacity>
        </View>
      </View>
    </KeyboardAvoidingView>
  );
}
