import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  Modal,
  TextInput,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { userAPI } from '../services/api';

interface Vehicle {
  id: number;
  make: string;
  model: string;
  year: number;
  license_plate: string;
  vehicle_type: string;
}

export default function GarageScreen() {
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [newVehicle, setNewVehicle] = useState({
    make: '',
    model: '',
    year: new Date().getFullYear(),
    license_plate: '',
    vehicle_type: 'car',
  });

  useEffect(() => {
    loadVehicles();
  }, []);

  const loadVehicles = async () => {
    try {
      const data = await userAPI.getVehicles();
      setVehicles(data);
    } catch (error) {
      console.error('Failed to load vehicles:', error);
    }
  };

  const handleAddVehicle = async () => {
    if (!newVehicle.make || !newVehicle.model || !newVehicle.license_plate) {
      Alert.alert('Error', 'Please fill in all fields');
      return;
    }

    try {
      await userAPI.addVehicle(newVehicle);
      setModalVisible(false);
      setNewVehicle({
        make: '',
        model: '',
        year: new Date().getFullYear(),
        license_plate: '',
        vehicle_type: 'car',
      });
      loadVehicles();
      Alert.alert('Success', 'Vehicle added successfully!');
    } catch (error: any) {
      Alert.alert('Error', error.response?.data?.detail || 'Failed to add vehicle');
    }
  };

  const getVehicleIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case 'motorcycle':
        return 'bicycle';
      case 'truck':
        return 'bus';
      case 'suv':
        return 'car-sport';
      default:
        return 'car';
    }
  };

  return (
    <View className="flex-1 bg-gray-50">
      <ScrollView className="flex-1 p-4">
        {/* Header */}
        <View className="flex-row justify-between items-center mb-6">
          <View>
            <Text className="text-2xl font-bold text-gray-800">My Garage</Text>
            <Text className="text-gray-500">{vehicles.length} vehicles</Text>
          </View>
          <TouchableOpacity
            className="bg-primary-500 rounded-full p-3 active:bg-primary-600"
            onPress={() => setModalVisible(true)}
          >
            <Ionicons name="add" size={28} color="white" />
          </TouchableOpacity>
        </View>

        {/* Vehicle List */}
        {vehicles.length === 0 ? (
          <View className="items-center justify-center py-20">
            <Text className="text-6xl mb-4">🚗</Text>
            <Text className="text-gray-400 text-center text-lg">
              No vehicles yet{'\n'}Tap + to add your first vehicle
            </Text>
          </View>
        ) : (
          vehicles.map((vehicle) => (
            <View key={vehicle.id} className="bg-white rounded-2xl p-5 mb-4 shadow-sm">
              <View className="flex-row items-center mb-3">
                <View className="bg-primary-100 rounded-full p-3 mr-4">
                  <Ionicons name={getVehicleIcon(vehicle.vehicle_type) as any} size={32} color="#0ea5e9" />
                </View>
                <View className="flex-1">
                  <Text className="text-xl font-bold text-gray-800">
                    {vehicle.make} {vehicle.model}
                  </Text>
                  <Text className="text-gray-500">{vehicle.year}</Text>
                </View>
              </View>
              <View className="border-t border-gray-100 pt-3">
                <View className="flex-row justify-between">
                  <Text className="text-gray-600">License Plate</Text>
                  <Text className="font-semibold text-gray-800">{vehicle.license_plate}</Text>
                </View>
                <View className="flex-row justify-between mt-2">
                  <Text className="text-gray-600">Type</Text>
                  <Text className="font-semibold text-gray-800 capitalize">{vehicle.vehicle_type}</Text>
                </View>
              </View>
            </View>
          ))
        )}
      </ScrollView>

      {/* Add Vehicle Modal */}
      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => setModalVisible(false)}
      >
        <View className="flex-1 justify-end bg-black/50">
          <View className="bg-white rounded-t-3xl p-6">
            <View className="flex-row justify-between items-center mb-6">
              <Text className="text-2xl font-bold text-gray-800">Add Vehicle</Text>
              <TouchableOpacity onPress={() => setModalVisible(false)}>
                <Ionicons name="close" size={28} color="#666" />
              </TouchableOpacity>
            </View>

            <View className="mb-4">
              <Text className="text-sm font-medium text-gray-700 mb-2">Make</Text>
              <TextInput
                className="bg-gray-100 rounded-xl px-4 py-3"
                placeholder="e.g., Toyota, Honda"
                value={newVehicle.make}
                onChangeText={(text) => setNewVehicle({ ...newVehicle, make: text })}
              />
            </View>

            <View className="mb-4">
              <Text className="text-sm font-medium text-gray-700 mb-2">Model</Text>
              <TextInput
                className="bg-gray-100 rounded-xl px-4 py-3"
                placeholder="e.g., Camry, Civic"
                value={newVehicle.model}
                onChangeText={(text) => setNewVehicle({ ...newVehicle, model: text })}
              />
            </View>

            <View className="mb-4">
              <Text className="text-sm font-medium text-gray-700 mb-2">Year</Text>
              <TextInput
                className="bg-gray-100 rounded-xl px-4 py-3"
                placeholder="e.g., 2023"
                value={newVehicle.year.toString()}
                onChangeText={(text) => setNewVehicle({ ...newVehicle, year: parseInt(text) || new Date().getFullYear() })}
                keyboardType="numeric"
              />
            </View>

            <View className="mb-4">
              <Text className="text-sm font-medium text-gray-700 mb-2">License Plate</Text>
              <TextInput
                className="bg-gray-100 rounded-xl px-4 py-3"
                placeholder="e.g., ABC-1234"
                value={newVehicle.license_plate}
                onChangeText={(text) => setNewVehicle({ ...newVehicle, license_plate: text })}
                autoCapitalize="characters"
              />
            </View>

            <TouchableOpacity
              className="bg-primary-500 rounded-xl py-4 active:bg-primary-600"
              onPress={handleAddVehicle}
            >
              <Text className="text-white text-center text-lg font-bold">Add Vehicle</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
}
