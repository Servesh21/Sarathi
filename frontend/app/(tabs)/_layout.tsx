import { Tabs, router } from 'expo-router';
import React, { useEffect } from 'react';

import { HapticTab } from '@/components/haptic-tab';
import { IconSymbol } from '@/components/ui/icon-symbol';
import { Colors } from '@/constants/theme';
import { useColorScheme } from '@/hooks/use-color-scheme';
import { useAuthStore } from '../../src/stores/authStore';
import { useAlertsStore } from '@/src/stores/alertsStore';

export default function TabLayout() {
  const colorScheme = useColorScheme();
  const { isAuthenticated } = useAuthStore();
  const { unreadCount } = useAlertsStore();

  useEffect(() => {
    if (!isAuthenticated) {
      router.replace('/auth');
    }
  }, [isAuthenticated]);

  if (!isAuthenticated) {
    return null;
  }

  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: '#0ea5e9',
        tabBarInactiveTintColor: '#6b7280',
        headerShown: false,
        tabBarButton: HapticTab,
        tabBarStyle: {
          backgroundColor: 'white',
          borderTopWidth: 1,
          borderTopColor: '#e5e7eb',
        },
      }}>
      <Tabs.Screen
        name="index"
        options={{
          title: 'Dashboard',
          tabBarIcon: ({ color }) => <IconSymbol size={24} name="house.fill" color={color} />,
        }}
      />
      <Tabs.Screen
        name="garage"
        options={{
          title: 'Garage',
          tabBarIcon: ({ color }) => <IconSymbol size={24} name="car.fill" color={color} />,
        }}
      />
      <Tabs.Screen
        name="goals"
        options={{
          title: 'Goals',
          tabBarIcon: ({ color }) => <IconSymbol size={24} name="target" color={color} />,
        }}
      />
      <Tabs.Screen
        name="notifications"
        options={{
          title: 'Alerts',
          tabBarIcon: ({ color }) => <IconSymbol size={24} name="bell.fill" color={color} />,
          tabBarBadge: unreadCount > 0 ? unreadCount : undefined,
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Profile',
          tabBarIcon: ({ color }) => <IconSymbol size={24} name="person.fill" color={color} />,
        }}
      />
    </Tabs>
  );
}
