import React, { useState, useRef, useEffect } from 'react';
import { View, Text, TextInput, ScrollView, KeyboardAvoidingView, Platform, SafeAreaView, ActivityIndicator } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { agentAPI } from '../../api/alerts';
import { Button, Card } from '../../components';

interface Message {
    id: string;
    type: 'user' | 'agent';
    content: string;
    timestamp: Date;
}

const QUICK_ACTIONS = [
    { title: 'Earnings Tips', icon: 'trending-up', message: 'How can I increase my daily earnings?' },
    { title: 'Vehicle Health', icon: 'car-sport', message: 'Check my vehicle maintenance status' },
    { title: 'Investment Options', icon: 'wallet', message: 'What investment options do you recommend?' },
    { title: 'Route Optimization', icon: 'location', message: 'Suggest the best routes for today' },
];

export default function ChatScreen({ navigation }: any) {
    const [messages, setMessages] = useState<Message[]>([
        {
            id: '1',
            type: 'agent',
            content: 'Hello! I\'m Sarathi AI, your autonomous resilience agent. I can help you with earnings optimization, vehicle health, and investment planning. How can I assist you today?',
            timestamp: new Date(),
        }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const scrollViewRef = useRef<ScrollView>(null);

    useEffect(() => {
        scrollViewRef.current?.scrollToEnd({ animated: true });
    }, [messages]);

    const handleSend = async (message?: string) => {
        const messageToSend = message || input.trim();
        if (!messageToSend) return;

        const userMessage: Message = {
            id: Date.now().toString(),
            type: 'user',
            content: messageToSend,
            timestamp: new Date(),
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await agentAPI.chat(messageToSend);

            const agentMessage: Message = {
                id: (Date.now() + 1).toString(),
                type: 'agent',
                content: response.response,
                timestamp: new Date(),
            };

            setMessages(prev => [...prev, agentMessage]);

            // Add recommendations if present
            if (response.recommendations && response.recommendations.length > 0) {
                const recsMessage: Message = {
                    id: (Date.now() + 2).toString(),
                    type: 'agent',
                    content: '📊 Recommendations:\n' + response.recommendations.map((r: any, i: number) =>
                        `${i + 1}. ${JSON.stringify(r)}`
                    ).join('\n'),
                    timestamp: new Date(),
                };
                setMessages(prev => [...prev, recsMessage]);
            }
        } catch (error) {
            const errorMessage: Message = {
                id: (Date.now() + 1).toString(),
                type: 'agent',
                content: 'Sorry, I encountered an error. Please try again.',
                timestamp: new Date(),
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const renderMessage = (message: Message) => {
        const isUser = message.type === 'user';

        return (
            <View
                key={message.id}
                className={`mb-4 ${isUser ? 'items-end' : 'items-start'}`}
            >
                {!isUser && (
                    <View className="flex-row items-center mb-2">
                        <LinearGradient
                            colors={['#8b5cf6', '#7c3aed']}
                            className="w-8 h-8 rounded-full items-center justify-center mr-2"
                        >
                            <Ionicons name="chatbubbles" size={16} color="white" />
                        </LinearGradient>
                        <Text className="text-xs text-gray-500">Sarathi AI</Text>
                    </View>
                )}

                <View
                    className={`max-w-[80%] p-4 rounded-2xl ${isUser
                        ? 'bg-primary-500 rounded-br-sm'
                        : 'bg-white rounded-bl-sm shadow-sm'
                        }`}
                >
                    <Text className={`${isUser ? 'text-white' : 'text-gray-900'}`}>
                        {message.content}
                    </Text>
                </View>

                <Text className="text-xs text-gray-400 mt-1">
                    {message.timestamp.toLocaleTimeString([], {
                        hour: '2-digit',
                        minute: '2-digit'
                    })}
                </Text>
            </View>
        );
    };

    return (
        <KeyboardAvoidingView
            behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
            className="flex-1 bg-gray-50"
            keyboardVerticalOffset={Platform.OS === 'ios' ? 90 : 0}
        >
            <View className="flex-1">
                <View className="bg-primary px-4 py-6 pt-12">
                    <Text className="text-white text-2xl font-bold">Chat with Sarathi</Text>
                    <Text className="text-white opacity-90">Your AI Resilience Agent</Text>
                </View>

                <ScrollView className="flex-1 px-4 py-4">
                    {messages.map((message) => (
                        <View
                            key={message.id}
                            className={`mb-4 ${message.type === 'user' ? 'items-end' : 'items-start'}`}
                        >
                            <View
                                className={`max-w-[80%] rounded-2xl px-4 py-3 ${message.type === 'user'
                                    ? 'bg-primary'
                                    : 'bg-white border border-gray-200'
                                    }`}
                            >
                                <Text
                                    className={`${message.type === 'user' ? 'text-white' : 'text-gray-900'
                                        }`}
                                >
                                    {message.content}
                                </Text>
                                <Text
                                    className={`text-xs mt-1 ${message.type === 'user' ? 'text-white opacity-70' : 'text-gray-500'
                                        }`}
                                >
                                    {message.timestamp.toLocaleTimeString()}
                                </Text>
                            </View>
                        </View>
                    ))}

                    {isLoading && (
                        <View className="items-start mb-4">
                            <View className="bg-white rounded-2xl px-4 py-3 border border-gray-200">
                                <ActivityIndicator size="small" color="#10b981" />
                            </View>
                        </View>
                    )}
                </ScrollView>

                {/* Input Bar */}
                <View className="px-4 py-4 bg-white border-t border-gray-200">
                    <View className="flex-row items-end space-x-3">
                        <View className="flex-1">
                            <TextInput
                                className="bg-gray-100 rounded-2xl px-4 py-3 text-gray-900 max-h-24"
                                placeholder="Ask me about earnings, vehicle health, investments..."
                                placeholderTextColor="#9ca3af"
                                value={input}
                                onChangeText={setInput}
                                multiline
                                returnKeyType="send"
                                onSubmitEditing={() => handleSend()}
                            />
                        </View>
                        <LinearGradient
                            colors={['#10b981', '#059669']}
                            className={`rounded-full w-12 h-12 items-center justify-center ${(!input.trim() || isLoading) ? 'opacity-50' : ''
                                }`}
                        >
                            <Ionicons
                                name="send"
                                size={20}
                                color="white"
                                onPress={() => handleSend()}
                                suppressHighlighting={true}
                                style={{ opacity: (!input.trim() || isLoading) ? 0.5 : 1 }}
                            />
                        </LinearGradient>
                    </View>
                </View>
            </View>
        </KeyboardAvoidingView>
    );
}
