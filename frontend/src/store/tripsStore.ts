import { create } from 'zustand';
import { tripsAPI, Trip, TripStats, ZoneRecommendation } from '../api/trips';

interface TripsState {
    trips: Trip[];
    stats: TripStats | null;
    zoneRecommendations: ZoneRecommendation[];
    isLoading: boolean;
    error: string | null;

    fetchTrips: (days?: number) => Promise<void>;
    fetchStats: (days?: number) => Promise<void>;
    fetchZoneRecommendations: () => Promise<void>;
    createTrip: (data: any) => Promise<void>;
    uploadVoiceTrip: (audioFile: FormData) => Promise<void>;
}

export const useTripsStore = create<TripsState>((set) => ({
    trips: [],
    stats: null,
    zoneRecommendations: [],
    isLoading: false,
    error: null,

    fetchTrips: async (days?: number) => {
        set({ isLoading: true, error: null });
        try {
            const trips = await tripsAPI.getTrips(days);
            set({ trips, isLoading: false });
        } catch (error: any) {
            set({
                error: error.response?.data?.detail || 'Failed to fetch trips',
                isLoading: false
            });
        }
    },

    fetchStats: async (days?: number) => {
        set({ isLoading: true, error: null });
        try {
            const stats = await tripsAPI.getTripStats(days);
            set({ stats, isLoading: false });
        } catch (error: any) {
            set({
                error: error.response?.data?.detail || 'Failed to fetch stats',
                isLoading: false
            });
        }
    },

    fetchZoneRecommendations: async () => {
        set({ isLoading: true, error: null });
        try {
            const zoneRecommendations = await tripsAPI.getZoneRecommendations();
            set({ zoneRecommendations, isLoading: false });
        } catch (error: any) {
            set({
                error: error.response?.data?.detail || 'Failed to fetch recommendations',
                isLoading: false
            });
        }
    },

    createTrip: async (data: any) => {
        set({ isLoading: true, error: null });
        try {
            const newTrip = await tripsAPI.createTrip(data);
            set((state) => ({
                trips: [newTrip, ...state.trips],
                isLoading: false
            }));
        } catch (error: any) {
            set({
                error: error.response?.data?.detail || 'Failed to create trip',
                isLoading: false
            });
            throw error;
        }
    },

    uploadVoiceTrip: async (audioFile: FormData) => {
        set({ isLoading: true, error: null });
        try {
            const newTrip = await tripsAPI.createTripFromVoice(audioFile);
            set((state) => ({
                trips: [newTrip, ...state.trips],
                isLoading: false
            }));
        } catch (error: any) {
            set({
                error: error.response?.data?.detail || 'Failed to upload voice trip',
                isLoading: false
            });
            throw error;
        }
    },
}));
