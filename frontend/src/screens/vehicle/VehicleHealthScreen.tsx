import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, Alert, SafeAreaView, Image, ActivityIndicator } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';
import { useVehiclesStore } from '../../store/vehiclesStore';
import { Card, Button, StatCard } from '../../components';

export default function VehicleHealthScreen() {
    const { vehicles, healthChecks, selectedVehicle, fetchVehicles, fetchHealthChecks, uploadHealthCheckImages, isLoading } = useVehiclesStore();
    const [selectedImages, setSelectedImages] = useState<any[]>([]);

    useEffect(() => {
        fetchVehicles();
    }, []);

    useEffect(() => {
        if (selectedVehicle) {
            fetchHealthChecks(selectedVehicle.id);
        }
    }, [selectedVehicle]);

    const latestCheck = healthChecks.length > 0 ? healthChecks[0] : null;
    const getBatteryScore = () => {
        if (!latestCheck?.battery_health) return 0;
        if (latestCheck.battery_health === 'good') return 85;
        if (latestCheck.battery_health === 'fair') return 70;
        return 50;
    };
    const getEngineScore = () => latestCheck?.engine_oil_level === 'good' ? 90 : 70;
    const getBrakeScore = () => latestCheck?.brake_condition === 'good' ? 85 : 70;
    const getTireScore = () => latestCheck?.tire_condition === 'good' ? 88 : 70;

    const pickImages = async () => {
        const permission = await ImagePicker.requestMediaLibraryPermissionsAsync();
        if (!permission.granted) {
            Alert.alert('Permission required', 'Please grant photo library permission');
            return;
        }

        const result = await ImagePicker.launchImageLibraryAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.Images,
            allowsMultipleSelection: true,
            quality: 0.8,
        });

        if (!result.canceled && result.assets) {
            setSelectedImages(result.assets);
        }
    };

    const handleUpload = async () => {
        if (!selectedVehicle || selectedImages.length === 0) {
            Alert.alert('Error', 'Please select at least one image');
            return;
        }

        const formData = new FormData();
        selectedImages.forEach((image, idx) => {
            formData.append('images', {
                uri: image.uri,
                type: 'image/jpeg',
                name: `vehicle_${idx}.jpg`,
            } as any);
        });

        try {
            await uploadHealthCheckImages(selectedVehicle.id, formData);
            setSelectedImages([]);
            Alert.alert('Success', 'Vehicle diagnostics completed!');
        } catch (err) {
            Alert.alert('Error', 'Failed to analyze vehicle images');
        }
    };

    const getHealthColor = (score: number) => {
        if (score >= 85) return '#10b981';
        if (score >= 70) return '#f59e0b';
        return '#ef4444';
    };

    return (
        <SafeAreaView className="flex-1 bg-gray-50">
            {/* Header */}
            <LinearGradient
                colors={['#f59e0b', '#d97706']}
                className="px-4 pt-4 pb-8"
            >
                <View className="flex-row items-center justify-between">
                    <View className="flex-1">
                        <Text className="text-white text-2xl font-bold">Resilience Shield</Text>
                        <Text className="text-orange-100 mt-1">AI-powered vehicle diagnostics</Text>
                    </View>
                    <View className="bg-white/20 rounded-full p-3">
                        <Ionicons name="shield-checkmark" size={24} color="white" />
                    </View>
                </View>
            </LinearGradient>

            <ScrollView className="flex-1 -mt-4" showsVerticalScrollIndicator={false}>
                <View className="px-4 pb-6">
                    {/* Overall Health Status */}
                    <LinearGradient
                        colors={latestCheck && !latestCheck.immediate_action_required ? ['#d1fae5', '#10b981'] : ['#fee2e2', '#ef4444']}
                        className="rounded-2xl p-5 mb-6 -mt-2"
                    >
                        <View className="flex-row items-center justify-between">
                            <View>
                                <Text className="text-white text-xl font-bold">Vehicle Health</Text>
                                <Text className="text-white text-lg">
                                    {latestCheck ? (latestCheck.immediate_action_required ? 'Needs Attention' : 'Good Condition') : 'No Data'}
                                </Text>
                            </View>
                            <View className="bg-white/30 rounded-full p-4">
                                <Ionicons
                                    name={latestCheck && !latestCheck.immediate_action_required ? "checkmark-circle" : "alert-circle"}
                                    size={32}
                                    color="white"
                                />
                            </View>
                        </View>
                        <View className="flex-row justify-between mt-4">
                            <Text className="text-white opacity-90">
                                Last Check: {latestCheck ? new Date(latestCheck.created_at).toLocaleDateString() : 'Never'}
                            </Text>
                        </View>
                    </LinearGradient>

                    {/* Health Metrics Grid */}
                    <View className="flex-row flex-wrap justify-between mb-6">
                        <View className="w-[48%] mb-3">
                            <StatCard
                                title="Battery Health"
                                value={latestCheck?.battery_health || 'N/A'}
                                icon="battery-charging"
                                iconColor={getHealthColor(getBatteryScore())}
                                gradientColors={['#f3f4f6', '#ffffff']}
                            />
                        </View>
                        <View className="w-[48%] mb-3">
                            <StatCard
                                title="Engine Oil"
                                value={latestCheck?.engine_oil_level || 'N/A'}
                                icon="car-sport"
                                iconColor={getHealthColor(getEngineScore())}
                                gradientColors={['#f3f4f6', '#ffffff']}
                            />
                        </View>
                        <View className="w-[48%]">
                            <StatCard
                                title="Brake System"
                                value={latestCheck?.brake_condition || 'N/A'}
                                icon="disc"
                                iconColor={getHealthColor(getBrakeScore())}
                                gradientColors={['#f3f4f6', '#ffffff']}
                            />
                        </View>
                        <View className="w-[48%]">
                            <StatCard
                                title="Tire Condition"
                                value={latestCheck?.tire_condition || 'N/A'}
                                icon="ellipse"
                                iconColor={getHealthColor(getTireScore())}
                                gradientColors={['#f3f4f6', '#ffffff']}
                            />
                        </View>
                    </View>

                    {/* AI Diagnostics Card */}
                    <Card
                        title="AI Diagnostics"
                        subtitle="Upload vehicle images for instant analysis"
                        icon="camera-outline"
                        iconColor="#3b82f6"
                        className="mb-6"
                    >
                        <View className="bg-blue-50 rounded-xl p-4 mb-4">
                            <Text className="text-blue-900 font-medium mb-2">📸 What to photograph:</Text>
                            <View className="space-y-1">
                                <Text className="text-blue-800">• Engine bay and components</Text>
                                <Text className="text-blue-800">• Tire tread and sidewalls</Text>
                                <Text className="text-blue-800">• Dashboard warning lights</Text>
                                <Text className="text-blue-800">• Exterior body damage</Text>
                            </View>
                        </View>

                        {selectedImages.length > 0 && (
                            <View className="mb-4">
                                <Text className="font-medium text-gray-900 mb-2">Selected Images ({selectedImages.length})</Text>
                                <ScrollView horizontal showsHorizontalScrollIndicator={false}>
                                    {selectedImages.map((image, idx) => (
                                        <View key={idx} className="mr-2">
                                            <Image
                                                source={{ uri: image.uri }}
                                                className="w-20 h-20 rounded-lg"
                                            />
                                        </View>
                                    ))}
                                </ScrollView>
                            </View>
                        )}

                        <View className="space-y-3">
                            <Button
                                title={`Select Images${selectedImages.length > 0 ? ` (${selectedImages.length})` : ''}`}
                                onPress={pickImages}
                                variant="outline"
                                icon="camera"
                            />

                            {selectedImages.length > 0 && (
                                <Button
                                    title="Analyze Vehicle"
                                    onPress={handleUpload}
                                    loading={isLoading}
                                    icon="analytics"
                                />
                            )}
                        </View>
                    </Card>

                    {/* Maintenance Reminders */}
                    <Card
                        title="Maintenance Schedule"
                        subtitle="Stay on top of regular service"
                        icon="calendar-outline"
                        iconColor="#8b5cf6"
                        className="mb-6"
                    >
                        <View className="space-y-3">
                            <View className="flex-row items-center justify-between bg-gray-50 rounded-xl p-3">
                                <View className="flex-row items-center">
                                    <View className="bg-blue-100 rounded-full p-2 mr-3">
                                        <Ionicons name="calendar" size={16} color="#3b82f6" />
                                    </View>
                                    <View>
                                        <Text className="font-medium text-gray-900">Regular Service</Text>
                                        <Text className="text-sm text-gray-600">Schedule your next check</Text>
                                    </View>
                                </View>
                            </View>
                        </View>
                    </Card>

                    {/* Recent Health Checks */}
                    {healthChecks.length > 0 && (
                        <View className="mb-6">
                            <Text className="text-xl font-bold text-gray-900 mb-4">Recent Diagnostics</Text>
                            {healthChecks.slice(0, 3).map((check) => (
                                <Card key={check.id} className="mb-3">
                                    <View className="flex-row justify-between items-start mb-3">
                                        <View>
                                            <Text className="font-semibold text-gray-900">
                                                {check.check_type}
                                            </Text>
                                            <Text className="text-sm text-gray-600">
                                                {new Date(check.created_at).toLocaleDateString()}
                                            </Text>
                                        </View>
                                        <View className="bg-green-100 rounded-full px-3 py-1">
                                            <Text className="text-green-800 font-bold text-sm">
                                                {check.severity_score || 0}/100
                                            </Text>
                                        </View>
                                    </View>

                                    {check.ai_analysis && (
                                        <Text className="text-gray-700 mb-3">{check.ai_analysis}</Text>
                                    )}

                                    {check.recommendations && (
                                        <View className="bg-blue-50 rounded-xl p-3">
                                            <Text className="font-medium text-blue-900 mb-2">Recommendations:</Text>
                                            <Text className="text-blue-800 text-sm">{check.recommendations}</Text>
                                        </View>
                                    )}

                                    {check.immediate_action_required && (
                                        <View className="bg-red-50 border-l-4 border-red-500 p-3 mt-3">
                                            <View className="flex-row items-center">
                                                <Ionicons name="warning" size={20} color="#ef4444" />
                                                <Text className="text-red-700 font-semibold ml-2">Immediate Action Required</Text>
                                            </View>
                                        </View>
                                    )}
                                </Card>
                            ))}
                        </View>
                    )}

                    {healthChecks.length === 0 && (
                        <Card className="items-center py-8">
                            <View className="bg-gray-100 rounded-full p-4 mb-4">
                                <Ionicons name="camera-outline" size={32} color="#6b7280" />
                            </View>
                            <Text className="text-lg font-semibold text-gray-900 mb-2">No health checks yet</Text>
                            <Text className="text-gray-600 text-center mb-4">
                                Upload vehicle images to get AI-powered diagnostics and maintenance insights
                            </Text>
                            <Button
                                title="Start Vehicle Check"
                                onPress={pickImages}
                                icon="camera"
                            />
                        </Card>
                    )}
                </View>
            </ScrollView>
        </SafeAreaView>
    );
}
