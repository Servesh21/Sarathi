import React, { useState, useRef, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  TextInput,
  Alert,
  ActivityIndicator,
  Dimensions,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useAuthStore } from '../../src/stores/authStore';
import { agentAPI } from '../../src/services/api';

const { width: screenWidth, height: screenHeight } = Dimensions.get('window');

export default function DashboardScreen() {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversations, setConversations] = useState([
    {
      id: '1',
      message: 'Hello! I\'m your AI driving assistant 🚗\n\n• Ask about earnings & income\n• Get weather updates\n• Find nearby mechanics\n• Trip planning help\n\nTap the buttons below or just ask me anything!',
      isBot: true,
      intent: 'welcome',
      timestamp: new Date(),
    },
  ]);
  const { user } = useAuthStore();
  const scrollViewRef = useRef<ScrollView>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    scrollViewRef.current?.scrollToEnd({ animated: true });
  }, [conversations]);

  const quickActions = [
    {
      id: 'earnings',
      icon: '💰',
      title: 'Today\'s Earnings',
      message: 'How much did I earn today?',
      color: '#10b981',
      bgColor: '#ecfdf5',
    },
    {
      id: 'weather',
      icon: '🌤️',
      title: 'Weather Update',
      message: 'What\'s the weather like in Mumbai?',
      color: '#0ea5e9',
      bgColor: '#f0f9ff',
    },
    {
      id: 'mechanics',
      icon: '🔧',
      title: 'Find Mechanics',
      message: 'Find mechanics near me',
      color: '#f59e0b',
      bgColor: '#fefbeb',
    },
    {
      id: 'trip',
      icon: '🗺️',
      title: 'Add Trip',
      message: 'I completed a trip from Bandra to Andheri for 150 rupees',
      color: '#8b5cf6',
      bgColor: '#faf5ff',
    },
  ];

  const sendMessage = async (customMessage?: string) => {
    const messageToSend = customMessage || message.trim();
    if (!messageToSend || loading) return;

    // Add user message
    const userMessage = {
      id: Date.now().toString(),
      message: messageToSend,
      isBot: false,
      intent: 'user_input',
      timestamp: new Date(),
    };
    setConversations(prev => [...prev, userMessage]);

    if (!customMessage) setMessage('');
    setLoading(true);

    try {
      // Call our optimized AI agent
      const response = await agentAPI.sendMessage(messageToSend, user?.id);

      const botResponse = {
        id: (Date.now() + 1).toString(),
        message: response.data.response || 'Sorry, I couldn\'t process that request.',
        isBot: true,
        intent: response.data.intent || 'unknown',
        timestamp: new Date(),
      };

      setConversations(prev => [...prev, botResponse]);

    } catch (error) {
      console.error('AI Agent Error:', error);

      // Fallback response
      const errorResponse = {
        id: (Date.now() + 1).toString(),
        message: '🔧 Connection issue detected. Make sure you have internet connectivity and try again.',
        isBot: true,
        intent: 'error',
        timestamp: new Date(),
      };

      setConversations(prev => [...prev, errorResponse]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={{ flex: 1 }}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <View style={{ flex: 1, backgroundColor: '#f8fafc' }}>
        {/* Header */}
        <LinearGradient
          colors={['#1e40af', '#3b82f6']}
          style={{
            paddingTop: Platform.OS === 'ios' ? 50 : 40,
            paddingBottom: 20,
            paddingHorizontal: 20,
          }}
        >
          <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>
            <View>
              <Text style={{ color: 'white', fontSize: 24, fontWeight: 'bold' }}>
                Good {new Date().getHours() < 12 ? 'Morning' : new Date().getHours() < 17 ? 'Afternoon' : 'Evening'}
              </Text>
              <Text style={{ color: 'rgba(255,255,255,0.8)', fontSize: 16 }}>
                {user?.name?.split(' ')[0] || 'Driver'} • Ready to assist you
              </Text>
            </View>
            <View style={{
              backgroundColor: 'rgba(255,255,255,0.2)',
              borderRadius: 20,
              padding: 10,
            }}>
              <Text style={{ color: 'white', fontSize: 24 }}>🚗</Text>
            </View>
          </View>
        </LinearGradient>

        {/* Quick Actions */}
        <View style={{
          backgroundColor: 'white',
          marginHorizontal: 16,
          marginTop: -10,
          borderRadius: 16,
          padding: 16,
          shadowColor: '#000',
          shadowOffset: { width: 0, height: 2 },
          shadowOpacity: 0.1,
          shadowRadius: 8,
          elevation: 4,
        }}>
          <Text style={{ fontSize: 16, fontWeight: '600', color: '#374151', marginBottom: 12 }}>
            Quick Actions
          </Text>
          <View style={{
            flexDirection: 'row',
            flexWrap: 'wrap',
            justifyContent: 'space-between'
          }}>
            {quickActions.map((action) => (
              <TouchableOpacity
                key={action.id}
                style={{
                  backgroundColor: action.bgColor,
                  borderRadius: 12,
                  padding: 12,
                  width: '48%',
                  marginBottom: 8,
                  borderWidth: 1,
                  borderColor: action.color + '20',
                }}
                onPress={() => sendMessage(action.message)}
              >
                <Text style={{ fontSize: 20, marginBottom: 4 }}>{action.icon}</Text>
                <Text style={{
                  fontSize: 14,
                  fontWeight: '600',
                  color: action.color,
                  marginBottom: 2
                }}>
                  {action.title}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* Chat Messages */}
        <View style={{
          flex: 1,
          marginHorizontal: 16,
          marginTop: 16,
          marginBottom: 16,
          backgroundColor: 'white',
          borderRadius: 16,
          shadowColor: '#000',
          shadowOffset: { width: 0, height: 2 },
          shadowOpacity: 0.1,
          shadowRadius: 8,
          elevation: 4,
        }}>
          <View style={{
            borderBottomWidth: 1,
            borderBottomColor: '#f3f4f6',
            padding: 16,
          }}>
            <Text style={{ fontSize: 16, fontWeight: '600', color: '#374151' }}>
              AI Assistant Chat
            </Text>
            <Text style={{ fontSize: 12, color: '#6b7280', marginTop: 2 }}>
              {conversations.length - 1} messages • Powered by Sarathi AI
            </Text>
          </View>

          <ScrollView
            ref={scrollViewRef}
            style={{ flex: 1, padding: 16 }}
            showsVerticalScrollIndicator={false}
          >
            {conversations.map((conv) => (
              <View
                key={conv.id}
                style={{
                  alignSelf: conv.isBot ? 'flex-start' : 'flex-end',
                  marginBottom: 16,
                  maxWidth: '85%',
                }}
              >
                {/* Message bubble */}
                <View
                  style={{
                    backgroundColor: conv.isBot ? '#f8fafc' : '#3b82f6',
                    padding: 16,
                    borderRadius: 20,
                    borderBottomLeftRadius: conv.isBot ? 4 : 20,
                    borderBottomRightRadius: conv.isBot ? 20 : 4,
                    borderWidth: conv.isBot ? 1 : 0,
                    borderColor: '#e5e7eb',
                  }}
                >
                  {/* Intent badge for bot messages */}
                  {conv.isBot && conv.intent && conv.intent !== 'welcome' && conv.intent !== 'error' && (
                    <View style={{
                      backgroundColor:
                        conv.intent === 'weather' ? '#dbeafe' :
                          conv.intent === 'earnings' ? '#d1fae5' :
                            conv.intent === 'garage' ? '#fed7aa' : '#f3f4f6',
                      paddingHorizontal: 8,
                      paddingVertical: 4,
                      borderRadius: 12,
                      marginBottom: 8,
                      alignSelf: 'flex-start'
                    }}>
                      <Text style={{
                        fontSize: 12,
                        fontWeight: '600',
                        color:
                          conv.intent === 'weather' ? '#1d4ed8' :
                            conv.intent === 'earnings' ? '#059669' :
                              conv.intent === 'garage' ? '#ea580c' : '#374151'
                      }}>
                        {conv.intent === 'weather' ? '🌤️ Weather' :
                          conv.intent === 'earnings' ? '💰 Earnings' :
                            conv.intent === 'garage' ? '🔧 Mechanics' :
                              conv.intent.charAt(0).toUpperCase() + conv.intent.slice(1)}
                      </Text>
                    </View>
                  )}

                  <Text style={{
                    color: conv.isBot ? '#374151' : 'white',
                    fontSize: 16,
                    lineHeight: 22,
                  }}>
                    {conv.message}
                  </Text>

                  {/* Timestamp */}
                  <Text style={{
                    fontSize: 12,
                    color: conv.isBot ? '#9ca3af' : 'rgba(255,255,255,0.7)',
                    marginTop: 6,
                    textAlign: conv.isBot ? 'left' : 'right',
                  }}>
                    {conv.timestamp.toLocaleTimeString([], {
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </Text>
                </View>
              </View>
            ))}

            {/* Typing indicator */}
            {loading && (
              <View style={{
                alignSelf: 'flex-start',
                marginBottom: 16,
              }}>
                <View style={{
                  backgroundColor: '#f8fafc',
                  padding: 16,
                  borderRadius: 20,
                  borderBottomLeftRadius: 4,
                  borderWidth: 1,
                  borderColor: '#e5e7eb',
                  flexDirection: 'row',
                  alignItems: 'center',
                }}>
                  <ActivityIndicator color="#3b82f6" size="small" />
                  <Text style={{ color: '#6b7280', marginLeft: 8, fontStyle: 'italic' }}>
                    AI is thinking...
                  </Text>
                </View>
              </View>
            )}
          </ScrollView>

          {/* Input area */}
          <View style={{
            flexDirection: 'row',
            alignItems: 'flex-end',
            padding: 16,
            borderTopWidth: 1,
            borderTopColor: '#f3f4f6',
          }}>
            <TextInput
              style={{
                flex: 1,
                borderWidth: 1,
                borderColor: '#d1d5db',
                borderRadius: 24,
                paddingHorizontal: 16,
                paddingVertical: 12,
                marginRight: 12,
                backgroundColor: '#f9fafb',
                fontSize: 16,
                maxHeight: 100,
              }}
              value={message}
              onChangeText={setMessage}
              placeholder="Ask about earnings, weather, mechanics..."
              placeholderTextColor="#9ca3af"
              multiline
              textAlignVertical="top"
              onSubmitEditing={() => sendMessage()}
              returnKeyType="send"
            />
            <TouchableOpacity
              style={{
                backgroundColor: (loading || !message.trim()) ? '#9ca3af' : '#3b82f6',
                borderRadius: 24,
                width: 48,
                height: 48,
                justifyContent: 'center',
                alignItems: 'center',
                shadowColor: '#3b82f6',
                shadowOffset: { width: 0, height: 2 },
                shadowOpacity: 0.3,
                shadowRadius: 4,
                elevation: 4,
              }}
              onPress={() => sendMessage()}
              disabled={loading || !message.trim()}
            >
              {loading ? (
                <ActivityIndicator color="white" size="small" />
              ) : (
                <Text style={{ color: 'white', fontSize: 18, fontWeight: 'bold' }}>
                  ➤
                </Text>
              )}
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </KeyboardAvoidingView>
  );
}
