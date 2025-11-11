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
import { LinearGradient } from 'expo-linear-gradient';

interface Goal {
    id: string;
    title: string;
    description: string;
    targetValue: number;
    currentValue: number;
    unit: string;
    category: 'safety' | 'efficiency' | 'savings' | 'distance';
    deadline: string;
    completed: boolean;
}

export default function GoalsScreen() {
    const [goals, setGoals] = useState<Goal[]>([
        {
            id: '1',
            title: 'Improve Safety Score',
            description: 'Maintain a 95% safety score for the month',
            targetValue: 95,
            currentValue: 88,
            unit: '%',
            category: 'safety',
            deadline: '2025-01-31',
            completed: false,
        },
        {
            id: '2',
            title: 'Fuel Efficiency Goal',
            description: 'Achieve 35 MPG average this month',
            targetValue: 35,
            currentValue: 32.5,
            unit: 'MPG',
            category: 'efficiency',
            deadline: '2025-01-31',
            completed: false,
        },
        {
            id: '3',
            title: 'Save on Gas',
            description: 'Save $200 this month through efficient driving',
            targetValue: 200,
            currentValue: 145,
            unit: '$',
            category: 'savings',
            deadline: '2025-01-31',
            completed: false,
        },
    ]);

    const [showAddModal, setShowAddModal] = useState(false);
    const [newGoal, setNewGoal] = useState({
        title: '',
        description: '',
        targetValue: '',
        unit: '',
        category: 'safety' as Goal['category'],
        deadline: '',
    });

    const addGoal = () => {
        if (!newGoal.title || !newGoal.targetValue) {
            Alert.alert('Error', 'Please fill in the required fields');
            return;
        }

        const goal: Goal = {
            id: Date.now().toString(),
            title: newGoal.title,
            description: newGoal.description,
            targetValue: parseFloat(newGoal.targetValue),
            currentValue: 0,
            unit: newGoal.unit,
            category: newGoal.category,
            deadline: newGoal.deadline,
            completed: false,
        };

        setGoals([...goals, goal]);
        setShowAddModal(false);
        setNewGoal({
            title: '',
            description: '',
            targetValue: '',
            unit: '',
            category: 'safety',
            deadline: '',
        });
    };

    const getProgressPercentage = (goal: Goal) => {
        return Math.min((goal.currentValue / goal.targetValue) * 100, 100);
    };

    const getCategoryColor = (category: Goal['category']) => {
        switch (category) {
            case 'safety': return '#ef4444';
            case 'efficiency': return '#10b981';
            case 'savings': return '#f59e0b';
            case 'distance': return '#8b5cf6';
            default: return '#6b7280';
        }
    };

    const getCategoryIcon = (category: Goal['category']) => {
        switch (category) {
            case 'safety': return '🛡️';
            case 'efficiency': return '⛽';
            case 'savings': return '💰';
            case 'distance': return '📍';
            default: return '🎯';
        }
    };

    return (
        <View style={{ flex: 1, backgroundColor: '#f9fafb' }}>
            <LinearGradient
                colors={['#0ea5e9', '#3b82f6']}
                style={{ paddingTop: 60, paddingBottom: 20, paddingHorizontal: 20 }}
            >
                <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>
                    <View>
                        <Text style={{ color: 'white', fontSize: 28, fontWeight: 'bold', marginBottom: 8 }}>
                            My Goals
                        </Text>
                        <Text style={{ color: 'rgba(255,255,255,0.9)', fontSize: 16 }}>
                            Track your driving progress
                        </Text>
                    </View>
                    <TouchableOpacity
                        style={{
                            backgroundColor: 'rgba(255,255,255,0.2)',
                            borderRadius: 12,
                            padding: 12,
                        }}
                        onPress={() => setShowAddModal(true)}
                    >
                        <Text style={{ color: 'white', fontWeight: 'bold' }}>+ New</Text>
                    </TouchableOpacity>
                </View>
            </LinearGradient>

            <ScrollView style={{ flex: 1, padding: 20 }}>
                {goals.map((goal) => (
                    <View
                        key={goal.id}
                        style={{
                            backgroundColor: 'white',
                            borderRadius: 16,
                            padding: 20,
                            marginBottom: 16,
                            shadowColor: '#000',
                            shadowOffset: { width: 0, height: 2 },
                            shadowOpacity: 0.1,
                            shadowRadius: 4,
                            elevation: 3,
                        }}
                    >
                        <View style={{ flexDirection: 'row', alignItems: 'center', marginBottom: 12 }}>
                            <Text style={{ fontSize: 24, marginRight: 12 }}>
                                {getCategoryIcon(goal.category)}
                            </Text>
                            <View style={{ flex: 1 }}>
                                <Text style={{ fontSize: 18, fontWeight: 'bold', color: '#1f2937', marginBottom: 4 }}>
                                    {goal.title}
                                </Text>
                                <Text style={{ color: '#6b7280', fontSize: 14 }}>
                                    {goal.description}
                                </Text>
                            </View>
                            <View style={{
                                backgroundColor: getCategoryColor(goal.category),
                                borderRadius: 20,
                                paddingHorizontal: 8,
                                paddingVertical: 2,
                            }}>
                                <Text style={{ color: 'white', fontSize: 10, fontWeight: 'bold' }}>
                                    {goal.category.toUpperCase()}
                                </Text>
                            </View>
                        </View>

                        <View style={{ marginBottom: 12 }}>
                            <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginBottom: 8 }}>
                                <Text style={{ fontSize: 16, fontWeight: '600', color: '#374151' }}>
                                    Progress
                                </Text>
                                <Text style={{ fontSize: 16, fontWeight: '600', color: '#374151' }}>
                                    {goal.currentValue}{goal.unit} / {goal.targetValue}{goal.unit}
                                </Text>
                            </View>
                            <View style={{ 
                                height: 8, 
                                backgroundColor: '#e5e7eb', 
                                borderRadius: 4,
                                overflow: 'hidden'
                            }}>
                                <View style={{
                                    height: '100%',
                                    width: `${getProgressPercentage(goal)}%`,
                                    backgroundColor: getCategoryColor(goal.category),
                                    borderRadius: 4,
                                }} />
                            </View>
                            <Text style={{ 
                                textAlign: 'right', 
                                color: '#6b7280', 
                                fontSize: 12, 
                                marginTop: 4 
                            }}>
                                {getProgressPercentage(goal).toFixed(0)}% Complete
                            </Text>
                        </View>

                        <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>
                            <Text style={{ color: '#6b7280', fontSize: 14 }}>
                                Due: {new Date(goal.deadline).toLocaleDateString()}
                            </Text>
                            <TouchableOpacity
                                style={{
                                    backgroundColor: '#f3f4f6',
                                    borderRadius: 8,
                                    paddingHorizontal: 16,
                                    paddingVertical: 8,
                                }}
                            >
                                <Text style={{ color: '#374151', fontWeight: '500' }}>Update Progress</Text>
                            </TouchableOpacity>
                        </View>
                    </View>
                ))}

                {goals.length === 0 && (
                    <View style={{ 
                        backgroundColor: 'white', 
                        borderRadius: 16, 
                        padding: 40, 
                        alignItems: 'center',
                        shadowColor: '#000',
                        shadowOffset: { width: 0, height: 2 },
                        shadowOpacity: 0.1,
                        shadowRadius: 4,
                        elevation: 3,
                    }}>
                        <Text style={{ fontSize: 48, marginBottom: 16 }}>🎯</Text>
                        <Text style={{ fontSize: 18, fontWeight: 'bold', color: '#1f2937', marginBottom: 8 }}>
                            No Goals Yet
                        </Text>
                        <Text style={{ color: '#6b7280', textAlign: 'center', marginBottom: 20 }}>
                            Set your first driving goal to start tracking your progress!
                        </Text>
                        <TouchableOpacity
                            style={{
                                backgroundColor: '#0ea5e9',
                                borderRadius: 12,
                                paddingHorizontal: 24,
                                paddingVertical: 12,
                            }}
                            onPress={() => setShowAddModal(true)}
                        >
                            <Text style={{ color: 'white', fontWeight: 'bold' }}>Create Your First Goal</Text>
                        </TouchableOpacity>
                    </View>
                )}
            </ScrollView>

            <Modal visible={showAddModal} animationType="slide" presentationStyle="pageSheet">
                <View style={{ flex: 1, backgroundColor: 'white' }}>
                    <View style={{ padding: 20, borderBottomWidth: 1, borderBottomColor: '#e5e7eb' }}>
                        <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>
                            <TouchableOpacity onPress={() => setShowAddModal(false)}>
                                <Text style={{ color: '#6b7280', fontSize: 16 }}>Cancel</Text>
                            </TouchableOpacity>
                            <Text style={{ fontSize: 18, fontWeight: 'bold' }}>New Goal</Text>
                            <TouchableOpacity onPress={addGoal}>
                                <Text style={{ color: '#0ea5e9', fontSize: 16, fontWeight: '600' }}>Save</Text>
                            </TouchableOpacity>
                        </View>
                    </View>

                    <ScrollView style={{ padding: 20 }}>
                        <View style={{ marginBottom: 20 }}>
                            <Text style={{ fontSize: 16, fontWeight: '600', marginBottom: 8, color: '#374151' }}>
                                Goal Title *
                            </Text>
                            <TextInput
                                style={{
                                    borderWidth: 1,
                                    borderColor: '#d1d5db',
                                    borderRadius: 12,
                                    padding: 16,
                                    fontSize: 16,
                                    backgroundColor: '#f9fafb',
                                }}
                                value={newGoal.title}
                                onChangeText={(text) => setNewGoal({ ...newGoal, title: text })}
                                placeholder="Improve safety score, Save money..."
                            />
                        </View>

                        <View style={{ marginBottom: 20 }}>
                            <Text style={{ fontSize: 16, fontWeight: '600', marginBottom: 8, color: '#374151' }}>
                                Description
                            </Text>
                            <TextInput
                                style={{
                                    borderWidth: 1,
                                    borderColor: '#d1d5db',
                                    borderRadius: 12,
                                    padding: 16,
                                    fontSize: 16,
                                    backgroundColor: '#f9fafb',
                                    minHeight: 80,
                                }}
                                value={newGoal.description}
                                onChangeText={(text) => setNewGoal({ ...newGoal, description: text })}
                                placeholder="Describe your goal..."
                                multiline
                                textAlignVertical="top"
                            />
                        </View>

                        <View style={{ marginBottom: 20 }}>
                            <Text style={{ fontSize: 16, fontWeight: '600', marginBottom: 8, color: '#374151' }}>
                                Category
                            </Text>
                            <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 8 }}>
                                {(['safety', 'efficiency', 'savings', 'distance'] as Goal['category'][]).map((category) => (
                                    <TouchableOpacity
                                        key={category}
                                        style={{
                                            backgroundColor: newGoal.category === category ? getCategoryColor(category) : '#f3f4f6',
                                            borderRadius: 20,
                                            paddingHorizontal: 16,
                                            paddingVertical: 8,
                                        }}
                                        onPress={() => setNewGoal({ ...newGoal, category })}
                                    >
                                        <Text style={{
                                            color: newGoal.category === category ? 'white' : '#374151',
                                            fontWeight: '500',
                                        }}>
                                            {getCategoryIcon(category)} {category.charAt(0).toUpperCase() + category.slice(1)}
                                        </Text>
                                    </TouchableOpacity>
                                ))}
                            </View>
                        </View>

                        <View style={{ marginBottom: 20 }}>
                            <Text style={{ fontSize: 16, fontWeight: '600', marginBottom: 8, color: '#374151' }}>
                                Target Value *
                            </Text>
                            <View style={{ flexDirection: 'row', gap: 12 }}>
                                <TextInput
                                    style={{
                                        flex: 2,
                                        borderWidth: 1,
                                        borderColor: '#d1d5db',
                                        borderRadius: 12,
                                        padding: 16,
                                        fontSize: 16,
                                        backgroundColor: '#f9fafb',
                                    }}
                                    value={newGoal.targetValue}
                                    onChangeText={(text) => setNewGoal({ ...newGoal, targetValue: text })}
                                    placeholder="100"
                                    keyboardType="numeric"
                                />
                                <TextInput
                                    style={{
                                        flex: 1,
                                        borderWidth: 1,
                                        borderColor: '#d1d5db',
                                        borderRadius: 12,
                                        padding: 16,
                                        fontSize: 16,
                                        backgroundColor: '#f9fafb',
                                    }}
                                    value={newGoal.unit}
                                    onChangeText={(text) => setNewGoal({ ...newGoal, unit: text })}
                                    placeholder="%, $, MPG"
                                />
                            </View>
                        </View>

                        <View style={{ marginBottom: 20 }}>
                            <Text style={{ fontSize: 16, fontWeight: '600', marginBottom: 8, color: '#374151' }}>
                                Deadline
                            </Text>
                            <TextInput
                                style={{
                                    borderWidth: 1,
                                    borderColor: '#d1d5db',
                                    borderRadius: 12,
                                    padding: 16,
                                    fontSize: 16,
                                    backgroundColor: '#f9fafb',
                                }}
                                value={newGoal.deadline}
                                onChangeText={(text) => setNewGoal({ ...newGoal, deadline: text })}
                                placeholder="2025-01-31"
                            />
                        </View>
                    </ScrollView>
                </View>
            </Modal>
        </View>
    );
}