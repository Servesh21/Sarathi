/**
 * Health Meter - Wellness-style burnout indicator
 * Green = Rested, Yellow = Moderate, Red = High Risk
 */
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Colors, Typography, Spacing, Radius } from '@/constants/theme';
import { useColorScheme } from '@/hooks/use-color-scheme';

interface HealthMeterProps {
  riskLevel: 'low' | 'moderate' | 'high';
  daysSinceRest: number;
  consecutiveWorkDays: number;
}

export function HealthMeter({ riskLevel, daysSinceRest, consecutiveWorkDays }: HealthMeterProps) {
  const colorScheme = useColorScheme();
  const colors = Colors[colorScheme ?? 'light'];

  const getColor = () => {
    switch (riskLevel) {
      case 'low':
        return colors.success;
      case 'moderate':
        return colors.warning;
      case 'high':
        return colors.danger;
    }
  };

  const getLabel = () => {
    switch (riskLevel) {
      case 'low':
        return 'Rested';
      case 'moderate':
        return 'Watch Out';
      case 'high':
        return 'High Risk';
    }
  };

  const getProgress = () => {
    // 0-7 days = low risk (0-33%)
    // 8-14 days = moderate (34-66%)
    // 15+ days = high risk (67-100%)
    const progress = Math.min((consecutiveWorkDays / 21) * 100, 100);
    return progress;
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={[styles.title, { color: colors.text }]}>My Health</Text>
        <Text style={[styles.status, { color: getColor() }]}>{getLabel()}</Text>
      </View>

      {/* Progress bar */}
      <View style={[styles.progressTrack, { backgroundColor: colors.backgroundCard }]}>
        <View
          style={[styles.progressFill, { backgroundColor: getColor(), width: `${getProgress()}%` }]}
        />
      </View>

      <Text style={[styles.detail, { color: colors.textSecondary }]}>
        {consecutiveWorkDays} consecutive work days • {daysSinceRest} days since rest
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    gap: Spacing.sm,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  title: {
    fontSize: Typography.lg,
    fontWeight: '600',
  },
  status: {
    fontSize: Typography.md,
    fontWeight: '700',
  },
  progressTrack: {
    height: 12,
    borderRadius: Radius.full,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    borderRadius: Radius.full,
  },
  detail: {
    fontSize: Typography.sm,
  },
});