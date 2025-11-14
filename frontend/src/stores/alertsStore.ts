import { create } from 'zustand';

export type AlertPriority = 1 | 2 | 3 | 4 | 5; // LOW..EMERGENCY
export type AlertStatus = 'pending' | 'sent' | 'delivered' | 'read' | 'acknowledged' | 'dismissed' | 'failed';

export interface SarathiAlert {
    alert_id: string;
    user_id: string;
    title: string;
    message: string;
    priority: AlertPriority;
    status: AlertStatus;
    created_at: string; // ISO
    actions?: Array<{ type: string; label: string }>;
}

interface AlertsState {
    alerts: SarathiAlert[];
    unreadCount: number;
    lastReceivedAt?: string;
    addAlert: (alert: SarathiAlert) => void;
    setAlerts: (alerts: SarathiAlert[]) => void;
    acknowledge: (alertId: string) => void;
    dismiss: (alertId: string) => void;
    markAllRead: () => void;
    clear: () => void;
}

export const useAlertsStore = create<AlertsState>((set, get) => ({
    alerts: [],
    unreadCount: 0,
    lastReceivedAt: undefined,

    addAlert: (alert) => {
        set((state) => ({
            alerts: [alert, ...state.alerts],
            unreadCount: state.unreadCount + 1,
            lastReceivedAt: new Date().toISOString(),
        }));
    },

    setAlerts: (alerts) => {
        // Assume all received alerts as 'delivered'
        set({
            alerts,
            unreadCount: alerts.filter((a) => a.status !== 'read' && a.status !== 'dismissed' && a.status !== 'acknowledged').length,
        });
    },

    acknowledge: (alertId) => {
        set((state) => ({
            alerts: state.alerts.map((a) => (a.alert_id === alertId ? { ...a, status: 'acknowledged' } : a)),
            unreadCount: Math.max(0, state.unreadCount - 1),
        }));
    },

    dismiss: (alertId) => {
        set((state) => ({
            alerts: state.alerts.map((a) => (a.alert_id === alertId ? { ...a, status: 'dismissed' } : a)),
            unreadCount: Math.max(0, state.unreadCount - 1),
        }));
    },

    markAllRead: () => {
        set((state) => ({
            alerts: state.alerts.map((a) => (a.status === 'pending' || a.status === 'sent' || a.status === 'delivered' ? { ...a, status: 'read' } : a)),
            unreadCount: 0,
        }));
    },

    clear: () => set({ alerts: [], unreadCount: 0 }),
}));
