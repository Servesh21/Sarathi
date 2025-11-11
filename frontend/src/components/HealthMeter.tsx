import React from 'react';
import { View, Text } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface HealthMeterProps {
  score: number; // 0-100
}

export default function HealthMeter({ score }: HealthMeterProps) {
  const getColor = () => {
    if (score >= 80) return 'bg-green-500';
    if (score >= 60) return 'bg-yellow-500';
    if (score >= 40) return 'bg-orange-500';
    return 'bg-red-500';
  };

  const getEmoji = () => {
    if (score >= 80) return '😊';
    if (score >= 60) return '😐';
    if (score >= 40) return '😟';
    return '😰';
  };

  const getStatus = () => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
    return 'Needs Attention';
  };

  return (
    <View className="bg-white/20 rounded-2xl p-4">
      <View className="flex-row items-center justify-between mb-2">
        <View className="flex-row items-center">
          <Text className="text-2xl mr-2">{getEmoji()}</Text>
          <Text className="text-white text-lg font-semibold">Driver Health</Text>
        </View>
        <Text className="text-white text-2xl font-bold">{score}%</Text>
      </View>
      
      <View className="bg-white/30 rounded-full h-2 overflow-hidden mb-2">
        <View
          className={`h-full ${getColor()} rounded-full`}
          style={{ width: `${score}%` }}
        />
      </View>
      
      <Text className="text-white/80 text-sm">{getStatus()}</Text>
    </View>
  );
}
