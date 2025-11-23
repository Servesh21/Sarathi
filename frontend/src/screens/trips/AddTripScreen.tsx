import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, Alert, SafeAreaView } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { Audio } from 'expo-av';
import { useTripsStore } from '../../store/tripsStore';
import { Card, Button, Input } from '../../components';

export default function AddTripScreen({ navigation }: any) {
    const [recording, setRecording] = useState<Audio.Recording | null>(null);
    const [isRecording, setIsRecording] = useState(false);
    const [manualEntry, setManualEntry] = useState(false);
    const [tripData, setTripData] = useState({
        pickup: '',
        dropoff: '',
        distance: '',
        fare: '',
        notes: ''
    });
    const { uploadVoiceTrip, isLoading } = useTripsStore();

    useEffect(() => {
        return () => {
            if (recording) {
                recording.stopAndUnloadAsync();
            }
        };
    }, [recording]);

    const startRecording = async () => {
        try {
            const permission = await Audio.requestPermissionsAsync();
            if (!permission.granted) {
                Alert.alert('Permission required', 'Please grant microphone permission');
                return;
            }

            await Audio.setAudioModeAsync({
                allowsRecordingIOS: true,
                playsInSilentModeIOS: true,
            });

            const { recording: newRecording } = await Audio.Recording.createAsync(
                Audio.RecordingOptionsPresets.HIGH_QUALITY
            );
            setRecording(newRecording);
            setIsRecording(true);
        } catch (err) {
            console.error('Failed to start recording', err);
            Alert.alert('Error', 'Failed to start recording');
        }
    };

    const stopRecording = async () => {
        if (!recording) return;

        try {
            setIsRecording(false);
            await recording.stopAndUnloadAsync();
            const uri = recording.getURI();

            if (uri) {
                const formData = new FormData();

                formData.append('audio_file', {
                    uri,
                    type: 'audio/m4a',
                    name: 'trip_audio.m4a',
                } as any);

                await uploadVoiceTrip(formData);
                Alert.alert('Success', 'Trip logged successfully!', [
                    { text: 'OK', onPress: () => navigation.goBack() }
                ]);
            }
        } catch (err) {
            console.error('Failed to stop recording', err);
            Alert.alert('Error', 'Failed to save trip');
        }
    };

    const handleManualSubmit = () => {
        // Implement manual trip submission
        Alert.alert('Success', 'Trip logged successfully!', [
            { text: 'OK', onPress: () => navigation.goBack() }
        ]);
    };

    return (
        <SafeAreaView className="flex-1 bg-gray-50">
            {/* Header */}
            <LinearGradient
                colors={['#10b981', '#059669']}
                className="px-4 pt-4 pb-8"
            >
                <View className="flex-row items-center">
                    <Button
                        title=""
                        onPress={() => navigation.goBack()}
                        variant="secondary"
                        size="sm"
                        icon="arrow-back"
                        className="w-10 h-10 mr-3"
                    />
                    <View className="flex-1">
                        <Text className="text-white text-2xl font-bold">Log Your Trip</Text>
                        <Text className="text-green-100 mt-1">Add trip details quickly</Text>
                    </View>
                </View>
            </LinearGradient>

            <ScrollView className="flex-1 -mt-4" showsVerticalScrollIndicator={false}>
                <View className="px-4 pb-6">
                    {/* Method Selection */}
                    <View className="flex-row mb-6 -mt-2">
                        <Button
                            title="Voice Entry"
                            onPress={() => setManualEntry(false)}
                            variant={!manualEntry ? "primary" : "outline"}
                            size="sm"
                            icon="mic"
                            className="flex-1 mr-2"
                        />
                        <Button
                            title="Manual Entry"
                            onPress={() => setManualEntry(true)}
                            variant={manualEntry ? "primary" : "outline"}
                            size="sm"
                            icon="create"
                            className="flex-1 ml-2"
                        />
                    </View>

                    {!manualEntry ? (
                        /* Voice Recording Card */
                        <Card
                            title="Voice Recording"
                            subtitle="Speak naturally to log your trip"
                            icon="mic-outline"
                            iconColor="#10b981"
                        >
                            <View className="bg-gray-50 rounded-xl p-4 mb-6">
                                <Text className="text-gray-600 text-center">
                                    💡 "I went from Andheri to Bandra, fare was ₹250, distance 8 km"
                                </Text>
                            </View>

                            <View className="items-center">
                                {!isRecording ? (
                                    <View className="items-center">
                                        <LinearGradient
                                            colors={['#10b981', '#059669']}
                                            className="rounded-full w-24 h-24 justify-center items-center mb-4"
                                        >
                                            <Ionicons name="mic" size={32} color="white" />
                                        </LinearGradient>
                                        <Button
                                            title="Start Recording"
                                            onPress={startRecording}
                                            loading={isLoading}
                                            icon="play"
                                            className="w-full"
                                        />
                                    </View>
                                ) : (
                                    <View className="items-center">
                                        <LinearGradient
                                            colors={['#ef4444', '#dc2626']}
                                            className="rounded-full w-24 h-24 justify-center items-center mb-4"
                                        >
                                            <Ionicons name="stop" size={32} color="white" />
                                        </LinearGradient>
                                        <Text className="text-center text-gray-600 mb-4">Recording...</Text>
                                        <Button
                                            title="Stop & Save"
                                            onPress={stopRecording}
                                            variant="danger"
                                            icon="stop"
                                            className="w-full"
                                        />
                                    </View>
                                )}
                            </View>
                        </Card>
                    ) : (
                        /* Manual Entry Form */
                        <Card
                            title="Manual Entry"
                            subtitle="Enter trip details manually"
                            icon="create-outline"
                            iconColor="#3b82f6"
                        >
                            <Input
                                label="Pickup Location"
                                placeholder="e.g., Andheri Station"
                                value={tripData.pickup}
                                onChangeText={(text) => setTripData({ ...tripData, pickup: text })}
                                leftIcon="location"
                            />

                            <Input
                                label="Drop-off Location"
                                placeholder="e.g., Bandra West"
                                value={tripData.dropoff}
                                onChangeText={(text) => setTripData({ ...tripData, dropoff: text })}
                                leftIcon="flag"
                            />

                            <View className="flex-row space-x-2">
                                <Input
                                    label="Distance (km)"
                                    placeholder="8.5"
                                    value={tripData.distance}
                                    onChangeText={(text) => setTripData({ ...tripData, distance: text })}
                                    keyboardType="numeric"
                                    leftIcon="speedometer"
                                    containerClassName="flex-1 mr-2"
                                />

                                <Input
                                    label="Fare (₹)"
                                    placeholder="250"
                                    value={tripData.fare}
                                    onChangeText={(text) => setTripData({ ...tripData, fare: text })}
                                    keyboardType="numeric"
                                    leftIcon="wallet"
                                    containerClassName="flex-1 ml-2"
                                />
                            </View>

                            <Input
                                label="Notes (Optional)"
                                placeholder="Any additional details..."
                                value={tripData.notes}
                                onChangeText={(text) => setTripData({ ...tripData, notes: text })}
                                leftIcon="document-text"
                                containerClassName="mb-2"
                            />

                            <Button
                                title="Save Trip"
                                onPress={handleManualSubmit}
                                icon="checkmark"
                                className="w-full"
                            />
                        </Card>
                    )}

                    {/* Tips Card */}
                    <Card
                        title="💡 Pro Tips"
                        className="mt-4"
                    >
                        <View className="space-y-2">
                            <View className="flex-row items-center">
                                <Ionicons name="checkmark-circle" size={16} color="#10b981" />
                                <Text className="text-gray-700 ml-2">Speak clearly and mention all details</Text>
                            </View>
                            <View className="flex-row items-center">
                                <Ionicons name="checkmark-circle" size={16} color="#10b981" />
                                <Text className="text-gray-700 ml-2">AI extracts pickup, drop, fare automatically</Text>
                            </View>
                            <View className="flex-row items-center">
                                <Ionicons name="checkmark-circle" size={16} color="#10b981" />
                                <Text className="text-gray-700 ml-2">Works in multiple languages</Text>
                            </View>
                        </View>
                    </Card>
                </View>
            </ScrollView>
        </SafeAreaView>
    );
}
