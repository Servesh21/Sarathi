/**
 * Voice FAB - Floating Action Button for voice-first logging
 * Always visible, instant voice input on tap
 */
import React from 'react';
import { TouchableOpacity, StyleSheet, Alert, Platform } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Radius, Spacing } from '@/constants/theme';
import { useColorScheme } from '@/hooks/use-color-scheme';

interface VoiceFABProps {
  onPress?: () => void;
}

export function VoiceFAB({ onPress }: VoiceFABProps) {
  const colorScheme = useColorScheme();
  const colors = Colors[colorScheme ?? 'light'];

  const handlePress = () => {
    if (onPress) {
      onPress();
    } else {
      // Default behavior - show voice input prompt
      Alert.alert(
        'Voice Logging',
        'Tap and speak to log your trip.\n\nExample: "Zomato, Andheri, 150"',
        [
          { text: 'Cancel', style: 'cancel' },
          { text: 'Start Recording', onPress: () => console.log('Voice recording started') },
        ]
      );
    }
  };

  return (
    <TouchableOpacity
      style={[styles.fab, { backgroundColor: colors.action, shadowColor: colors.primary }]}
      onPress={handlePress}
      activeOpacity={0.8}
    >
      <Ionicons name="mic" size={28} color={colors.textInverse} />
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  fab: {
    position: 'absolute',
    bottom: 20,
    right: 20,
    width: 64,
    height: 64,
    borderRadius: Radius.full,
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 8,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    zIndex: 1000,
  },
});