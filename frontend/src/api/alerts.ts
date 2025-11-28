import api from './client';

export interface Alert {
    id: number;
    alert_type: string;
    title: string;
    message: string;
    priority: string;
    action_required: boolean;
    is_read: boolean;
    status: string;
    created_at: string;
}

export interface AgentQuery {
    query: string;
    context?: any;
}

export interface AgentResponse {
    response: string;
    recommendations: any[];
    action_items: string[];
    query_type: string;
    analysis?: any;
    // NEW FIELDS FOR VOICE
    audio_url?: string | null;     
    transcription?: string; 
}

export const alertsAPI = {
    getAlerts: async (): Promise<Alert[]> => {
        const response = await api.get<Alert[]>('/alerts');
        return response.data;
    },

    markAsRead: async (alertId: number): Promise<Alert> => {
        const response = await api.post<Alert>(`/alerts/${alertId}/mark-read`);
        return response.data;
    },

    deleteAlert: async (alertId: number): Promise<void> => {
        await api.delete(`/alerts/${alertId}`);
    },
};

export const agentAPI = {
    // Standard Text Chat
    chat: async (query: string): Promise<AgentResponse> => {
        const response = await api.post<AgentResponse>('/agent/chat', { query });
        return response.data;
    },

    // NEW: Voice Chat (Uploads Audio File)
    voiceChat: async (audioUri: string): Promise<AgentResponse> => {
        const formData = new FormData();
        
        // React Native specific FormData structure
        formData.append('file', {
            uri: audioUri,
            name: 'voice_message.m4a', // Naming it .m4a helps backend identify it
            type: 'audio/m4a',         // Standard iOS/Android audio type
        } as any);

        // We use the same 'api' instance so Auth Tokens are included automatically
        const response = await api.post<AgentResponse>('/agent/voice-chat', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    }
};