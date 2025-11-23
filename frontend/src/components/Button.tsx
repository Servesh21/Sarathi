import React from 'react';
import { TouchableOpacity, Text, ActivityIndicator, ViewStyle } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

type ButtonVariant = 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'outline';
type ButtonSize = 'sm' | 'md' | 'lg';

interface ButtonProps {
    title: string;
    onPress: () => void;
    variant?: ButtonVariant;
    size?: ButtonSize;
    loading?: boolean;
    disabled?: boolean;
    icon?: keyof typeof Ionicons.glyphMap;
    className?: string;
    style?: ViewStyle;
}

export default function Button({
    title,
    onPress,
    variant = 'primary',
    size = 'md',
    loading = false,
    disabled = false,
    icon,
    className = '',
    style
}: ButtonProps) {
    const getVariantStyles = () => {
        switch (variant) {
            case 'primary':
                return 'bg-primary-500 border-primary-500';
            case 'secondary':
                return 'bg-gray-100 border-gray-200';
            case 'success':
                return 'bg-green-500 border-green-500';
            case 'warning':
                return 'bg-orange-500 border-orange-500';
            case 'danger':
                return 'bg-red-500 border-red-500';
            case 'outline':
                return 'bg-transparent border-primary-500 border-2';
            default:
                return 'bg-primary-500 border-primary-500';
        }
    };

    const getSizeStyles = () => {
        switch (size) {
            case 'sm':
                return 'py-2 px-4';
            case 'md':
                return 'py-3 px-6';
            case 'lg':
                return 'py-4 px-8';
            default:
                return 'py-3 px-6';
        }
    };

    const getTextColor = () => {
        if (variant === 'secondary') return 'text-gray-700';
        if (variant === 'outline') return 'text-primary-500';
        return 'text-white';
    };

    const getTextSize = () => {
        switch (size) {
            case 'sm':
                return 'text-sm';
            case 'md':
                return 'text-base';
            case 'lg':
                return 'text-lg';
            default:
                return 'text-base';
        }
    };

    return (
        <TouchableOpacity
            onPress={onPress}
            disabled={disabled || loading}
            className={`rounded-xl items-center justify-center border ${getVariantStyles()} ${getSizeStyles()} ${disabled ? 'opacity-50' : ''} ${className}`}
            style={style}
        >
            {loading ? (
                <ActivityIndicator
                    size="small"
                    color={variant === 'secondary' || variant === 'outline' ? '#10b981' : '#ffffff'}
                />
            ) : (
                <Text className={`font-semibold ${getTextColor()} ${getTextSize()}`}>
                    {icon && (
                        <Ionicons
                            name={icon}
                            size={size === 'sm' ? 16 : size === 'lg' ? 20 : 18}
                            color={variant === 'secondary' ? '#374151' : variant === 'outline' ? '#10b981' : '#ffffff'}
                        />
                    )}
                    {icon ? ' ' : ''}{title}
                </Text>
            )}
        </TouchableOpacity>
    );
}