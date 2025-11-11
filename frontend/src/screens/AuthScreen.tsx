import React, { useState } from 'react';
import {
    View,
    Text,
    TextInput,
    TouchableOpacity,
    Alert,
    ScrollView,
    KeyboardAvoidingView,
    Platform,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useAuthStore } from '../stores/authStore';
import { router } from 'expo-router';

export default function AuthScreen() {
    const [isLogin, setIsLogin] = useState(true);
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    const { login, register, isLoading } = useAuthStore();

    const handleSubmit = async () => {
        if (!email || !password) {
            Alert.alert('Error', 'Please fill in all required fields');
            return;
        }

        if (!isLogin) {
            if (!name) {
                Alert.alert('Error', 'Please enter your name');
                return;
            }
            if (password !== confirmPassword) {
                Alert.alert('Error', 'Passwords do not match');
                return;
            }
        }

        try {
            if (isLogin) {
                await login(email, password);
            } else {
                await register(name, email, password);
            }
            router.replace('/(tabs)');
        } catch (error) {
            Alert.alert('Error', 'Authentication failed. Please try again.');
        }
    };

    return (
        <LinearGradient
            colors={['#0ea5e9', '#3b82f6']}
            style={{ flex: 1 }}
        >
            <KeyboardAvoidingView
                style={{ flex: 1 }}
                behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
            >
                <ScrollView contentContainerStyle={{ flexGrow: 1, justifyContent: 'center', padding: 20 }}>
                    <View style={{ backgroundColor: 'white', borderRadius: 20, padding: 30, shadowColor: '#000', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.1, shadowRadius: 10, elevation: 5 }}>
                        <Text style={{ fontSize: 32, fontWeight: 'bold', textAlign: 'center', marginBottom: 10, color: '#1f2937' }}>
                            Sarathi
                        </Text>
                        <Text style={{ fontSize: 16, textAlign: 'center', marginBottom: 30, color: '#6b7280' }}>
                            Your AI-Powered Driving Companion
                        </Text>

                        {!isLogin && (
                            <View style={{ marginBottom: 16 }}>
                                <Text style={{ fontSize: 16, fontWeight: '600', marginBottom: 8, color: '#374151' }}>
                                    Full Name
                                </Text>
                                <TextInput
                                    style={{ borderWidth: 1, borderColor: '#d1d5db', borderRadius: 12, padding: 16, fontSize: 16, backgroundColor: '#f9fafb' }}
                                    value={name}
                                    onChangeText={setName}
                                    placeholder="Enter your full name"
                                    autoCapitalize="words"
                                />
                            </View>
                        )}

                        <View style={{ marginBottom: 16 }}>
                            <Text style={{ fontSize: 16, fontWeight: '600', marginBottom: 8, color: '#374151' }}>
                                Email Address
                            </Text>
                            <TextInput
                                style={{ borderWidth: 1, borderColor: '#d1d5db', borderRadius: 12, padding: 16, fontSize: 16, backgroundColor: '#f9fafb' }}
                                value={email}
                                onChangeText={setEmail}
                                placeholder="Enter your email"
                                keyboardType="email-address"
                                autoCapitalize="none"
                            />
                        </View>

                        <View style={{ marginBottom: 16 }}>
                            <Text style={{ fontSize: 16, fontWeight: '600', marginBottom: 8, color: '#374151' }}>
                                Password
                            </Text>
                            <TextInput
                                style={{ borderWidth: 1, borderColor: '#d1d5db', borderRadius: 12, padding: 16, fontSize: 16, backgroundColor: '#f9fafb' }}
                                value={password}
                                onChangeText={setPassword}
                                placeholder="Enter your password"
                                secureTextEntry
                            />
                        </View>

                        {!isLogin && (
                            <View style={{ marginBottom: 24 }}>
                                <Text style={{ fontSize: 16, fontWeight: '600', marginBottom: 8, color: '#374151' }}>
                                    Confirm Password
                                </Text>
                                <TextInput
                                    style={{ borderWidth: 1, borderColor: '#d1d5db', borderRadius: 12, padding: 16, fontSize: 16, backgroundColor: '#f9fafb' }}
                                    value={confirmPassword}
                                    onChangeText={setConfirmPassword}
                                    placeholder="Confirm your password"
                                    secureTextEntry
                                />
                            </View>
                        )}

                        <TouchableOpacity
                            style={{ backgroundColor: '#0ea5e9', borderRadius: 12, padding: 16, marginBottom: 16, opacity: isLoading ? 0.7 : 1 }}
                            onPress={handleSubmit}
                            disabled={isLoading}
                        >
                            <Text style={{ color: 'white', fontSize: 18, fontWeight: 'bold', textAlign: 'center' }}>
                                {isLoading ? 'Please wait...' : (isLogin ? 'Sign In' : 'Create Account')}
                            </Text>
                        </TouchableOpacity>

                        <TouchableOpacity
                            style={{ paddingVertical: 12 }}
                            onPress={() => setIsLogin(!isLogin)}
                        >
                            <Text style={{ textAlign: 'center', color: '#6b7280', fontSize: 16 }}>
                                {isLogin ? "Don't have an account? " : 'Already have an account? '}
                                <Text style={{ color: '#0ea5e9', fontWeight: '600' }}>
                                    {isLogin ? 'Sign Up' : 'Sign In'}
                                </Text>
                            </Text>
                        </TouchableOpacity>
                    </View>
                </ScrollView>
            </KeyboardAvoidingView>
        </LinearGradient>
    );
}