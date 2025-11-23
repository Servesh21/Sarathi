import React, { useEffect } from 'react';
import { View, Text, ScrollView, ActivityIndicator } from 'react-native';
import { useFinancialStore } from '../../store/financialStore';

export default function GoalsScreen() {
    const { goals, fetchGoals, isLoading } = useFinancialStore();

    useEffect(() => {
        fetchGoals();
    }, []);

    if (isLoading && goals.length === 0) {
        return (
            <View className="flex-1 justify-center items-center bg-gray-50">
                <ActivityIndicator size="large" color="#10b981" />
            </View>
        );
    }

    return (
        <ScrollView className="flex-1 bg-gray-50">
            <View className="px-4 py-6">
                <Text className="text-3xl font-bold text-gray-900 mb-6">Financial Goals</Text>

                {goals.map((goal) => (
                    <View key={goal.id} className="bg-white rounded-xl p-5 mb-4 shadow-sm">
                        <View className="flex-row justify-between items-start mb-3">
                            <View className="flex-1">
                                <Text className="text-lg font-semibold text-gray-900">{goal.goal_name}</Text>
                                <Text className="text-gray-600 text-sm mt-1">{goal.goal_type}</Text>
                            </View>
                            <View className={`px-3 py-1 rounded-full ${goal.status === 'completed' ? 'bg-green-100' :
                                    goal.status === 'on_track' ? 'bg-blue-100' : 'bg-yellow-100'
                                }`}>
                                <Text className={`font-semibold text-sm ${goal.status === 'completed' ? 'text-green-700' :
                                        goal.status === 'on_track' ? 'text-blue-700' : 'text-yellow-700'
                                    }`}>
                                    {goal.status}
                                </Text>
                            </View>
                        </View>

                        <View className="mb-3">
                            <View className="flex-row justify-between mb-2">
                                <Text className="text-gray-600">Progress</Text>
                                <Text className="font-semibold text-gray-900">{goal.completion_percentage.toFixed(1)}%</Text>
                            </View>
                            <View className="bg-gray-200 rounded-full h-3">
                                <View
                                    className="bg-primary rounded-full h-3"
                                    style={{ width: `${goal.completion_percentage}%` }}
                                />
                            </View>
                        </View>

                        <View className="space-y-1">
                            <View className="flex-row justify-between">
                                <Text className="text-gray-600">Current</Text>
                                <Text className="font-semibold text-gray-900">₹{goal.current_amount.toFixed(0)}</Text>
                            </View>
                            <View className="flex-row justify-between">
                                <Text className="text-gray-600">Target</Text>
                                <Text className="font-semibold text-gray-900">₹{goal.target_amount.toFixed(0)}</Text>
                            </View>
                            <View className="flex-row justify-between">
                                <Text className="text-gray-600">Monthly</Text>
                                <Text className="font-semibold text-primary">₹{goal.monthly_contribution.toFixed(0)}</Text>
                            </View>
                            {goal.target_date && (
                                <View className="flex-row justify-between">
                                    <Text className="text-gray-600">Target Date</Text>
                                    <Text className="font-semibold text-gray-900">
                                        {new Date(goal.target_date).toLocaleDateString()}
                                    </Text>
                                </View>
                            )}
                        </View>
                    </View>
                ))}

                {goals.length === 0 && (
                    <View className="bg-gray-100 rounded-xl p-6 items-center">
                        <Text className="text-gray-600 text-center">No goals set yet. Start by creating your first financial goal!</Text>
                    </View>
                )}
            </View>
        </ScrollView>
    );
}
