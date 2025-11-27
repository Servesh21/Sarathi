import React, { useState, useRef, useEffect } from 'react';
import { View, Text, TextInput, ScrollView, KeyboardAvoidingView, Platform, ActivityIndicator, TouchableOpacity } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { agentAPI } from '../../api/alerts';
import { SafeAreaView } from 'react-native-safe-area-context';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Audio } from 'expo-av'; // <--- NEW: Audio Library
import { API_URL } from '../../api/client'; // Import your API URL helper

interface Message {
    id: string;
    type: 'user' | 'agent';
    content: string;
    timestamp: string;
}

const STORAGE_KEY = 'SARATHI_CHAT_V3'; // Changed key to V3 for fresh voice features

export default function ChatScreen({ navigation }: any) {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const scrollViewRef = useRef<ScrollView>(null);

    // --- VOICE STATE ---
    const [recording, setRecording] = useState<Audio.Recording | null>(null);
    const [isRecording, setIsRecording] = useState(false);
    const [sound, setSound] = useState<Audio.Sound | null>(null);

    // 1. SETUP: Hide Default Header & Load History
    useEffect(() => {
        // FIX: This removes the duplicate header from the navigation stack
        navigation.setOptions({ headerShown: false });
        
        loadHistory();

        // Cleanup audio on exit
        return () => {
            if (sound) sound.unloadAsync();
        };
    }, []);

    const loadHistory = async () => {
        try {
            const stored = await AsyncStorage.getItem(STORAGE_KEY);
            if (stored) {
                setMessages(JSON.parse(stored));
            } else {
                const welcome: Message = {
                    id: '1',
                    type: 'agent',
                    content: 'Hello! I\'m Sarathi AI. Type or speak to get started.',
                    timestamp: new Date().toISOString(),
                };
                setMessages([welcome]);
                saveHistory([welcome]);
            }
        } catch (e) { console.error(e); }
    };

    const saveHistory = async (newMessages: Message[]) => {
        await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(newMessages));
    };

    // --- VOICE FUNCTIONS ---

    async function startRecording() {
        try {
            const perm = await Audio.requestPermissionsAsync();
            if (perm.status !== 'granted') return;

            await Audio.setAudioModeAsync({
                allowsRecordingIOS: true,
                playsInSilentModeIOS: true,
            });

            const { recording } = await Audio.Recording.createAsync(
                Audio.RecordingOptionsPresets.HIGH_QUALITY
            );
            setRecording(recording);
            setIsRecording(true);
        } catch (err) {
            console.error('Failed to start recording', err);
        }
    }

    async function stopRecording() {
        setIsRecording(false);
        setRecording(null);
        if (!recording) return;

        await recording.stopAndUnloadAsync();
        const uri = recording.getURI(); 
        if (uri) sendVoiceMessage(uri);
    }

    const sendVoiceMessage = async (uri: string) => {
        setIsLoading(true);
        // Show temp message
        const tempId = Date.now().toString();
        const tempHistory = [...messages, {
            id: tempId,
            type: 'user' as const,
            content: '🎤 Sending Voice...',
            timestamp: new Date().toISOString()
        }];
        setMessages(tempHistory);

        try {
            const response = await agentAPI.voiceChat(uri);

            // 1. Play Audio Response
            if (response.audio_url) {
                const audioSource = response.audio_url.startsWith('http') 
                    ? response.audio_url 
                    : `${API_URL}${response.audio_url}`;
                
                const { sound } = await Audio.Sound.createAsync(
                    { uri: audioSource },
                    { shouldPlay: true }
                );
                setSound(sound);
            }

            // 2. Update UI with real text
            const userMsg: Message = {
                id: tempId,
                type: 'user',
                content: `🎤 "${response.transcription || 'Voice Message'}"`,
                timestamp: new Date().toISOString()
            };

            const agentMsg: Message = {
                id: (Date.now() + 1).toString(),
                type: 'agent',
                content: response.response,
                timestamp: new Date().toISOString()
            };

            // Remove temp, add real
            const final = tempHistory.filter(m => m.id !== tempId).concat([userMsg, agentMsg]);
            setMessages(final);
            saveHistory(final);

        } catch (error) {
            console.error(error);
            const errHistory = [...tempHistory.filter(m => m.id !== tempId), {
                id: Date.now().toString(),
                type: 'agent' as const,
                content: 'Sorry, voice processing failed.',
                timestamp: new Date().toISOString()
            }];
            setMessages(errHistory);
        } finally {
            setIsLoading(false);
        }
    };

    // --- TEXT FUNCTIONS ---

    const handleSend = async () => {
        const text = input.trim();
        if (!text) return;

        const userMsg: Message = {
            id: Date.now().toString(),
            type: 'user',
            content: text,
            timestamp: new Date().toISOString()
        };

        const newHistory = [...messages, userMsg];
        setMessages(newHistory);
        saveHistory(newHistory);
        setInput('');
        setIsLoading(true);

        try {
            const response = await agentAPI.chat(text);
            const agentMsg: Message = {
                id: (Date.now() + 1).toString(),
                type: 'agent',
                content: response.response,
                timestamp: new Date().toISOString()
            };
            const finalHistory = [...newHistory, agentMsg];
            setMessages(finalHistory);
            saveHistory(finalHistory);
        } catch (error) {
            const errHistory = [...newHistory, {
                id: Date.now().toString(),
                type: 'agent' as const,
                content: 'Network error. Please try again.',
                timestamp: new Date().toISOString()
            }];
            setMessages(errHistory);
        } finally {
            setIsLoading(false);
        }
    };

    const formatTime = (ts: string) => {
        try { return new Date(ts).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}); }
        catch(e) { return ''; }
    };

    const clearChat = async () => {
        await AsyncStorage.removeItem(STORAGE_KEY);
        setMessages([]);
        loadHistory();
    };

    return (
        <SafeAreaView className="flex-1 bg-gray-50" edges={['top', 'bottom', 'left', 'right']}>
            <KeyboardAvoidingView
                behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
                className="flex-1"
                keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 0}
            >
                <View className="flex-1">
                    {/* Header - This is now the ONLY header */}
                    <View className="bg-emerald-600 px-4 py-4 flex-row justify-between items-center">
                        <View>
                            <Text className="text-white text-2xl font-bold">Chat with Sarathi</Text>
                            <Text className="text-white opacity-90">Your AI Resilience Agent</Text>
                        </View>
                        <TouchableOpacity onPress={clearChat}>
                            <Ionicons name="trash-outline" size={24} color="white" />
                        </TouchableOpacity>
                    </View>

                    {/* Chat Area */}
                    <ScrollView 
                        ref={scrollViewRef}
                        className="flex-1 px-4 py-4"
                        contentContainerStyle={{ paddingBottom: 20 }}
                        keyboardShouldPersistTaps="handled"
                        onContentSizeChange={() => scrollViewRef.current?.scrollToEnd({ animated: true })}
                    >
                        {messages.map((message) => {
                            const isUser = message.type === 'user';
                            return (
                                <View key={message.id} className={`mb-4 ${isUser ? 'items-end' : 'items-start'}`}>
                                    <View className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                                        isUser ? 'bg-emerald-600 rounded-br-none' : 'bg-white border border-gray-200 rounded-bl-none'
                                    }`}>
                                        <Text className={`${isUser ? 'text-white' : 'text-gray-900'} text-base`}>
                                            {message.content}
                                        </Text>
                                        <Text className={`text-xs mt-1 ${isUser ? 'text-emerald-100' : 'text-gray-400'}`}>
                                            {formatTime(message.timestamp)}
                                        </Text>
                                    </View>
                                </View>
                            );
                        })}
                        {isLoading && (
                            <View className="items-start mb-4">
                                <View className="bg-white rounded-2xl px-4 py-3 border border-gray-200">
                                    <ActivityIndicator size="small" color="#059669" />
                                </View>
                            </View>
                        )}
                    </ScrollView>

                    {/* Input Bar */}
                    <View className="px-4 py-4 bg-white border-t border-gray-200 pb-6">
                        <View className="flex-row items-end space-x-3">
                            <View className="flex-1">
                                <TextInput
                                    className="bg-gray-100 rounded-2xl px-4 py-3 text-gray-900 max-h-24"
                                    placeholder={isRecording ? "Listening..." : "Type or speak..."}
                                    placeholderTextColor="#9ca3af"
                                    value={input}
                                    onChangeText={setInput}
                                    multiline
                                    editable={!isRecording}
                                />
                            </View>

                            {/* LOGIC: Show Send if typing, otherwise Show Mic */}
                            {input.trim().length > 0 ? (
                                <TouchableOpacity onPress={handleSend} disabled={isLoading}>
                                    <LinearGradient
                                        colors={['#10b981', '#059669']}
                                        className="rounded-full w-12 h-12 items-center justify-center"
                                    >
                                        <Ionicons name="send" size={20} color="white" />
                                    </LinearGradient>
                                </TouchableOpacity>
                            ) : (
                                <TouchableOpacity onPress={isRecording ? stopRecording : startRecording}>
                                    <LinearGradient
                                        colors={isRecording ? ['#ef4444', '#dc2626'] : ['#3b82f6', '#2563eb']}
                                        className="rounded-full w-12 h-12 items-center justify-center"
                                    >
                                        <Ionicons 
                                            name={isRecording ? "stop" : "mic"} 
                                            size={24} 
                                            color="white" 
                                        />
                                    </LinearGradient>
                                </TouchableOpacity>
                            )}
                        </View>
                    </View>
                </View>
            </KeyboardAvoidingView>
        </SafeAreaView>
    );
}