import React, { useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  TextInput,
  RefreshControl,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../hooks/useAuth';
import VoiceInputButton from '../components/VoiceInputButton';
import HealthMeter from '../components/HealthMeter';

export default function DashboardScreen() {
  const { user, logout } = useAuth();
  const [query, setQuery] = useState('');
  const [chatHistory, setChatHistory] = useState<Array<{ type: 'user' | 'agent'; message: string }>>([]);
  const [refreshing, setRefreshing] = useState(false);

  const onRefresh = React.useCallback(() => {
    setRefreshing(true);
    // Fetch latest data
    setTimeout(() => setRefreshing(false), 1000);
  }, []);

  const handleSendMessage = () => {
    if (!query.trim()) return;

    // Add user message
    setChatHistory([...chatHistory, { type: 'user', message: query }]);
    
    // Simulate agent response (replace with actual API call)
    setTimeout(() => {
      setChatHistory((prev) => [
        ...prev,
        { type: 'agent', message: 'I received your message: "' + query + '". How can I assist you further?' }
      ]);
    }, 500);

    setQuery('');
  };

  return (
    <View className="flex-1 bg-gray-50">
      <ScrollView
        className="flex-1"
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
      >
        {/* Header */}
        <View className="bg-primary-500 rounded-b-3xl p-6 pb-8">
          <View className="flex-row justify-between items-center mb-4">
            <View>
              <Text className="text-white/80 text-sm">Welcome back,</Text>
              <Text className="text-white text-2xl font-bold">{user?.full_name || 'Driver'}</Text>
            </View>
            <TouchableOpacity onPress={logout}>
              <Ionicons name="log-out-outline" size={28} color="white" />
            </TouchableOpacity>
          </View>

          {/* Health Meter */}
          <HealthMeter score={85} />
        </View>

        {/* Stats Cards */}
        <View className="px-4 -mt-4 mb-4">
          <View className="flex-row justify-between">
            <View className="bg-white rounded-2xl p-4 flex-1 mr-2 shadow-sm">
              <Text className="text-gray-500 text-xs mb-1">Today's Earnings</Text>
              <Text className="text-2xl font-bold text-green-600">$124</Text>
              <Text className="text-xs text-gray-400 mt-1">↑ 12% vs yesterday</Text>
            </View>
            <View className="bg-white rounded-2xl p-4 flex-1 ml-2 shadow-sm">
              <Text className="text-gray-500 text-xs mb-1">Total Trips</Text>
              <Text className="text-2xl font-bold text-primary-600">8</Text>
              <Text className="text-xs text-gray-400 mt-1">This week: 45</Text>
            </View>
          </View>
        </View>

        {/* Quick Actions */}
        <View className="px-4 mb-4">
          <Text className="text-lg font-bold text-gray-800 mb-3">Quick Actions</Text>
          <View className="flex-row flex-wrap">
            <TouchableOpacity className="bg-white rounded-xl p-4 mr-3 mb-3 items-center w-24 shadow-sm">
              <Ionicons name="map-outline" size={32} color="#0ea5e9" />
              <Text className="text-xs text-gray-600 mt-2 text-center">Navigate</Text>
            </TouchableOpacity>
            <TouchableOpacity className="bg-white rounded-xl p-4 mr-3 mb-3 items-center w-24 shadow-sm">
              <Ionicons name="sunny-outline" size={32} color="#f59e0b" />
              <Text className="text-xs text-gray-600 mt-2 text-center">Weather</Text>
            </TouchableOpacity>
            <TouchableOpacity className="bg-white rounded-xl p-4 mr-3 mb-3 items-center w-24 shadow-sm">
              <Ionicons name="trending-up-outline" size={32} color="#10b981" />
              <Text className="text-xs text-gray-600 mt-2 text-center">Earnings</Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* Chat Interface */}
        <View className="px-4 mb-4">
          <Text className="text-lg font-bold text-gray-800 mb-3">Chat with Sarathi</Text>
          <View className="bg-white rounded-2xl p-4 min-h-[300px] shadow-sm">
            {chatHistory.length === 0 ? (
              <View className="flex-1 justify-center items-center py-12">
                <Text className="text-6xl mb-4">🤖</Text>
                <Text className="text-gray-400 text-center">
                  Ask me anything about routes,{'\n'}earnings, or weather conditions!
                </Text>
              </View>
            ) : (
              <ScrollView className="mb-4">
                {chatHistory.map((chat, index) => (
                  <View
                    key={index}
                    className={`mb-3 ${chat.type === 'user' ? 'items-end' : 'items-start'}`}
                  >
                    <View
                      className={`rounded-2xl px-4 py-2 max-w-[80%] ${
                        chat.type === 'user' ? 'bg-primary-500' : 'bg-gray-100'
                      }`}
                    >
                      <Text className={chat.type === 'user' ? 'text-white' : 'text-gray-800'}>
                        {chat.message}
                      </Text>
                    </View>
                  </View>
                ))}
              </ScrollView>
            )}
          </View>
        </View>
      </ScrollView>

      {/* Input Area */}
      <View className="bg-white border-t border-gray-200 p-4">
        <View className="flex-row items-center">
          <TextInput
            className="flex-1 bg-gray-100 rounded-full px-4 py-3 mr-2"
            placeholder="Type your message..."
            value={query}
            onChangeText={setQuery}
            onSubmitEditing={handleSendMessage}
          />
          <VoiceInputButton onVoiceInput={(text) => setQuery(text)} />
          <TouchableOpacity
            className="bg-primary-500 rounded-full p-3 ml-2 active:bg-primary-600"
            onPress={handleSendMessage}
          >
            <Ionicons name="send" size={24} color="white" />
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}
