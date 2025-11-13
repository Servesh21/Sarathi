/**
 * Goal Progress Card - Visual savings pot/goal tracker
 * Motivational progress display with clear action button
 */
import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Typography, Spacing, Radius } from '@/constants/theme';
import { useColorScheme } from '@/hooks/use-color-scheme';

interface GoalProgressCardProps {
  goalName: string;
  currentAmount: number;
  targetAmount: number;
  icon?: keyof typeof Ionicons.glyphMap;
  onAddFunds?: () => void;
}

export function GoalProgressCard({
  goalName,
  currentAmount,
  targetAmount,
  icon = 'umbrella',
  onAddFunds,
}: GoalProgressCardProps) {
  const colorScheme = useColorScheme();
  const colors = Colors[colorScheme ?? 'light'];

  const progress = Math.min((currentAmount / targetAmount) * 100, 100);
  const remaining = Math.max(targetAmount - currentAmount, 0);

  return (
    <View style={[styles.card, { backgroundColor: colors.backgroundCard }]}>
      <View style={styles.header}>
        <View style={[styles.iconCircle, { backgroundColor: colors.primary + '15' }]}>
          <Ionicons name={icon} size={28} color={colors.primary} />
        </View>
        <View style={styles.headerText}>
          <Text style={[styles.goalName, { color: colors.text }]}>{goalName}</Text>
          <Text style={[styles.remaining, { color: colors.textSecondary }]}>
            ₹{remaining.toLocaleString()} left to reach goal
          </Text>
        </View>
      </View>

      {/* Large progress bar */}
      <View style={styles.progressSection}>
        <View style={[styles.progressTrack, { backgroundColor: colors.backgroundSecondary }]}>
          <View
            style={[
              styles.progressFill,
              { backgroundColor: colors.primary, width: `${progress}%` },
            ]}
          />
        </View>
        <View style={styles.amountRow}>
          <Text style={[styles.currentAmount, { color: colors.primary }]}>
            ₹{currentAmount.toLocaleString()}
          </Text>
          <Text style={[styles.targetAmount, { color: colors.textLight }]}>
            ₹{targetAmount.toLocaleString()}
          </Text>
        </View>
      </View>

      {/* Action button */}
      <TouchableOpacity
        style={[styles.actionButton, { backgroundColor: colors.action }]}
        onPress={onAddFunds}
        activeOpacity={0.8}
      >
        <Text style={[styles.actionText, { color: colors.textInverse }]}>Add to Goal</Text>
        <Ionicons name="add-circle" size={20} color={colors.textInverse} />
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    borderRadius: Radius.lg,
    padding: Spacing.lg,
    gap: Spacing.lg,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.md,
  },
  iconCircle: {
    width: 56,
    height: 56,
    borderRadius: Radius.full,
    justifyContent: 'center',
    alignItems: 'center',
  },
  headerText: {
    flex: 1,
    gap: Spacing.xs,
  },
  goalName: {
    fontSize: Typography.xl,
    fontWeight: '700',
  },
  remaining: {
    fontSize: Typography.sm,
  },
  progressSection: {
    gap: Spacing.sm,
  },
  progressTrack: {
    height: 16,
    borderRadius: Radius.full,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    borderRadius: Radius.full,
  },
  amountRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  currentAmount: {
    fontSize: Typography.xxl,
    fontWeight: '800',
  },
  targetAmount: {
    fontSize: Typography.lg,
    fontWeight: '600',
  },
  actionButton: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: Spacing.sm,
    paddingVertical: Spacing.md,
    borderRadius: Radius.md,
  },
  actionText: {
    fontSize: Typography.lg,
    fontWeight: '700',
  },
});