import { create } from 'zustand';
import { Vehicle, VehicleHealthCheck, vehiclesAPI } from '../api/vehicles';

interface VehiclesState {
    vehicles: Vehicle[];
    healthChecks: VehicleHealthCheck[];
    selectedVehicle: Vehicle | null;
    isLoading: boolean;
    error: string | null;

    fetchVehicles: () => Promise<void>;
    fetchHealthChecks: (vehicleId: number) => Promise<void>;
    uploadHealthCheckImages: (vehicleId: number, images: FormData) => Promise<void>;
    setSelectedVehicle: (vehicle: Vehicle) => void;
}

export const useVehiclesStore = create<VehiclesState>((set) => ({
    vehicles: [],
    healthChecks: [],
    selectedVehicle: null,
    isLoading: false,
    error: null,

    fetchVehicles: async () => {
        set({ isLoading: true, error: null });
        try {
            const vehicles = await vehiclesAPI.getVehicles();
            set({
                vehicles,
                selectedVehicle: vehicles.length > 0 ? vehicles[0] : null,
                isLoading: false
            });
        } catch (error: any) {
            set({
                error: error.response?.data?.detail || 'Failed to fetch vehicles',
                isLoading: false
            });
        }
    },

    fetchHealthChecks: async (vehicleId: number) => {
        set({ isLoading: true, error: null });
        try {
            const healthChecks = await vehiclesAPI.getHealthChecks(vehicleId);
            set({ healthChecks, isLoading: false });
        } catch (error: any) {
            set({
                error: error.response?.data?.detail || 'Failed to fetch health checks',
                isLoading: false
            });
        }
    },

    uploadHealthCheckImages: async (vehicleId: number, images: FormData) => {
        set({ isLoading: true, error: null });
        try {
            const healthCheck = await vehiclesAPI.uploadHealthCheckImages(vehicleId, images);
            set((state) => ({
                healthChecks: [healthCheck, ...state.healthChecks],
                isLoading: false
            }));
        } catch (error: any) {
            set({
                error: error.response?.data?.detail || 'Failed to upload images',
                isLoading: false
            });
            throw error;
        }
    },

    setSelectedVehicle: (vehicle: Vehicle) => {
        set({ selectedVehicle: vehicle });
    },
}));
