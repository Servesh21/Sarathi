import React from 'react';
import { View, Text, TouchableOpacity, ScrollView } from 'react-native';
import { useAuthStore } from '../../store/authStore';

export default function ProfileScreen({ navigation }: any) {
    const { user, logout } = useAuthStore();

    const handleLogout = async () => {
        await logout();
    };

    return (
        <ScrollView className="flex-1 bg-gray-50">
            <View className="px-4 py-6">
                <View className="bg-white rounded-2xl p-6 mb-6 shadow-sm">
                    <View className="items-center mb-6">
                        <View className="w-24 h-24 bg-primary rounded-full justify-center items-center mb-4">
                            <Text className="text-white text-4xl">{user?.name?.charAt(0) || 'U'}</Text>
                        </View>
                        <Text className="text-2xl font-bold text-gray-900">{user?.name}</Text>
                        <Text className="text-gray-600">{user?.phone_number}</Text>
                    </View>

                    <View className="space-y-3">
                        <View className="flex-row justify-between py-2">
                            <Text className="text-gray-600">City</Text>
                            <Text className="font-semibold text-gray-900">{user?.city || 'Not set'}</Text>
                        </View>
                        <View className="flex-row justify-between py-2">
                            <Text className="text-gray-600">Vehicle Type</Text>
                            <Text className="font-semibold text-gray-900">{user?.vehicle_type || 'Not set'}</Text>
                        </View>
                        <View className="flex-row justify-between py-2">
                            <Text className="text-gray-600">Member Since</Text>
                            <Text className="font-semibold text-gray-900">
                                {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
                            </Text>
                        </View>
                    </View>
                </View>

                <View className="bg-white rounded-xl p-4 mb-6 shadow-sm">
                    <Text className="text-lg font-semibold text-gray-900 mb-4">App Settings</Text>

                    <TouchableOpacity className="py-3 border-b border-gray-200">
                        <Text className="text-gray-700">Edit Profile</Text>
                    </TouchableOpacity>

                    <TouchableOpacity className="py-3 border-b border-gray-200">
                        <Text className="text-gray-700">Notifications</Text>
                    </TouchableOpacity>

                    <TouchableOpacity className="py-3 border-b border-gray-200">
                        <Text className="text-gray-700">Language Preferences</Text>
                    </TouchableOpacity>

                    <TouchableOpacity className="py-3">
                        <Text className="text-gray-700">Privacy & Security</Text>
                    </TouchableOpacity>
                </View>

                <TouchableOpacity
                    className="bg-red-500 rounded-xl py-4"
                    onPress={handleLogout}
                >
                    <Text className="text-white text-center font-semibold text-lg">Logout</Text>
                </TouchableOpacity>

                <Text className="text-gray-500 text-center mt-6 text-sm">
                    Sarathi v1.0.0 • Autonomous Resilience Agent
                </Text>
            </View>
        </ScrollView>
    );
}
