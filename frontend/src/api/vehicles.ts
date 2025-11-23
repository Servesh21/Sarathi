import api from './client';

export interface Vehicle {
    id: number;
    vehicle_number: string;
    vehicle_type: string;
    make?: string;
    model?: string;
    year?: number;
    current_odometer_km: number;
    insurance_expiry?: string;
    last_service_date?: string;
    next_service_due_km?: number;
    created_at: string;
}

export interface VehicleHealthCheck {
    id: number;
    vehicle_id: number;
    check_type: string;
    image_urls?: string[];
    ai_analysis?: string;
    detected_issues?: any[];
    severity_score?: number;
    tire_condition?: string;
    engine_oil_level?: string;
    brake_condition?: string;
    battery_health?: string;
    body_damage?: string;
    immediate_action_required: boolean;
    recommendations?: string;
    estimated_repair_cost?: number;
    created_at: string;
}

export interface CreateVehicleData {
    vehicle_number: string;
    vehicle_type: string;
    make?: string;
    model?: string;
    year?: number;
}

export const vehiclesAPI = {
    getVehicles: async (): Promise<Vehicle[]> => {
        const response = await api.get<Vehicle[]>('/vehicles');
        return response.data;
    },

    createVehicle: async (data: CreateVehicleData): Promise<Vehicle> => {
        const response = await api.post<Vehicle>('/vehicles', data);
        return response.data;
    },

    getVehicle: async (id: number): Promise<Vehicle> => {
        const response = await api.get<Vehicle>(`/vehicles/${id}`);
        return response.data;
    },

    updateVehicle: async (id: number, data: Partial<CreateVehicleData>): Promise<Vehicle> => {
        const response = await api.patch<Vehicle>(`/vehicles/${id}`, data);
        return response.data;
    },

    uploadHealthCheckImages: async (
        vehicleId: number,
        images: FormData
    ): Promise<VehicleHealthCheck> => {
        const response = await api.post<VehicleHealthCheck>(
            `/vehicles/${vehicleId}/health-check`,
            images,
            {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            }
        );
        return response.data;
    },

    getHealthChecks: async (vehicleId: number): Promise<VehicleHealthCheck[]> => {
        const response = await api.get<VehicleHealthCheck[]>(`/vehicles/${vehicleId}/health-checks`);
        return response.data;
    },

    getHealthCheck: async (vehicleId: number, checkId: number): Promise<VehicleHealthCheck> => {
        const response = await api.get<VehicleHealthCheck>(
            `/vehicles/${vehicleId}/health-checks/${checkId}`
        );
        return response.data;
    },
};
