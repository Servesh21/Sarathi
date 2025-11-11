import React from 'react';
import {
    View,
    Text,
    ScrollView,
    TouchableOpacity,
    Alert,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useAuthStore } from '../../src/stores/authStore';
import { router } from 'expo-router';

export default function ProfileScreen() {
    const { user, logout } = useAuthStore();

    const handleLogout = async () => {
        Alert.alert(
            'Logout',
            'Are you sure you want to logout?',
            [
                { text: 'Cancel', style: 'cancel' },
                {
                    text: 'Logout',
                    style: 'destructive',
                    onPress: async () => {
                        await logout();
                        router.replace('/auth');
                    },
                },
            ]
        );
    };

    const profileItems = [
        { icon: '👤', title: 'Edit Profile', subtitle: 'Update your personal information' },
        { icon: '🚗', title: 'Driving Preferences', subtitle: 'Set your driving style and preferences' },
        { icon: '🔔', title: 'Notifications', subtitle: 'Manage your notification settings' },
        { icon: '🔒', title: 'Privacy & Security', subtitle: 'Control your privacy and security settings' },
        { icon: '📊', title: 'Data & Analytics', subtitle: 'View your driving data and insights' },
        { icon: '💳', title: 'Subscription', subtitle: 'Manage your premium features' },
        { icon: '❓', title: 'Help & Support', subtitle: 'Get help and contact support' },
        { icon: '⚙️', title: 'Settings', subtitle: 'App settings and preferences' },
    ];

    return (
        <View style={{ flex: 1, backgroundColor: '#f9fafb' }}>
            <LinearGradient
                colors={['#0ea5e9', '#3b82f6']}
                style={{ paddingTop: 60, paddingBottom: 30, paddingHorizontal: 20 }}
            >
                <View style={{ alignItems: 'center' }}>
                    <View style={{
                        width: 80,
                        height: 80,
                        borderRadius: 40,
                        backgroundColor: 'rgba(255,255,255,0.2)',
                        alignItems: 'center',
                        justifyContent: 'center',
                        marginBottom: 16,
                    }}>
                        <Text style={{ fontSize: 32, color: 'white' }}>
                            {user?.name?.charAt(0) || 'U'}
                        </Text>
                    </View>
                    <Text style={{ color: 'white', fontSize: 24, fontWeight: 'bold', marginBottom: 4 }}>
                        {user?.name || 'User'}
                    </Text>
                    <Text style={{ color: 'rgba(255,255,255,0.9)', fontSize: 16 }}>
                        {user?.email || 'user@example.com'}
                    </Text>
                </View>
            </LinearGradient>

            <ScrollView style={{ flex: 1, padding: 20 }}>
                <View style={{
                    backgroundColor: 'white',
                    borderRadius: 16,
                    marginBottom: 20,
                    shadowColor: '#000',
                    shadowOffset: { width: 0, height: 2 },
                    shadowOpacity: 0.1,
                    shadowRadius: 4,
                    elevation: 3,
                }}>
                    <View style={{ padding: 20, alignItems: 'center' }}>
                        <Text style={{ fontSize: 20, fontWeight: 'bold', color: '#1f2937', marginBottom: 16 }}>
                            Quick Stats
                        </Text>
                        <View style={{ flexDirection: 'row', justifyContent: 'space-around', width: '100%' }}>
                            <View style={{ alignItems: 'center' }}>
                                <Text style={{ fontSize: 24, fontWeight: 'bold', color: '#0ea5e9' }}>1,245</Text>
                                <Text style={{ color: '#6b7280', fontSize: 14 }}>Miles</Text>
                            </View>
                            <View style={{ alignItems: 'center' }}>
                                <Text style={{ fontSize: 24, fontWeight: 'bold', color: '#10b981' }}>45</Text>
                                <Text style={{ color: '#6b7280', fontSize: 14 }}>Trips</Text>
                            </View>
                            <View style={{ alignItems: 'center' }}>
                                <Text style={{ fontSize: 24, fontWeight: 'bold', color: '#f59e0b' }}>98%</Text>
                                <Text style={{ color: '#6b7280', fontSize: 14 }}>Safety</Text>
                            </View>
                        </View>
                    </View>
                </View>

                <View style={{
                    backgroundColor: 'white',
                    borderRadius: 16,
                    marginBottom: 20,
                    shadowColor: '#000',
                    shadowOffset: { width: 0, height: 2 },
                    shadowOpacity: 0.1,
                    shadowRadius: 4,
                    elevation: 3,
                }}>
                    {profileItems.map((item, index) => (
                        <TouchableOpacity
                            key={index}
                            style={{
                                flexDirection: 'row',
                                alignItems: 'center',
                                padding: 16,
                                borderBottomWidth: index < profileItems.length - 1 ? 1 : 0,
                                borderBottomColor: '#f3f4f6',
                            }}
                        >
                            <Text style={{ fontSize: 24, marginRight: 16 }}>{item.icon}</Text>
                            <View style={{ flex: 1 }}>
                                <Text style={{ fontSize: 16, fontWeight: '600', color: '#374151', marginBottom: 2 }}>
                                    {item.title}
                                </Text>
                                <Text style={{ fontSize: 14, color: '#6b7280' }}>
                                    {item.subtitle}
                                </Text>
                            </View>
                            <Text style={{ color: '#9ca3af', fontSize: 18 }}>›</Text>
                        </TouchableOpacity>
                    ))}
                </View>

                <TouchableOpacity
                    style={{
                        backgroundColor: 'white',
                        borderRadius: 16,
                        padding: 16,
                        marginBottom: 40,
                        shadowColor: '#000',
                        shadowOffset: { width: 0, height: 2 },
                        shadowOpacity: 0.1,
                        shadowRadius: 4,
                        elevation: 3,
                    }}
                    onPress={handleLogout}
                >
                    <View style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'center' }}>
                        <Text style={{ fontSize: 20, marginRight: 12 }}>🚪</Text>
                        <Text style={{ fontSize: 16, fontWeight: '600', color: '#ef4444' }}>
                            Logout
                        </Text>
                    </View>
                </TouchableOpacity>
            </ScrollView>
        </View>
    );
}