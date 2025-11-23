import React from 'react';
import { View, Text, TouchableOpacity, ViewStyle } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface CardProps {
    title?: string;
    subtitle?: string;
    children: React.ReactNode;
    onPress?: () => void;
    className?: string;
    style?: ViewStyle;
    icon?: keyof typeof Ionicons.glyphMap;
    iconColor?: string;
}

export default function Card({
    title,
    subtitle,
    children,
    onPress,
    className = '',
    style,
    icon,
    iconColor = '#10b981'
}: CardProps) {
    const Component = onPress ? TouchableOpacity : View;

    return (
        <Component
            onPress={onPress}
            className={`bg-white rounded-2xl p-5 shadow-sm border border-gray-100 ${className}`}
            style={style}
        >
            {(title || icon) && (
                <View className="flex-row items-center mb-4">
                    {icon && (
                        <Ionicons
                            name={icon}
                            size={24}
                            color={iconColor}
                            style={{ marginRight: 12 }}
                        />
                    )}
                    <View className="flex-1">
                        {title && (
                            <Text className="text-lg font-semibold text-gray-900">{title}</Text>
                        )}
                        {subtitle && (
                            <Text className="text-sm text-gray-600 mt-1">{subtitle}</Text>
                        )}
                    </View>
                </View>
            )}
            {children}
        </Component>
    );
}