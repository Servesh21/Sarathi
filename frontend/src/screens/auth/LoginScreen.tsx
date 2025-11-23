import React, { useState } from 'react';
import { View, Text, KeyboardAvoidingView, Platform, SafeAreaView, Image } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useAuthStore } from '../../store/authStore';
import { Input, Button, Card } from '../../components';

export default function LoginScreen({ navigation }: any) {
    const [phone, setPhone] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const { login, isLoading, error } = useAuthStore();

    const handleLogin = async () => {
        try {
            await login(phone, password);
        } catch (err) {
            console.error('Login error:', err);
        }
    };

    return (
        <SafeAreaView className="flex-1">
            <LinearGradient
                colors={['#10b981', '#059669', '#047857']}
                className="flex-1"
            >
                <KeyboardAvoidingView
                    behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
                    className="flex-1"
                >
                    <View className="flex-1 justify-center px-6">
                        {/* Logo and Brand */}
                        <View className="items-center mb-12">
                            <View className="bg-white/20 rounded-full p-6 mb-4">
                                <Ionicons name="car-sport" size={48} color="white" />
                            </View>
                            <Text className="text-4xl font-bold text-white mb-2">Sarathi</Text>
                            <Text className="text-lg text-green-100 text-center">
                                Your Autonomous Resilience Agent
                            </Text>
                            <Text className="text-green-200 text-center mt-2">
                                Empowering drivers with smart financial insights
                            </Text>
                        </View>

                        {/* Login Card */}
                        <Card className="bg-white/95 backdrop-blur-sm">
                            <Text className="text-2xl font-bold text-gray-900 text-center mb-6">
                                Welcome Back
                            </Text>

                            {error && (
                                <View className="bg-red-50 border border-red-200 rounded-xl p-4 mb-4 flex-row items-center">
                                    <Ionicons name="alert-circle" size={20} color="#dc2626" />
                                    <Text className="text-red-700 ml-2 flex-1">{error}</Text>
                                </View>
                            )}

                            <Input
                                label="Phone Number"
                                placeholder="Enter your phone number"
                                value={phone}
                                onChangeText={setPhone}
                                keyboardType="phone-pad"
                                autoCapitalize="none"
                                leftIcon="call-outline"
                            />

                            <Input
                                label="Password"
                                placeholder="Enter your password"
                                value={password}
                                onChangeText={setPassword}
                                secureTextEntry={!showPassword}
                                leftIcon="lock-closed-outline"
                                rightIcon={showPassword ? "eye-off-outline" : "eye-outline"}
                                onRightIconPress={() => setShowPassword(!showPassword)}
                            />

                            <Button
                                title="Sign In"
                                onPress={handleLogin}
                                loading={isLoading}
                                className="mt-2"
                                icon="log-in-outline"
                            />

                            <View className="flex-row items-center justify-center mt-6">
                                <Text className="text-gray-600">Don't have an account? </Text>
                                <Button
                                    title="Register"
                                    onPress={() => navigation.navigate('Register')}
                                    variant="outline"
                                    size="sm"
                                />
                            </View>
                        </Card>

                        {/* Features Preview */}
                        <View className="mt-8 space-y-3">
                            <View className="flex-row items-center">
                                <View className="bg-white/20 rounded-full p-2 mr-3">
                                    <Ionicons name="analytics" size={16} color="white" />
                                </View>
                                <Text className="text-green-100">Track earnings and optimize routes</Text>
                            </View>
                            <View className="flex-row items-center">
                                <View className="bg-white/20 rounded-full p-2 mr-3">
                                    <Ionicons name="shield-checkmark" size={16} color="white" />
                                </View>
                                <Text className="text-green-100">Vehicle health monitoring</Text>
                            </View>
                            <View className="flex-row items-center">
                                <View className="bg-white/20 rounded-full p-2 mr-3">
                                    <Ionicons name="trending-up" size={16} color="white" />
                                </View>
                                <Text className="text-green-100">AI-powered financial advice</Text>
                            </View>
                        </View>
                    </View>
                </KeyboardAvoidingView>
            </LinearGradient>
        </SafeAreaView>
    );
}
