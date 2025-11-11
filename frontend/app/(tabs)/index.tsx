import React, { useState } from 'react';
import {
    View,
    Text,
    ScrollView,
    TouchableOpacity,
    TextInput,
    Alert,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useAuthStore } from '../../src/stores/authStore';

export default function DashboardScreen() {
    const [message, setMessage] = useState('');
    const [conversations, setConversations] = useState([
        { id: '1', message: 'Welcome to Sarathi! How can I help you today?', isBot: true },
    ]);
    const { user } = useAuthStore();

    const sendMessage = () => {
        if (!message.trim()) return;

        // Add user message
        const userMessage = { id: Date.now().toString(), message, isBot: false };
        setConversations(prev => [...prev, userMessage]);

        // Simulate bot response
        setTimeout(() => {
            const botResponse = {
                id: (Date.now() + 1).toString(),
                message: 'I understand you said: "' + message + '". How can I assist you further with your driving goals?',
                isBot: true,
            };
            setConversations(prev => [...prev, botResponse]);
        }, 1000);

        setMessage('');
    };

    return (
        <View style={{ flex: 1, backgroundColor: '#f9fafb' }}>
            <LinearGradient
                colors={['#0ea5e9', '#3b82f6']}
                style={{ paddingTop: 60, paddingBottom: 20, paddingHorizontal: 20 }}
            >
                <Text style={{ color: 'white', fontSize: 28, fontWeight: 'bold', marginBottom: 8 }}>
                    Welcome back, {user?.name?.split(' ')[0] || 'Driver'}!
                </Text>
                <Text style={{ color: 'rgba(255,255,255,0.9)', fontSize: 16 }}>
                    Ready for your next journey?
                </Text>
            </LinearGradient>

            <ScrollView style={{ flex: 1, padding: 20 }}>
                <View style={{ backgroundColor: 'white', borderRadius: 16, padding: 20, marginBottom: 20, shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.1, shadowRadius: 4, elevation: 3 }}>
                    <Text style={{ fontSize: 20, fontWeight: 'bold', marginBottom: 16, color: '#1f2937' }}>
                        Quick Stats
                    </Text>
                    <View style={{ flexDirection: 'row', justifyContent: 'space-between' }}>
                        <View style={{ alignItems: 'center' }}>
                            <Text style={{ fontSize: 24, fontWeight: 'bold', color: '#0ea5e9' }}>12.5k</Text>
                            <Text style={{ color: '#6b7280' }}>Miles Driven</Text>
                        </View>
                        <View style={{ alignItems: 'center' }}>
                            <Text style={{ fontSize: 24, fontWeight: 'bold', color: '#10b981' }}>98%</Text>
                            <Text style={{ color: '#6b7280' }}>Safety Score</Text>
                        </View>
                        <View style={{ alignItems: 'center' }}>
                            <Text style={{ fontSize: 24, fontWeight: 'bold', color: '#f59e0b' }}>$2,340</Text>
                            <Text style={{ color: '#6b7280' }}>Saved</Text>
                        </View>
                    </View>
                </View>

                <View style={{ backgroundColor: 'white', borderRadius: 16, padding: 20, marginBottom: 20, shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.1, shadowRadius: 4, elevation: 3 }}>
                    <Text style={{ fontSize: 20, fontWeight: 'bold', marginBottom: 16, color: '#1f2937' }}>
                        AI Assistant
                    </Text>
                    
                    <ScrollView style={{ height: 200, marginBottom: 16 }}>
                        {conversations.map((conv) => (
                            <View
                                key={conv.id}
                                style={{
                                    alignSelf: conv.isBot ? 'flex-start' : 'flex-end',
                                    backgroundColor: conv.isBot ? '#f3f4f6' : '#0ea5e9',
                                    padding: 12,
                                    borderRadius: 12,
                                    marginBottom: 8,
                                    maxWidth: '80%',
                                }}
                            >
                                <Text style={{ color: conv.isBot ? '#374151' : 'white' }}>
                                    {conv.message}
                                </Text>
                            </View>
                        ))}
                    </ScrollView>

                    <View style={{ flexDirection: 'row', alignItems: 'center' }}>
                        <TextInput
                            style={{
                                flex: 1,
                                borderWidth: 1,
                                borderColor: '#d1d5db',
                                borderRadius: 12,
                                padding: 12,
                                marginRight: 12,
                                backgroundColor: '#f9fafb',
                            }}
                            value={message}
                            onChangeText={setMessage}
                            placeholder="Ask me anything about driving..."
                            multiline
                        />
                        <TouchableOpacity
                            style={{
                                backgroundColor: '#0ea5e9',
                                borderRadius: 12,
                                padding: 12,
                            }}
                            onPress={sendMessage}
                        >
                            <Text style={{ color: 'white', fontWeight: 'bold' }}>Send</Text>
                        </TouchableOpacity>
                    </View>
                </View>
            </ScrollView>
        </View>
    );
}
