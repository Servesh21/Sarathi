import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface VoiceInputButtonProps {
  onVoiceInput: (text: string) => void;
}

export default function VoiceInputButton({ onVoiceInput }: VoiceInputButtonProps) {
  const [isRecording, setIsRecording] = React.useState(false);

  const handleVoiceInput = () => {
    // TODO: Implement actual voice recording and speech-to-text
    setIsRecording(!isRecording);
    
    // Simulate voice input (replace with actual implementation)
    if (!isRecording) {
      setTimeout(() => {
        setIsRecording(false);
        onVoiceInput("Sample voice input text");
      }, 2000);
    }
  };

  return (
    <TouchableOpacity
      className={`rounded-full p-3 ${isRecording ? 'bg-red-500' : 'bg-primary-500'} active:opacity-80`}
      onPress={handleVoiceInput}
    >
      <Ionicons 
        name={isRecording ? "stop" : "mic"} 
        size={24} 
        color="white" 
      />
    </TouchableOpacity>
  );
}
