/**
 * Goals Screen - Financial goal management and tracking
 * Helps drivers save for important financial objectives
 * 
 * Features:
 * 1. Active Goals List with progress tracking
 * 2. Add new goal functionality
 * 3. Quick fund addition to goals
 * 4. Goal completion celebrations
 */
import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  RefreshControl,
  Alert,
  Modal,
  TextInput,
  Platform,
  StatusBar,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Typography, Spacing, Radius } from '@/constants/theme';
import { useColorScheme } from '@/hooks/use-color-scheme';
import { GoalProgressCard } from '@/components/goal-progress-card';
import { LinearGradient } from 'expo-linear-gradient';

interface Goal {
  id: string;
  name: string;
  targetAmount: number;
  currentAmount: number;
  icon: keyof typeof Ionicons.glyphMap;
  category: 'emergency' | 'vehicle' | 'family' | 'health' | 'business' | 'other';
  createdAt: Date;
  targetDate?: Date;
}

interface NewGoalForm {
  name: string;
  targetAmount: string;
  category: Goal['category'];
  icon: keyof typeof Ionicons.glyphMap;
}

const goalCategories = [
  { key: 'emergency' as const, label: 'Emergency Fund', icon: 'umbrella' as const, color: '#ef4444' },
  { key: 'vehicle' as const, label: 'Vehicle & Maintenance', icon: 'car' as const, color: '#3b82f6' },
  { key: 'family' as const, label: 'Family & Education', icon: 'home' as const, color: '#10b981' },
  { key: 'health' as const, label: 'Health & Insurance', icon: 'medical' as const, color: '#f59e0b' },
  { key: 'business' as const, label: 'Business Growth', icon: 'trending-up' as const, color: '#8b5cf6' },
  { key: 'other' as const, label: 'Other Goals', icon: 'star' as const, color: '#6b7280' },
];

export default function GoalsScreen() {
  const colorScheme = useColorScheme();
  const colors = Colors[colorScheme ?? 'light'];
  const [refreshing, setRefreshing] = useState(false);
  const [showAddGoal, setShowAddGoal] = useState(false);
  const [showAddFunds, setShowAddFunds] = useState<string | null>(null);
  const [fundAmount, setFundAmount] = useState('');

  // Mock goals data - replace with real API calls
  const [goals, setGoals] = useState<Goal[]>([
    {
      id: '1',
      name: 'Monsoon Emergency Fund',
      targetAmount: 25000,
      currentAmount: 18500,
      icon: 'umbrella',
      category: 'emergency',
      createdAt: new Date('2024-10-01'),
      targetDate: new Date('2025-06-01'),
    },
    {
      id: '2',
      name: 'Car Service & Repair Fund',
      targetAmount: 15000,
      currentAmount: 8200,
      icon: 'car',
      category: 'vehicle',
      createdAt: new Date('2024-11-01'),
    },
    {
      id: '3',
      name: 'Child School Fees',
      targetAmount: 35000,
      currentAmount: 12000,
      icon: 'school',
      category: 'family',
      createdAt: new Date('2024-09-15'),
      targetDate: new Date('2025-04-01'),
    },
  ]);

  const [newGoal, setNewGoal] = useState<NewGoalForm>({
    name: '',
    targetAmount: '',
    category: 'emergency',
    icon: 'umbrella',
  });

  const onRefresh = React.useCallback(() => {
    setRefreshing(true);
    // Simulate API call
    setTimeout(() => {
      setRefreshing(false);
    }, 1000);
  }, []);

  const handleAddFunds = (goalId: string, amount: number) => {
    setGoals(prev => prev.map(goal => 
      goal.id === goalId 
        ? { ...goal, currentAmount: goal.currentAmount + amount }
        : goal
    ));

    // Check if goal is completed
    const updatedGoal = goals.find(g => g.id === goalId);
    if (updatedGoal && updatedGoal.currentAmount + amount >= updatedGoal.targetAmount) {
      Alert.alert(
        '🎉 Goal Completed!',
        `Congratulations! You've successfully saved ₹${updatedGoal.targetAmount.toLocaleString()} for "${updatedGoal.name}"!`,
        [{ text: 'Celebrate!', style: 'default' }]
      );
    }

    setShowAddFunds(null);
    setFundAmount('');
  };

  const handleCreateGoal = () => {
    if (!newGoal.name.trim() || !newGoal.targetAmount.trim()) {
      Alert.alert('Missing Information', 'Please fill in all required fields.');
      return;
    }

    const targetAmount = parseInt(newGoal.targetAmount.replace(/[^\d]/g, ''));
    if (targetAmount <= 0) {
      Alert.alert('Invalid Amount', 'Please enter a valid target amount.');
      return;
    }

    const goal: Goal = {
      id: Date.now().toString(),
      name: newGoal.name.trim(),
      targetAmount,
      currentAmount: 0,
      icon: newGoal.icon,
      category: newGoal.category,
      createdAt: new Date(),
    };

    setGoals(prev => [...prev, goal]);
    setNewGoal({ name: '', targetAmount: '', category: 'emergency', icon: 'umbrella' });
    setShowAddGoal(false);

    Alert.alert('Goal Created!', `Your goal "${goal.name}" has been created successfully.`);
  };

  const handleCategorySelect = (category: Goal['category']) => {
    const categoryInfo = goalCategories.find(c => c.key === category);
    setNewGoal(prev => ({
      ...prev,
      category,
      icon: categoryInfo?.icon || 'star'
    }));
  };

  const formatCurrency = (amount: string) => {
    const numericAmount = amount.replace(/[^\d]/g, '');
    return numericAmount ? `₹${parseInt(numericAmount).toLocaleString()}` : '';
  };

  const totalSaved = goals.reduce((sum, goal) => sum + goal.currentAmount, 0);
  const totalTarget = goals.reduce((sum, goal) => sum + goal.targetAmount, 0);

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <StatusBar 
        barStyle={colorScheme === 'dark' ? 'light-content' : 'dark-content'}
        backgroundColor={colors.background}
      />

      {/* Header */}
      <LinearGradient
        colors={[colors.primary, colors.primaryLight]}
        style={styles.header}
      >
        <View style={styles.headerContent}>
          <Text style={styles.headerTitle}>Financial Goals</Text>
          <Text style={styles.headerSubtitle}>
            ₹{totalSaved.toLocaleString()} saved of ₹{totalTarget.toLocaleString()}
          </Text>
        </View>
        
        <TouchableOpacity 
          style={styles.addButton}
          onPress={() => setShowAddGoal(true)}
        >
          <Ionicons name="add" size={24} color={colors.textInverse} />
        </TouchableOpacity>
      </LinearGradient>

      {/* Goals List */}
      <ScrollView
        style={styles.content}
        contentContainerStyle={styles.contentContainer}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {goals.length === 0 ? (
          <View style={styles.emptyState}>
            <Ionicons name="flag" size={64} color={colors.textLight} />
            <Text style={[styles.emptyTitle, { color: colors.text }]}>
              No Goals Yet
            </Text>
            <Text style={[styles.emptySubtitle, { color: colors.textSecondary }]}>
              Set your first financial goal to start building your future
            </Text>
            <TouchableOpacity
              style={[styles.emptyButton, { backgroundColor: colors.primary }]}
              onPress={() => setShowAddGoal(true)}
            >
              <Text style={styles.emptyButtonText}>Create Your First Goal</Text>
            </TouchableOpacity>
          </View>
        ) : (
          <>
            {goals.map((goal) => (
              <GoalProgressCard
                key={goal.id}
                goalName={goal.name}
                currentAmount={goal.currentAmount}
                targetAmount={goal.targetAmount}
                icon={goal.icon}
                onAddFunds={() => setShowAddFunds(goal.id)}
              />
            ))}

            {/* Summary Card */}
            <View style={[styles.summaryCard, { backgroundColor: colors.backgroundCard }]}>
              <Text style={[styles.summaryTitle, { color: colors.text }]}>
                Goals Summary
              </Text>
              <View style={styles.summaryStats}>
                <View style={styles.summaryItem}>
                  <Text style={[styles.summaryLabel, { color: colors.textSecondary }]}>
                    Active Goals
                  </Text>
                  <Text style={[styles.summaryValue, { color: colors.primary }]}>
                    {goals.length}
                  </Text>
                </View>
                <View style={styles.summaryItem}>
                  <Text style={[styles.summaryLabel, { color: colors.textSecondary }]}>
                    Total Saved
                  </Text>
                  <Text style={[styles.summaryValue, { color: colors.success }]}>
                    ₹{totalSaved.toLocaleString()}
                  </Text>
                </View>
                <View style={styles.summaryItem}>
                  <Text style={[styles.summaryLabel, { color: colors.textSecondary }]}>
                    Progress
                  </Text>
                  <Text style={[styles.summaryValue, { color: colors.primary }]}>
                    {totalTarget > 0 ? Math.round((totalSaved / totalTarget) * 100) : 0}%
                  </Text>
                </View>
              </View>
            </View>
          </>
        )}
      </ScrollView>

      {/* Add Goal Modal */}
      <Modal visible={showAddGoal} animationType="slide" presentationStyle="pageSheet">
        <View style={[styles.modalContainer, { backgroundColor: colors.background }]}>
          <View style={styles.modalHeader}>
            <TouchableOpacity onPress={() => setShowAddGoal(false)}>
              <Ionicons name="close" size={24} color={colors.text} />
            </TouchableOpacity>
            <Text style={[styles.modalTitle, { color: colors.text }]}>New Goal</Text>
            <TouchableOpacity onPress={handleCreateGoal}>
              <Text style={[styles.modalSave, { color: colors.primary }]}>Save</Text>
            </TouchableOpacity>
          </View>

          <ScrollView style={styles.modalContent}>
            <Text style={[styles.inputLabel, { color: colors.text }]}>Goal Name</Text>
            <TextInput
              style={[styles.textInput, { 
                backgroundColor: colors.backgroundCard,
                borderColor: colors.border,
                color: colors.text 
              }]}
              placeholder="e.g., Emergency Fund, New Vehicle..."
              placeholderTextColor={colors.textLight}
              value={newGoal.name}
              onChangeText={(text) => setNewGoal(prev => ({ ...prev, name: text }))}
            />

            <Text style={[styles.inputLabel, { color: colors.text }]}>Target Amount</Text>
            <TextInput
              style={[styles.textInput, { 
                backgroundColor: colors.backgroundCard,
                borderColor: colors.border,
                color: colors.text 
              }]}
              placeholder="₹25,000"
              placeholderTextColor={colors.textLight}
              value={formatCurrency(newGoal.targetAmount)}
              onChangeText={(text) => setNewGoal(prev => ({ 
                ...prev, 
                targetAmount: text.replace(/[^\d]/g, '') 
              }))}
              keyboardType="numeric"
            />

            <Text style={[styles.inputLabel, { color: colors.text }]}>Category</Text>
            <View style={styles.categoryGrid}>
              {goalCategories.map((category) => (
                <TouchableOpacity
                  key={category.key}
                  style={[
                    styles.categoryItem,
                    { 
                      backgroundColor: colors.backgroundCard,
                      borderColor: newGoal.category === category.key ? category.color : colors.border,
                      borderWidth: newGoal.category === category.key ? 2 : 1,
                    }
                  ]}
                  onPress={() => handleCategorySelect(category.key)}
                >
                  <Ionicons 
                    name={category.icon} 
                    size={24} 
                    color={newGoal.category === category.key ? category.color : colors.textSecondary} 
                  />
                  <Text style={[
                    styles.categoryLabel, 
                    { 
                      color: newGoal.category === category.key ? category.color : colors.textSecondary 
                    }
                  ]}>
                    {category.label}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </ScrollView>
        </View>
      </Modal>

      {/* Add Funds Modal */}
      <Modal visible={showAddFunds !== null} animationType="slide" transparent>
        <View style={styles.fundModalOverlay}>
          <View style={[styles.fundModal, { backgroundColor: colors.backgroundCard }]}>
            <Text style={[styles.fundModalTitle, { color: colors.text }]}>Add Funds</Text>
            <TextInput
              style={[styles.fundInput, { 
                backgroundColor: colors.background,
                borderColor: colors.border,
                color: colors.text 
              }]}
              placeholder="₹500"
              placeholderTextColor={colors.textLight}
              value={formatCurrency(fundAmount)}
              onChangeText={(text) => setFundAmount(text.replace(/[^\d]/g, ''))}
              keyboardType="numeric"
              autoFocus
            />
            <View style={styles.fundModalButtons}>
              <TouchableOpacity 
                style={[styles.fundModalButton, { backgroundColor: colors.border }]}
                onPress={() => {
                  setShowAddFunds(null);
                  setFundAmount('');
                }}
              >
                <Text style={[styles.fundModalButtonText, { color: colors.text }]}>Cancel</Text>
              </TouchableOpacity>
              <TouchableOpacity 
                style={[styles.fundModalButton, { backgroundColor: colors.primary }]}
                onPress={() => {
                  const amount = parseInt(fundAmount);
                  if (amount > 0 && showAddFunds) {
                    handleAddFunds(showAddFunds, amount);
                  }
                }}
                disabled={!fundAmount || parseInt(fundAmount) <= 0}
              >
                <Text style={styles.fundModalButtonTextPrimary}>Add</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    paddingTop: Platform.OS === 'ios' ? 60 : StatusBar.currentHeight! + 20,
    paddingHorizontal: Spacing.lg,
    paddingBottom: Spacing.lg,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  headerContent: {
    flex: 1,
  },
  headerTitle: {
    fontSize: Typography.xxl,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: Spacing.xs,
  },
  headerSubtitle: {
    fontSize: Typography.md,
    color: 'rgba(255, 255, 255, 0.8)',
  },
  addButton: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  content: {
    flex: 1,
  },
  contentContainer: {
    padding: Spacing.lg,
    paddingTop: Spacing.md,
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: Spacing.xl * 2,
  },
  emptyTitle: {
    fontSize: Typography.xl,
    fontWeight: 'bold',
    marginTop: Spacing.lg,
    marginBottom: Spacing.xs,
  },
  emptySubtitle: {
    fontSize: Typography.md,
    textAlign: 'center',
    marginBottom: Spacing.xl,
    paddingHorizontal: Spacing.lg,
  },
  emptyButton: {
    paddingHorizontal: Spacing.lg,
    paddingVertical: Spacing.md,
    borderRadius: Radius.md,
  },
  emptyButtonText: {
    fontSize: Typography.md,
    fontWeight: '600',
    color: '#ffffff',
  },
  summaryCard: {
    marginTop: Spacing.lg,
    padding: Spacing.lg,
    borderRadius: Radius.lg,
  },
  summaryTitle: {
    fontSize: Typography.lg,
    fontWeight: 'bold',
    marginBottom: Spacing.lg,
  },
  summaryStats: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  summaryItem: {
    alignItems: 'center',
  },
  summaryLabel: {
    fontSize: Typography.xs,
    textTransform: 'uppercase',
    marginBottom: Spacing.xs,
  },
  summaryValue: {
    fontSize: Typography.lg,
    fontWeight: 'bold',
  },
  modalContainer: {
    flex: 1,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: Spacing.lg,
    paddingVertical: Spacing.md,
    paddingTop: Platform.OS === 'ios' ? 60 : Spacing.lg,
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
  },
  modalTitle: {
    fontSize: Typography.xl,
    fontWeight: 'bold',
  },
  modalSave: {
    fontSize: Typography.md,
    fontWeight: '600',
  },
  modalContent: {
    flex: 1,
    padding: Spacing.lg,
  },
  inputLabel: {
    fontSize: Typography.xs,
    textTransform: 'uppercase',
    marginBottom: Spacing.xs,
    marginTop: Spacing.lg,
  },
  textInput: {
    fontSize: Typography.md,
    padding: Spacing.md,
    borderRadius: Radius.md,
    borderWidth: 1,
  },
  categoryGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: Spacing.md,
  },
  categoryItem: {
    width: '47%',
    padding: Spacing.md,
    borderRadius: Radius.md,
    alignItems: 'center',
    borderWidth: 1,
  },
  categoryLabel: {
    fontSize: Typography.xs,
    marginTop: Spacing.xs,
    textAlign: 'center',
  },
  fundModalOverlay: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
  },
  fundModal: {
    width: '80%',
    padding: Spacing.lg,
    borderRadius: Radius.lg,
  },
  fundModalTitle: {
    fontSize: Typography.lg,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: Spacing.lg,
  },
  fundInput: {
    fontSize: Typography.xl,
    fontWeight: 'bold',
    textAlign: 'center',
    padding: Spacing.md,
    borderRadius: Radius.md,
    borderWidth: 1,
    marginBottom: Spacing.lg,
  },
  fundModalButtons: {
    flexDirection: 'row',
    gap: Spacing.md,
  },
  fundModalButton: {
    flex: 1,
    padding: Spacing.md,
    borderRadius: Radius.md,
    alignItems: 'center',
  },
  fundModalButtonText: {
    fontSize: Typography.md,
    fontWeight: '600',
  },
  fundModalButtonTextPrimary: {
    fontSize: Typography.md,
    fontWeight: '600',
    color: '#ffffff',
  },
});