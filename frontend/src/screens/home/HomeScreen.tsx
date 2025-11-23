import React, { useEffect } from 'react';
import { View, Text, ScrollView, ActivityIndicator, SafeAreaView } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useAuthStore } from '../../store/authStore';
import { useTripsStore } from '../../store/tripsStore';
import { useFinancialStore } from '../../store/financialStore';
import { Card, Button, StatCard } from '../../components';

export default function HomeScreen({ navigation }: any) {
    const { user } = useAuthStore();
    const { stats, fetchStats, isLoading: tripsLoading } = useTripsStore();
    const { surplus, fetchSurplus, isLoading: financialLoading } = useFinancialStore();

    useEffect(() => {
        fetchStats(30);
        fetchSurplus();
    }, []);

    if (tripsLoading || financialLoading) {
        return (
            <View className="flex-1 justify-center items-center bg-gray-50">
                <ActivityIndicator size="large" color="#10b981" />
            </View>
        );
    }

    return (
        <SafeAreaView className="flex-1 bg-gray-50">
            {/* Header with Gradient */}
            <LinearGradient
                colors={['#10b981', '#059669']}
                className="px-4 pt-4 pb-8"
            >
                <View className="flex-row items-center justify-between">
                    <View className="flex-1">
                        <Text className="text-white text-2xl font-bold">Welcome back!</Text>
                        <Text className="text-green-100 mt-1">{user?.name}</Text>
                    </View>
                    <View className="bg-white/20 rounded-full p-3">
                        <Ionicons name="notifications-outline" size={24} color="white" />
                    </View>
                </View>
            </LinearGradient>

            <ScrollView className="flex-1 -mt-4" showsVerticalScrollIndicator={false}>
                <View className="px-4 pb-6">
                    {/* Quick Stats Grid */}
                    <View className="flex-row mb-6 -mt-2 space-x-3">
                        <View className="flex-1">
                            <StatCard
                                title="Total Trips"
                                value={stats?.total_trips || 0}
                                subtitle="Last 30 days"
                                icon="car-outline"
                                iconColor="#3b82f6"
                                gradientColors={['#dbeafe', '#ffffff']}
                                onPress={() => navigation.navigate('Trips')}
                            />
                        </View>
                        <View className="flex-1">
                            <StatCard
                                title="Earnings"
                                value={`₹${stats?.total_earnings?.toFixed(0) || '0'}`}
                                subtitle={`₹${stats?.average_trip_earnings?.toFixed(0) || '0'}/trip`}
                                icon="wallet-outline"
                                iconColor="#10b981"
                                gradientColors={['#d1fae5', '#ffffff']}
                                trend="up"
                                trendValue="12%"
                            />
                        </View>
                    </View>

                    {/* Main Action Cards */}
                    <Card
                        title="Earnings Engine"
                        subtitle="Track and optimize your income"
                        icon="trending-up"
                        iconColor="#10b981"
                        className="mb-4"
                    >
                        <View className="flex-row justify-between items-center mb-3">
                            <View>
                                <Text className="text-sm text-gray-600">This Month</Text>
                                <Text className="text-2xl font-bold text-gray-900">
                                    ₹{stats?.total_earnings?.toFixed(0) || '0'}
                                </Text>
                            </View>
                            <View className="items-end">
                                <Text className="text-sm text-gray-600">Average/Trip</Text>
                                <Text className="text-lg font-semibold text-green-600">
                                    ₹{stats?.average_trip_earnings?.toFixed(0) || '0'}
                                </Text>
                            </View>
                        </View>
                        <Button
                            title="Log New Trip"
                            onPress={() => navigation.navigate('AddTrip')}
                            icon="add"
                            variant="primary"
                        />
                    </Card>

                    {/* Vehicle Health Card */}
                    <Card
                        title="Resilience Shield"
                        subtitle="Vehicle health monitoring & alerts"
                        icon="car-sport-outline"
                        iconColor="#f59e0b"
                        className="mb-4"
                    >
                        <View className="flex-row items-center mb-4">
                            <View className="bg-green-100 rounded-full p-2 mr-3">
                                <Ionicons name="checkmark-circle" size={20} color="#10b981" />
                            </View>
                            <View>
                                <Text className="font-semibold text-gray-900">Vehicle Status: Good</Text>
                                <Text className="text-sm text-gray-600">Last checked: Today</Text>
                            </View>
                        </View>
                        <Button
                            title="Check Vehicle Health"
                            onPress={() => navigation.navigate('Vehicle')}
                            variant="warning"
                            icon="settings-outline"
                        />
                    </Card>

                    {/* Growth Engine Card */}
                    {surplus && (
                        <Card
                            title="Growth Engine"
                            subtitle="Investment and savings tracking"
                            icon="analytics-outline"
                            iconColor="#3b82f6"
                            className="mb-4"
                        >
                            <View className="space-y-2 mb-4">
                                <View className="flex-row justify-between">
                                    <Text className="text-gray-600">Monthly Surplus</Text>
                                    <Text className="font-bold text-green-600">
                                        ₹{surplus.monthly_surplus?.toFixed(0)}
                                    </Text>
                                </View>
                                <View className="flex-row justify-between">
                                    <Text className="text-gray-600">Savings Rate</Text>
                                    <Text className="font-semibold text-blue-600">
                                        {surplus.surplus_percentage?.toFixed(1)}%
                                    </Text>
                                </View>
                            </View>
                            <Button
                                title="View Investment Options"
                                onPress={() => navigation.navigate('Investments')}
                                variant="outline"
                                icon="trending-up"
                            />
                        </Card>
                    )}

                    {/* AI Chat Card */}
                    <LinearGradient
                        colors={['#8b5cf6', '#7c3aed']}
                        className="rounded-2xl p-5 mb-4"
                    >
                        <View className="flex-row items-center mb-3">
                            <View className="bg-white/20 rounded-full p-3 mr-3">
                                <Ionicons name="chatbubbles" size={24} color="white" />
                            </View>
                            <View className="flex-1">
                                <Text className="text-white text-lg font-bold">Sarathi AI Assistant</Text>
                                <Text className="text-purple-100 text-sm">Your personal finance advisor</Text>
                            </View>
                        </View>
                        <Text className="text-purple-100 mb-4">
                            Get personalized advice for earnings optimization, vehicle maintenance, and investment planning.
                        </Text>
                        <Button
                            title="Start Conversation"
                            onPress={() => navigation.navigate('Chat')}
                            variant="secondary"
                            icon="chatbubble-ellipses-outline"
                        />
                    </LinearGradient>
                </View>
            </ScrollView>
        </SafeAreaView>
    );
}
