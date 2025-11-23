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
    chat: async (query: string): Promise<AgentResponse> => {
        const response = await api.post<AgentResponse>('/agent/chat', { query });
        return response.data;
    },
};
