import React, { useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  Modal,
  TextInput,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface Goal {
  id: number;
  title: string;
  target_amount: number;
  current_amount: number;
  deadline: string;
  is_completed: boolean;
}

export default function GoalScreen() {
  const [goals, setGoals] = useState<Goal[]>([
    {
      id: 1,
      title: 'New Car Down Payment',
      target_amount: 5000,
      current_amount: 3200,
      deadline: '2025-12-31',
      is_completed: false,
    },
    {
      id: 2,
      title: 'Emergency Fund',
      target_amount: 2000,
      current_amount: 1500,
      deadline: '2025-06-30',
      is_completed: false,
    },
  ]);
  const [modalVisible, setModalVisible] = useState(false);
  const [newGoal, setNewGoal] = useState({
    title: '',
    target_amount: 0,
    deadline: '',
  });

  const handleAddGoal = () => {
    if (!newGoal.title || newGoal.target_amount <= 0) {
      Alert.alert('Error', 'Please fill in all fields');
      return;
    }

    const goal: Goal = {
      id: goals.length + 1,
      title: newGoal.title,
      target_amount: newGoal.target_amount,
      current_amount: 0,
      deadline: newGoal.deadline,
      is_completed: false,
    };

    setGoals([...goals, goal]);
    setModalVisible(false);
    setNewGoal({ title: '', target_amount: 0, deadline: '' });
    Alert.alert('Success', 'Goal created successfully!');
  };

  const calculateProgress = (current: number, target: number) => {
    return Math.min((current / target) * 100, 100);
  };

  return (
    <View className="flex-1 bg-gray-50">
      <ScrollView className="flex-1 p-4">
        {/* Header */}
        <View className="flex-row justify-between items-center mb-6">
          <View>
            <Text className="text-2xl font-bold text-gray-800">Financial Goals</Text>
            <Text className="text-gray-500">{goals.length} active goals</Text>
          </View>
          <TouchableOpacity
            className="bg-primary-500 rounded-full p-3 active:bg-primary-600"
            onPress={() => setModalVisible(true)}
          >
            <Ionicons name="add" size={28} color="white" />
          </TouchableOpacity>
        </View>

        {/* Goals List */}
        {goals.length === 0 ? (
          <View className="items-center justify-center py-20">
            <Text className="text-6xl mb-4">🎯</Text>
            <Text className="text-gray-400 text-center text-lg">
              No goals yet{'\n'}Tap + to set your first goal
            </Text>
          </View>
        ) : (
          goals.map((goal) => {
            const progress = calculateProgress(goal.current_amount, goal.target_amount);
            return (
              <View key={goal.id} className="bg-white rounded-2xl p-5 mb-4 shadow-sm">
                <View className="flex-row items-center justify-between mb-3">
                  <View className="flex-1">
                    <Text className="text-xl font-bold text-gray-800">{goal.title}</Text>
                    <Text className="text-gray-500 text-sm">Due: {goal.deadline}</Text>
                  </View>
                  {goal.is_completed && (
                    <View className="bg-green-100 rounded-full px-3 py-1">
                      <Text className="text-green-700 font-semibold text-xs">Completed</Text>
                    </View>
                  )}
                </View>

                {/* Progress Bar */}
                <View className="mb-3">
                  <View className="flex-row justify-between mb-2">
                    <Text className="text-gray-600 text-sm">${goal.current_amount.toFixed(2)}</Text>
                    <Text className="text-gray-600 text-sm">${goal.target_amount.toFixed(2)}</Text>
                  </View>
                  <View className="bg-gray-200 rounded-full h-3 overflow-hidden">
                    <View
                      className="bg-primary-500 h-full rounded-full"
                      style={{ width: `${progress}%` }}
                    />
                  </View>
                  <Text className="text-gray-500 text-xs mt-1 text-right">{progress.toFixed(0)}%</Text>
                </View>

                {/* Stats */}
                <View className="border-t border-gray-100 pt-3">
                  <View className="flex-row justify-between">
                    <Text className="text-gray-600">Remaining</Text>
                    <Text className="font-semibold text-gray-800">
                      ${(goal.target_amount - goal.current_amount).toFixed(2)}
                    </Text>
                  </View>
                </View>
              </View>
            );
          })
        )}
      </ScrollView>

      {/* Add Goal Modal */}
      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => setModalVisible(false)}
      >
        <View className="flex-1 justify-end bg-black/50">
          <View className="bg-white rounded-t-3xl p-6">
            <View className="flex-row justify-between items-center mb-6">
              <Text className="text-2xl font-bold text-gray-800">Set New Goal</Text>
              <TouchableOpacity onPress={() => setModalVisible(false)}>
                <Ionicons name="close" size={28} color="#666" />
              </TouchableOpacity>
            </View>

            <View className="mb-4">
              <Text className="text-sm font-medium text-gray-700 mb-2">Goal Title</Text>
              <TextInput
                className="bg-gray-100 rounded-xl px-4 py-3"
                placeholder="e.g., New Car Down Payment"
                value={newGoal.title}
                onChangeText={(text) => setNewGoal({ ...newGoal, title: text })}
              />
            </View>

            <View className="mb-4">
              <Text className="text-sm font-medium text-gray-700 mb-2">Target Amount ($)</Text>
              <TextInput
                className="bg-gray-100 rounded-xl px-4 py-3"
                placeholder="e.g., 5000"
                value={newGoal.target_amount.toString()}
                onChangeText={(text) => setNewGoal({ ...newGoal, target_amount: parseFloat(text) || 0 })}
                keyboardType="numeric"
              />
            </View>

            <View className="mb-6">
              <Text className="text-sm font-medium text-gray-700 mb-2">Deadline</Text>
              <TextInput
                className="bg-gray-100 rounded-xl px-4 py-3"
                placeholder="YYYY-MM-DD"
                value={newGoal.deadline}
                onChangeText={(text) => setNewGoal({ ...newGoal, deadline: text })}
              />
            </View>

            <TouchableOpacity
              className="bg-primary-500 rounded-xl py-4 active:bg-primary-600"
              onPress={handleAddGoal}
            >
              <Text className="text-white text-center text-lg font-bold">Create Goal</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
}
