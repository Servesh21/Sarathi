import React, { useEffect } from 'react';
import { View, Text, ScrollView, ActivityIndicator, SafeAreaView, FlatList } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useTripsStore } from '../../store/tripsStore';
import { Card, Button, StatCard } from '../../components';

export default function TripsScreen({ navigation }: any) {
    const { trips, stats, zoneRecommendations, fetchTrips, fetchStats, fetchZoneRecommendations, isLoading } = useTripsStore();

    useEffect(() => {
        fetchTrips(30);
        fetchStats(30);
        fetchZoneRecommendations();
    }, []);

    if (isLoading && trips.length === 0) {
        return (
            <View className="flex-1 justify-center items-center bg-gray-50">
                <ActivityIndicator size="large" color="#10b981" />
            </View>
        );
    }

    const renderTripItem = ({ item }: { item: any }) => (
        <Card className="mb-3">
            <View className="flex-row justify-between items-start">
                <View className="flex-1">
                    <View className="flex-row items-center mb-2">
                        <View className="bg-green-100 rounded-full p-2 mr-3">
                            <Ionicons name="checkmark-circle" size={16} color="#10b981" />
                        </View>
                        <Text className="font-semibold text-gray-900">Trip #{item.id}</Text>
                    </View>
                    <Text className="text-sm text-gray-600 mb-1">
                        {item.pickup_location} → {item.drop_location}
                    </Text>
                    <Text className="text-xs text-gray-500">
                        {new Date(item.trip_date).toLocaleDateString()} • {item.distance_km}km
                    </Text>
                </View>
                <View className="items-end">
                    <Text className="text-lg font-bold text-green-600">₹{item.fare_amount}</Text>
                    <Text className="text-xs text-gray-500">
                        ₹{(item.fare_amount / item.distance_km).toFixed(1)}/km
                    </Text>
                </View>
            </View>
        </Card>
    );

    return (
        <SafeAreaView className="flex-1 bg-gray-50">
            {/* Header */}
            <LinearGradient
                colors={['#10b981', '#059669']}
                className="px-4 pt-4 pb-8"
            >
                <View className="flex-row items-center justify-between">
                    <View className="flex-1">
                        <Text className="text-white text-2xl font-bold">Earnings Engine</Text>
                        <Text className="text-green-100 mt-1">Track your income & optimize</Text>
                    </View>
                    <Button
                        title="Add Trip"
                        onPress={() => navigation.navigate('AddTrip')}
                        variant="secondary"
                        size="sm"
                        icon="add"
                    />
                </View>
            </LinearGradient>

            <ScrollView className="flex-1 -mt-4" showsVerticalScrollIndicator={false}>
                <View className="px-4 pb-6">
                    {/* Stats Grid */}
                    {stats && (
                        <View className="flex-row flex-wrap justify-between mb-6 -mt-2">
                            <View className="w-[48%] mb-3">
                                <StatCard
                                    title="Total Trips"
                                    value={stats.total_trips}
                                    subtitle="Last 30 days"
                                    icon="car-outline"
                                    iconColor="#3b82f6"
                                    gradientColors={['#dbeafe', '#ffffff']}
                                />
                            </View>
                            <View className="w-[48%] mb-3">
                                <StatCard
                                    title="Total Earnings"
                                    value={`₹${stats.total_earnings?.toFixed(0) || '0'}`}
                                    subtitle="This month"
                                    icon="wallet-outline"
                                    iconColor="#10b981"
                                    gradientColors={['#d1fae5', '#ffffff']}
                                    trend="up"
                                    trendValue="8%"
                                />
                            </View>
                            <View className="w-[48%]">
                                <StatCard
                                    title="Avg per Trip"
                                    value={`₹${stats.average_trip_earnings?.toFixed(0) || '0'}`}
                                    subtitle="Per journey"
                                    icon="trending-up-outline"
                                    iconColor="#f59e0b"
                                    gradientColors={['#fef3c7', '#ffffff']}
                                />
                            </View>
                            <View className="w-[48%]">
                                <StatCard
                                    title="High Value Trips"
                                    value={stats.high_value_trips || 0}
                                    subtitle="Premium rides"
                                    icon="star-outline"
                                    iconColor="#8b5cf6"
                                    gradientColors={['#ede9fe', '#ffffff']}
                                />
                            </View>
                        </View>
                    )}

                    {/* Zone Recommendations */}
                    {zoneRecommendations.length > 0 && (
                        <LinearGradient
                            colors={['#fef3c7', '#fbbf24']}
                            className="rounded-2xl p-5 mb-6"
                        >
                            <View className="flex-row items-center mb-3">
                                <View className="bg-white/30 rounded-full p-2 mr-3">
                                    <Ionicons name="flame" size={20} color="#d97706" />
                                </View>
                                <Text className="text-lg font-bold text-orange-900">High Demand Zones</Text>
                            </View>
                            <View className="space-y-2">
                                {zoneRecommendations.slice(0, 3).map((zone, idx) => (
                                    <View key={idx} className="bg-white/50 rounded-xl p-3 flex-row justify-between items-center">
                                        <View>
                                            <Text className="font-semibold text-orange-900">{zone.zone_name}</Text>
                                            <Text className="text-sm text-orange-700">
                                                Confidence: {(zone.confidence_score * 100).toFixed(0)}%
                                            </Text>
                                        </View>
                                        <Text className="font-bold text-green-700">₹{zone.expected_earnings}</Text>
                                    </View>
                                ))}
                            </View>
                        </LinearGradient>
                    )}

                    {/* Recent Trips */}
                    <View className="mb-6">
                        <View className="flex-row justify-between items-center mb-4">
                            <Text className="text-xl font-bold text-gray-900">Recent Trips</Text>
                            <Text className="text-sm text-gray-600">{trips.length} trips</Text>
                        </View>

                        {trips.length > 0 ? (
                            <FlatList
                                data={trips}
                                renderItem={renderTripItem}
                                keyExtractor={(item) => item.id.toString()}
                                scrollEnabled={false}
                                showsVerticalScrollIndicator={false}
                            />
                        ) : (
                            <Card className="items-center py-8">
                                <View className="bg-gray-100 rounded-full p-4 mb-4">
                                    <Ionicons name="car-outline" size={32} color="#6b7280" />
                                </View>
                                <Text className="text-lg font-semibold text-gray-900 mb-2">No trips yet</Text>
                                <Text className="text-gray-600 text-center mb-4">
                                    Start logging your trips to track earnings and get insights
                                </Text>
                                <Button
                                    title="Log Your First Trip"
                                    onPress={() => navigation.navigate('AddTrip')}
                                    icon="add"
                                />
                            </Card>
                        )}
                    </View>
                </View>
            </ScrollView>
        </SafeAreaView>
    );
}
