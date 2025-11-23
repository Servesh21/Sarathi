import React, { useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';
import { useAuthStore } from '../store/authStore';

// Import screens (will create next)
import LoginScreen from '../screens/auth/LoginScreen';
import RegisterScreen from '../screens/auth/RegisterScreen';
import HomeScreen from '../screens/home/HomeScreen';
import TripsScreen from '../screens/trips/TripsScreen';
import AddTripScreen from '../screens/trips/AddTripScreen';
import VehicleHealthScreen from '../screens/vehicle/VehicleHealthScreen';
import GoalsScreen from '../screens/goals/GoalsScreen';
import InvestmentsScreen from '../screens/investments/InvestmentsScreen';
import ChatScreen from '../screens/chat/ChatScreen';
import ProfileScreen from '../screens/profile/ProfileScreen';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

function AuthStack() {
    return (
        <Stack.Navigator screenOptions={{ headerShown: false }}>
            <Stack.Screen name="Login" component={LoginScreen} />
            <Stack.Screen name="Register" component={RegisterScreen} />
        </Stack.Navigator>
    );
}

function MainTabs() {
    return (
        <Tab.Navigator
            screenOptions={({ route }) => ({
                tabBarIcon: ({ focused, color, size }) => {
                    let iconName: keyof typeof Ionicons.glyphMap;

                    switch (route.name) {
                        case 'Home':
                            iconName = focused ? 'home' : 'home-outline';
                            break;
                        case 'Trips':
                            iconName = focused ? 'wallet' : 'wallet-outline';
                            break;
                        case 'Vehicle':
                            iconName = focused ? 'car-sport' : 'car-sport-outline';
                            break;
                        case 'Goals':
                            iconName = focused ? 'flag' : 'flag-outline';
                            break;
                        case 'Investments':
                            iconName = focused ? 'trending-up' : 'trending-up-outline';
                            break;
                        default:
                            iconName = 'ellipse-outline';
                    }

                    return <Ionicons name={iconName} size={size} color={color} />;
                },
                tabBarActiveTintColor: '#10b981',
                tabBarInactiveTintColor: '#6b7280',
                headerShown: false,
                tabBarStyle: {
                    backgroundColor: '#ffffff',
                    borderTopWidth: 1,
                    borderTopColor: '#e5e7eb',
                    paddingBottom: 5,
                    paddingTop: 5,
                    height: 60,
                },
                tabBarLabelStyle: {
                    fontSize: 12,
                    fontWeight: '600',
                },
            })}
        >
            <Tab.Screen
                name="Home"
                component={HomeScreen}
                options={{ tabBarLabel: 'Dashboard' }}
            />
            <Tab.Screen
                name="Trips"
                component={TripsScreen}
                options={{ tabBarLabel: 'Earnings' }}
            />
            <Tab.Screen
                name="Vehicle"
                component={VehicleHealthScreen}
                options={{ tabBarLabel: 'Health' }}
            />
            <Tab.Screen
                name="Goals"
                component={GoalsScreen}
                options={{ tabBarLabel: 'Goals' }}
            />
            <Tab.Screen
                name="Investments"
                component={InvestmentsScreen}
                options={{ tabBarLabel: 'Growth' }}
            />
        </Tab.Navigator>
    );
}

function MainStack() {
    return (
        <Stack.Navigator>
            <Stack.Screen
                name="MainTabs"
                component={MainTabs}
                options={{ headerShown: false }}
            />
            <Stack.Screen name="AddTrip" component={AddTripScreen} />
            <Stack.Screen name="Chat" component={ChatScreen} />
            <Stack.Screen name="Profile" component={ProfileScreen} />
        </Stack.Navigator>
    );
}

export default function AppNavigator() {
    const { isAuthenticated, loadUser } = useAuthStore();

    useEffect(() => {
        loadUser();
    }, [loadUser]);

    return (
        <NavigationContainer>
            {isAuthenticated ? <MainStack /> : <AuthStack />}
        </NavigationContainer>
    );
}
