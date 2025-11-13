/**
 * Dashboard - Main "Command Center" Screen
 * Answers "Am I okay right now?" in one second
 * 
 * Structure:
 * 1. Today's Net Profit (Hero)
 * 2. Resilience Shield (Health + Vehicle)
 * 3. Growth Engine (Primary Goal)
 */
import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  View,
  Text,
  ScrollView,
  RefreshControl,
  Platform,
  StatusBar,
} from 'react-native';
import { Colors, Typography, Spacing, Radius } from '@/constants/theme';
import { useColorScheme } from '@/hooks/use-color-scheme';
import { VoiceFAB } from '@/components/voice-fab';
import { HealthMeter } from '@/components/health-meter';
import { VehicleHealthCard } from '@/components/vehicle-health-card';
import { GoalProgressCard } from '@/components/goal-progress-card';
import { useRouter } from 'expo-router';

export default function DashboardScreen() {
  const colorScheme = useColorScheme();
  const colors = Colors[colorScheme ?? 'light'];
  const router = useRouter();
  const [refreshing, setRefreshing] = useState(false);

  // Mock data - replace with real API calls
  const [dashboardData, setDashboardData] = useState({
    todayNet: 1430,
    todayEarned: 1850,
    todaySpent: 420,
    health: {
      riskLevel: 'moderate' as const,
      daysSinceRest: 9,
      consecutiveWorkDays: 9,
    },
    vehicle: {
      status: 'due-soon' as const,
      kmSinceService: 3400,
      kmUntilService: 600,
    },
    primaryGoal: {
      name: 'Monsoon Emergency Fund',
      current: 2100,
      target: 5000,
      icon: 'umbrella' as const,
    },
  });

  const onRefresh = async () => {
    setRefreshing(true);
    // TODO: Fetch fresh data from API
    setTimeout(() => setRefreshing(false), 1500);
  };

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <StatusBar barStyle={colorScheme === 'dark' ? 'light-content' : 'dark-content'} />
      
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={colors.primary} />
        }
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <View style={styles.header}>
          <Text style={[styles.greeting, { color: colors.textSecondary }]}>
            {getGreeting()}
          </Text>
          <Text style={[styles.brandName, { color: colors.primary }]}>Sarathi</Text>
        </View>

        {/* TODAY'S NET PROFIT - Hero Section */}
        <View style={[styles.netCard, { backgroundColor: colors.primary }]}>
          <Text style={[styles.netLabel, { color: colors.textInverse + 'CC' }]}>
            Today's Net Profit
          </Text>
          <Text style={[styles.netAmount, { color: colors.textInverse }]}>
            ₹{dashboardData.todayNet.toLocaleString()}
          </Text>
          <View style={styles.netBreakdown}>
            <View style={styles.breakdownItem}>
              <Text style={[styles.breakdownLabel, { color: colors.textInverse + 'CC' }]}>
                Total Earned
              </Text>
              <Text style={[styles.breakdownValue, { color: colors.textInverse }]}>
                ₹{dashboardData.todayEarned.toLocaleString()}
              </Text>
            </View>
            <View style={[styles.divider, { backgroundColor: colors.textInverse + '30' }]} />
            <View style={styles.breakdownItem}>
              <Text style={[styles.breakdownLabel, { color: colors.textInverse + 'CC' }]}>
                Total Spent
              </Text>
              <Text style={[styles.breakdownValue, { color: colors.textInverse }]}>
                ₹{dashboardData.todaySpent.toLocaleString()}
              </Text>
            </View>
          </View>
        </View>

        {/* RESILIENCE SHIELD */}
        <View style={styles.section}>
          <Text style={[styles.sectionTitle, { color: colors.text }]}>Resilience Shield</Text>
          
          {/* Health Meter */}
          <View style={[styles.healthCard, { backgroundColor: colors.backgroundCard }]}>
            <HealthMeter
              riskLevel={dashboardData.health.riskLevel}
              daysSinceRest={dashboardData.health.daysSinceRest}
              consecutiveWorkDays={dashboardData.health.consecutiveWorkDays}
            />
          </View>

          {/* Vehicle Health */}
          <VehicleHealthCard
            serviceStatus={dashboardData.vehicle.status}
            kmSinceService={dashboardData.vehicle.kmSinceService}
            kmUntilService={dashboardData.vehicle.kmUntilService}
            onFindMechanic={() => router.push('/garage')}
          />
        </View>

        {/* GROWTH ENGINE */}
        <View style={styles.section}>
          <Text style={[styles.sectionTitle, { color: colors.text }]}>Growth Engine</Text>
          <GoalProgressCard
            goalName={dashboardData.primaryGoal.name}
            currentAmount={dashboardData.primaryGoal.current}
            targetAmount={dashboardData.primaryGoal.target}
            icon={dashboardData.primaryGoal.icon}
            onAddFunds={() => router.push('/goals')}
          />
        </View>

        {/* Bottom spacing for FAB */}
        <View style={styles.fabSpacer} />
      </ScrollView>

      {/* Persistent Voice FAB */}
      <VoiceFAB />
    </View>
  );
}

// Helper function for time-based greeting
function getGreeting(): string {
  const hour = new Date().getHours();
  if (hour < 12) return 'Good Morning';
  if (hour < 17) return 'Good Afternoon';
  if (hour < 21) return 'Good Evening';
  return 'Drive Safe Tonight';
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: Spacing.lg,
    paddingTop: Platform.OS === 'ios' ? 60 : Spacing.lg,
  },
  header: {
    marginBottom: Spacing.xl,
  },
  greeting: {
    fontSize: Typography.md,
    marginBottom: Spacing.xs,
  },
  brandName: {
    fontSize: Typography.xxl,
    fontWeight: '800',
  },
  netCard: {
    borderRadius: Radius.xl,
    padding: Spacing.xl,
    marginBottom: Spacing.xl,
    elevation: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
  },
  netLabel: {
    fontSize: Typography.md,
    marginBottom: Spacing.xs,
  },
  netAmount: {
    fontSize: Typography.hero,
    fontWeight: '900',
    marginBottom: Spacing.lg,
  },
  netBreakdown: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
  },
  breakdownItem: {
    flex: 1,
    alignItems: 'center',
  },
  divider: {
    width: 1,
    height: 40,
  },
  breakdownLabel: {
    fontSize: Typography.sm,
    marginBottom: Spacing.xs,
  },
  breakdownValue: {
    fontSize: Typography.xl,
    fontWeight: '700',
  },
  section: {
    marginBottom: Spacing.xl,
    gap: Spacing.md,
  },
  sectionTitle: {
    fontSize: Typography.xl,
    fontWeight: '700',
  },
  healthCard: {
    borderRadius: Radius.lg,
    padding: Spacing.lg,
  },
  fabSpacer: {
    height: 100, // Space for FAB
  },
});
