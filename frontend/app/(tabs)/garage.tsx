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

interface Vehicle {
    id: string;
    make: string;
    model: string;
    year: number;
    color: string;
    mileage: number;
    fuelEfficiency: number;
}

export default function GarageScreen() {
    const [vehicles, setVehicles] = useState<Vehicle[]>([
        {
            id: '1',
            make: 'Toyota',
            model: 'Camry',
            year: 2022,
            color: 'Silver',
            mileage: 15420,
            fuelEfficiency: 32,
        },
    ]);

    const [showAddModal, setShowAddModal] = useState(false);
    const [newVehicle, setNewVehicle] = useState({
        make: '',
        model: '',
        year: '',
        color: '',
        mileage: '',
        fuelEfficiency: '',
    });

    const addVehicle = () => {
        if (!newVehicle.make || !newVehicle.model || !newVehicle.year) {
            Alert.alert('Error', 'Please fill in all required fields');
            return;
        }

        const vehicle: Vehicle = {
            id: Date.now().toString(),
            make: newVehicle.make,
            model: newVehicle.model,
            year: parseInt(newVehicle.year),
            color: newVehicle.color,
            mileage: parseInt(newVehicle.mileage) || 0,
            fuelEfficiency: parseFloat(newVehicle.fuelEfficiency) || 0,
        };

        setVehicles([...vehicles, vehicle]);
        setShowAddModal(false);
        setNewVehicle({
            make: '',
            model: '',
            year: '',
            color: '',
            mileage: '',
            fuelEfficiency: '',
        });
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
                            My Garage
                        </Text>
                        <Text style={{ color: 'rgba(255,255,255,0.9)', fontSize: 16 }}>
                            Manage your vehicles
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
                        <Text style={{ color: 'white', fontWeight: 'bold' }}>+ Add</Text>
                    </TouchableOpacity>
                </View>
            </LinearGradient>

            <ScrollView style={{ flex: 1, padding: 20 }}>
                {vehicles.map((vehicle) => (
                    <View
                        key={vehicle.id}
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
                        <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
                            <Text style={{ fontSize: 20, fontWeight: 'bold', color: '#1f2937' }}>
                                {vehicle.year} {vehicle.make} {vehicle.model}
                            </Text>
                            <View style={{
                                backgroundColor: '#0ea5e9',
                                borderRadius: 20,
                                paddingHorizontal: 12,
                                paddingVertical: 4,
                            }}>
                                <Text style={{ color: 'white', fontSize: 12, fontWeight: 'bold' }}>
                                    Primary
                                </Text>
                            </View>
                        </View>

                        <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 16 }}>
                            <View style={{ flex: 1, minWidth: 120 }}>
                                <Text style={{ color: '#6b7280', fontSize: 14, marginBottom: 4 }}>Color</Text>
                                <Text style={{ fontSize: 16, fontWeight: '600', color: '#374151' }}>
                                    {vehicle.color}
                                </Text>
                            </View>
                            <View style={{ flex: 1, minWidth: 120 }}>
                                <Text style={{ color: '#6b7280', fontSize: 14, marginBottom: 4 }}>Mileage</Text>
                                <Text style={{ fontSize: 16, fontWeight: '600', color: '#374151' }}>
                                    {vehicle.mileage.toLocaleString()} mi
                                </Text>
                            </View>
                            <View style={{ flex: 1, minWidth: 120 }}>
                                <Text style={{ color: '#6b7280', fontSize: 14, marginBottom: 4 }}>Fuel Efficiency</Text>
                                <Text style={{ fontSize: 16, fontWeight: '600', color: '#374151' }}>
                                    {vehicle.fuelEfficiency} MPG
                                </Text>
                            </View>
                        </View>

                        <View style={{ marginTop: 16, paddingTop: 16, borderTopWidth: 1, borderTopColor: '#e5e7eb' }}>
                            <Text style={{ fontSize: 16, fontWeight: '600', marginBottom: 8, color: '#374151' }}>
                                Quick Actions
                            </Text>
                            <View style={{ flexDirection: 'row', gap: 12 }}>
                                <TouchableOpacity
                                    style={{
                                        backgroundColor: '#f3f4f6',
                                        borderRadius: 8,
                                        paddingHorizontal: 16,
                                        paddingVertical: 8,
                                    }}
                                >
                                    <Text style={{ color: '#374151', fontWeight: '500' }}>Log Trip</Text>
                                </TouchableOpacity>
                                <TouchableOpacity
                                    style={{
                                        backgroundColor: '#f3f4f6',
                                        borderRadius: 8,
                                        paddingHorizontal: 16,
                                        paddingVertical: 8,
                                    }}
                                >
                                    <Text style={{ color: '#374151', fontWeight: '500' }}>Maintenance</Text>
                                </TouchableOpacity>
                            </View>
                        </View>
                    </View>
                ))}
            </ScrollView>

            <Modal visible={showAddModal} animationType="slide" presentationStyle="pageSheet">
                <View style={{ flex: 1, backgroundColor: 'white' }}>
                    <View style={{ padding: 20, borderBottomWidth: 1, borderBottomColor: '#e5e7eb' }}>
                        <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>
                            <TouchableOpacity onPress={() => setShowAddModal(false)}>
                                <Text style={{ color: '#6b7280', fontSize: 16 }}>Cancel</Text>
                            </TouchableOpacity>
                            <Text style={{ fontSize: 18, fontWeight: 'bold' }}>Add Vehicle</Text>
                            <TouchableOpacity onPress={addVehicle}>
                                <Text style={{ color: '#0ea5e9', fontSize: 16, fontWeight: '600' }}>Save</Text>
                            </TouchableOpacity>
                        </View>
                    </View>

                    <ScrollView style={{ padding: 20 }}>
                        <View style={{ marginBottom: 20 }}>
                            <Text style={{ fontSize: 16, fontWeight: '600', marginBottom: 8, color: '#374151' }}>
                                Make *
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
                                value={newVehicle.make}
                                onChangeText={(text) => setNewVehicle({ ...newVehicle, make: text })}
                                placeholder="Toyota, Honda, Ford..."
                            />
                        </View>

                        <View style={{ marginBottom: 20 }}>
                            <Text style={{ fontSize: 16, fontWeight: '600', marginBottom: 8, color: '#374151' }}>
                                Model *
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
                                value={newVehicle.model}
                                onChangeText={(text) => setNewVehicle({ ...newVehicle, model: text })}
                                placeholder="Camry, Civic, F-150..."
                            />
                        </View>

                        <View style={{ marginBottom: 20 }}>
                            <Text style={{ fontSize: 16, fontWeight: '600', marginBottom: 8, color: '#374151' }}>
                                Year *
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
                                value={newVehicle.year}
                                onChangeText={(text) => setNewVehicle({ ...newVehicle, year: text })}
                                placeholder="2023"
                                keyboardType="numeric"
                            />
                        </View>

                        <View style={{ marginBottom: 20 }}>
                            <Text style={{ fontSize: 16, fontWeight: '600', marginBottom: 8, color: '#374151' }}>
                                Color
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
                                value={newVehicle.color}
                                onChangeText={(text) => setNewVehicle({ ...newVehicle, color: text })}
                                placeholder="Silver, Black, White..."
                            />
                        </View>

                        <View style={{ marginBottom: 20 }}>
                            <Text style={{ fontSize: 16, fontWeight: '600', marginBottom: 8, color: '#374151' }}>
                                Current Mileage
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
                                value={newVehicle.mileage}
                                onChangeText={(text) => setNewVehicle({ ...newVehicle, mileage: text })}
                                placeholder="50000"
                                keyboardType="numeric"
                            />
                        </View>

                        <View style={{ marginBottom: 20 }}>
                            <Text style={{ fontSize: 16, fontWeight: '600', marginBottom: 8, color: '#374151' }}>
                                Fuel Efficiency (MPG)
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
                                value={newVehicle.fuelEfficiency}
                                onChangeText={(text) => setNewVehicle({ ...newVehicle, fuelEfficiency: text })}
                                placeholder="30.5"
                                keyboardType="numeric"
                            />
                        </View>
                    </ScrollView>
                </View>
            </Modal>
        </View>
    );
}