import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';

interface StatCardProps {
    title: string;
    value: string | number;
    subtitle?: string;
    icon: keyof typeof Ionicons.glyphMap;
    iconColor?: string;
    gradientColors?: string[];
    onPress?: () => void;
    trend?: 'up' | 'down' | 'neutral';
    trendValue?: string;
}

export default function StatCard({
    title,
    value,
    subtitle,
    icon,
    iconColor = '#10b981',
    gradientColors = ['#ffffff', '#f9fafb'],
    onPress,
    trend,
    trendValue
}: StatCardProps) {
    const Component = onPress ? TouchableOpacity : View;

    const getTrendIcon = () => {
        switch (trend) {
            case 'up':
                return 'trending-up';
            case 'down':
                return 'trending-down';
            default:
                return 'remove';
        }
    };

    const getTrendColor = () => {
        switch (trend) {
            case 'up':
                return '#10b981';
            case 'down':
                return '#ef4444';
            default:
                return '#6b7280';
        }
    };

    return (
        <Component onPress={onPress}>
            <LinearGradient
                colors={gradientColors}
                className="rounded-2xl p-5 shadow-sm border border-gray-100"
            >
                <View className="flex-row items-start justify-between mb-3">
                    <View className="bg-gray-100 rounded-xl p-3">
                        <Ionicons name={icon} size={24} color={iconColor} />
                    </View>
                    {trend && trendValue && (
                        <View className="flex-row items-center">
                            <Ionicons
                                name={getTrendIcon() as keyof typeof Ionicons.glyphMap}
                                size={16}
                                color={getTrendColor()}
                            />
                            <Text className="text-sm font-medium ml-1" style={{ color: getTrendColor() }}>
                                {trendValue}
                            </Text>
                        </View>
                    )}
                </View>

                <Text className="text-3xl font-bold text-gray-900 mb-1">{value}</Text>
                <Text className="text-gray-600 font-medium">{title}</Text>
                {subtitle && (
                    <Text className="text-sm text-gray-500 mt-1">{subtitle}</Text>
                )}
            </LinearGradient>
        </Component>
    );
}