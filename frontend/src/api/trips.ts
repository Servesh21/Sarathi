import api from './client';

export interface Trip {
    id: number;
    start_location: string;
    end_location: string;
    start_time: string;
    end_time?: string;
    earnings: number;
    fuel_cost: number;
    toll_cost: number;
    other_expenses: number;
    net_earnings?: number;
    distance_km?: number;
    duration_minutes?: number;
    platform?: string;
    trip_type: string;
    is_high_value_zone: boolean;
    zone_rating?: number;
    created_at: string;
}

export interface TripStats {
    total_trips: number;
    total_earnings: number;
    total_expenses: number;
    net_earnings: number;
    average_trip_earnings: number;
    high_value_trips: number;
    best_zone?: string;
    best_time_slot?: string;
}

export interface ZoneRecommendation {
    zone_name: string;
    latitude: number;
    longitude: number;
    expected_earnings: number;
    confidence_score: number;
    reason: string;
    best_time: string;
}

export interface CreateTripData {
    start_location: string;
    end_location: string;
    start_time: string;
    earnings: number;
    fuel_cost?: number;
    toll_cost?: number;
    other_expenses?: number;
    platform?: string;
    trip_type?: string;
}

export const tripsAPI = {
    getTrips: async (days?: number): Promise<Trip[]> => {
        const params = days ? { days } : {};
        const response = await api.get<Trip[]>('/trips', { params });
        return response.data;
    },

    createTrip: async (data: CreateTripData): Promise<Trip> => {
        const response = await api.post<Trip>('/trips', data);
        return response.data;
    },

    createTripFromVoice: async (audioFile: FormData): Promise<Trip> => {
        const response = await api.post<Trip>('/trips/voice', audioFile, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

    getTripStats: async (days: number = 30): Promise<TripStats> => {
        const response = await api.get<TripStats>('/trips/stats', { params: { days } });
        return response.data;
    },

    getZoneRecommendations: async (): Promise<ZoneRecommendation[]> => {
        const response = await api.get<ZoneRecommendation[]>('/trips/recommendations/zones');
        return response.data;
    },

    updateTrip: async (id: number, data: Partial<CreateTripData>): Promise<Trip> => {
        const response = await api.patch<Trip>(`/trips/${id}`, data);
        return response.data;
    },

    deleteTrip: async (id: number): Promise<void> => {
        await api.delete(`/trips/${id}`);
    },
};
