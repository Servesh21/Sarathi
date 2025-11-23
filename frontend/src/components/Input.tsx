import React from 'react';
import { View, Text, TextInput, TextInputProps } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface InputProps extends TextInputProps {
    label?: string;
    error?: string;
    leftIcon?: keyof typeof Ionicons.glyphMap;
    rightIcon?: keyof typeof Ionicons.glyphMap;
    onRightIconPress?: () => void;
    containerClassName?: string;
}

export default function Input({
    label,
    error,
    leftIcon,
    rightIcon,
    onRightIconPress,
    containerClassName = '',
    className = '',
    ...props
}: InputProps) {
    return (
        <View className={`mb-4 ${containerClassName}`}>
            {label && (
                <Text className="text-sm font-medium text-gray-700 mb-2">{label}</Text>
            )}
            <View className="relative">
                {leftIcon && (
                    <View className="absolute left-4 top-3 z-10">
                        <Ionicons name={leftIcon} size={20} color="#6b7280" />
                    </View>
                )}
                <TextInput
                    className={`bg-white border rounded-xl px-4 py-3 text-gray-900 ${leftIcon ? 'pl-12' : ''
                        } ${rightIcon ? 'pr-12' : ''
                        } ${error ? 'border-red-300' : 'border-gray-300'
                        } ${className}`}
                    placeholderTextColor="#9ca3af"
                    {...props}
                />
                {rightIcon && (
                    <View className="absolute right-4 top-3 z-10">
                        <Ionicons
                            name={rightIcon}
                            size={20}
                            color="#6b7280"
                            onPress={onRightIconPress}
                        />
                    </View>
                )}
            </View>
            {error && (
                <Text className="text-red-500 text-sm mt-1">{error}</Text>
            )}
        </View>
    );
}