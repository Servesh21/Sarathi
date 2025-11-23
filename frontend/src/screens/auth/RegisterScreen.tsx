import React, { useState } from 'react';
import { View, Text, KeyboardAvoidingView, Platform, ScrollView, SafeAreaView } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useAuthStore } from '../../store/authStore';
import { Input, Button, Card } from '../../components';

export default function RegisterScreen({ navigation }: any) {
    const [formData, setFormData] = useState({
        name: '',
        phone_number: '',
        password: '',
        confirmPassword: '',
        vehicle_type: 'auto',
        city: '',
    });
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const { register, isLoading, error } = useAuthStore();

    const handleRegister = async () => {
        if (formData.password !== formData.confirmPassword) {
            return;
        }

        try {
            const { confirmPassword, ...registerData } = formData;
            await register(registerData);
            navigation.navigate('Login');
        } catch (err) {
            console.error('Registration error:', err);
        }
    };

    const updateFormData = (field: string, value: string) => {
        setFormData(prev => ({ ...prev, [field]: value }));
    };

    return (
        <SafeAreaView className="flex-1">
            <LinearGradient
                colors={['#10b981', '#059669']}
                className="flex-1"
            >
                <KeyboardAvoidingView
                    behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
                    className="flex-1"
                >
                    <ScrollView className="flex-1" showsVerticalScrollIndicator={false}>
                        <View className="px-6 py-8">
                            {/* Header */}
                            <View className="items-center mb-8">
                                <View className="bg-white/20 rounded-full p-4 mb-4">
                                    <Ionicons name="person-add" size={32} color="white" />
                                </View>
                                <Text className="text-3xl font-bold text-white mb-2">Join Sarathi</Text>
                                <Text className="text-green-100 text-center">
                                    Start your journey towards financial resilience
                                </Text>
                            </View>

                            {/* Registration Form */}
                            <Card className="bg-white/95 backdrop-blur-sm">
                                <Text className="text-xl font-bold text-gray-900 text-center mb-6">
                                    Create Your Account
                                </Text>

                                {error && (
                                    <View className="bg-red-50 border border-red-200 rounded-xl p-4 mb-4 flex-row items-center">
                                        <Ionicons name="alert-circle" size={20} color="#dc2626" />
                                        <Text className="text-red-700 ml-2 flex-1">{error}</Text>
                                    </View>
                                )}

                                <Input
                                    label="Full Name"
                                    placeholder="Enter your full name"
                                    value={formData.name}
                                    onChangeText={(text) => updateFormData('name', text)}
                                    leftIcon="person-outline"
                                />

                                <Input
                                    label="Phone Number"
                                    placeholder="Enter your phone number"
                                    value={formData.phone_number}
                                    onChangeText={(text) => updateFormData('phone_number', text)}
                                    keyboardType="phone-pad"
                                    leftIcon="call-outline"
                                />

                                <Input
                                    label="City"
                                    placeholder="Enter your city"
                                    value={formData.city}
                                    onChangeText={(text) => updateFormData('city', text)}
                                    leftIcon="location-outline"
                                />

                                <Input
                                    label="Password"
                                    placeholder="Create a password"
                                    value={formData.password}
                                    onChangeText={(text) => updateFormData('password', text)}
                                    secureTextEntry={!showPassword}
                                    leftIcon="lock-closed-outline"
                                    rightIcon={showPassword ? "eye-off-outline" : "eye-outline"}
                                    onRightIconPress={() => setShowPassword(!showPassword)}
                                />

                                <Input
                                    label="Confirm Password"
                                    placeholder="Confirm your password"
                                    value={formData.confirmPassword}
                                    onChangeText={(text) => updateFormData('confirmPassword', text)}
                                    secureTextEntry={!showConfirmPassword}
                                    leftIcon="lock-closed-outline"
                                    rightIcon={showConfirmPassword ? "eye-off-outline" : "eye-outline"}
                                    onRightIconPress={() => setShowConfirmPassword(!showConfirmPassword)}
                                    error={
                                        formData.confirmPassword && formData.password !== formData.confirmPassword
                                            ? "Passwords don't match"
                                            : undefined
                                    }
                                />

                                <Button
                                    title="Create Account"
                                    onPress={handleRegister}
                                    loading={isLoading}
                                    className="mt-2"
                                    icon="person-add-outline"
                                />

                                <View className="flex-row items-center justify-center mt-6">
                                    <Text className="text-gray-600">Already have an account? </Text>
                                    <Button
                                        title="Sign In"
                                        onPress={() => navigation.navigate('Login')}
                                        variant="outline"
                                        size="sm"
                                    />
                                </View>
                            </Card>
                        </View>
                    </ScrollView>
                </KeyboardAvoidingView>
            </LinearGradient>
        </SafeAreaView>
    );
}
