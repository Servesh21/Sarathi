import { useEffect, useRef, useState } from 'react';
import { getWsUrl } from '@/src/services/api';
import { useAlertsStore, SarathiAlert } from '@/src/stores/alertsStore';

interface UseGuardianWSOptions {
    userId: string;
    autoConnect?: boolean;
}

export function useGuardianWebSocket({ userId, autoConnect = true }: UseGuardianWSOptions) {
    const wsRef = useRef<WebSocket | null>(null);
    const [connected, setConnected] = useState(false);
    const [lastMessage, setLastMessage] = useState<any>(null);
    const addAlert = useAlertsStore((s) => s.addAlert);

    useEffect(() => {
        if (!autoConnect || !userId) return;

        const url = getWsUrl(userId);
        let reconnectTimer: ReturnType<typeof setTimeout> | null = null;

        const connect = () => {
            try {
                const ws = new WebSocket(url);
                wsRef.current = ws;

                ws.onopen = () => {
                    setConnected(true);
                    // Send a ping to establish connection
                    ws.send(JSON.stringify({ type: 'ping' }));
                };

                ws.onmessage = (event) => {
                    try {
                        const data = JSON.parse(event.data);
                        setLastMessage(data);

                        // Handle known message types
                        if (data.type === 'alert') {
                            const alert: SarathiAlert = {
                                alert_id: data.alert_id,
                                user_id: userId,
                                title: data.title || 'Guardian Alert',
                                message: data.message || 'You have a new alert',
                                priority: data.priority || 2,
                                status: 'delivered',
                                created_at: data.created_at || new Date().toISOString(),
                                actions: data.actions || [],
                            };
                            addAlert(alert);
                        }
                    } catch (e) {
                        // ignore malformed message
                    }
                };

                ws.onclose = () => {
                    setConnected(false);
                    // Auto-reconnect after short delay
                    reconnectTimer = setTimeout(connect, 2000);
                };

                ws.onerror = () => {
                    // Let onclose handle reconnect
                };
            } catch (e) {
                reconnectTimer = setTimeout(connect, 3000);
            }
        };

        connect();

        return () => {
            if (reconnectTimer) clearTimeout(reconnectTimer);
            if (wsRef.current) {
                try { wsRef.current.close(); } catch { }
            }
        };
    }, [userId, autoConnect]);

    return { connected, lastMessage };
}
