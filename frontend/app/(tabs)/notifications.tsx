import React, { useEffect, useMemo, useState } from 'react';
import { View, Text, FlatList, RefreshControl, TouchableOpacity } from 'react-native';
import { useAlertsStore } from '@/src/stores/alertsStore';
import { eventsAPI } from '@/src/services/api';
import { useGuardianWebSocket } from '@/hooks/useGuardianWebSocket';
import { useAuthStore } from '@/src/stores/authStore';

function PriorityPill({ priority }: { priority: number }) {
    const bg = priority >= 5 ? '#ef4444' : priority >= 3 ? '#f59e0b' : '#10b981';
    const label = priority >= 5 ? 'EMERGENCY' : priority >= 3 ? 'HIGH' : 'NORMAL';
    return (
        <View style={{ backgroundColor: bg, paddingHorizontal: 8, paddingVertical: 2, borderRadius: 6 }}>
            <Text style={{ color: 'white', fontSize: 12, fontWeight: '600' }}>{label}</Text>
        </View>
    );
}

export default function NotificationsScreen() {
    const { user } = useAuthStore();
    const userId = user?.id || 'mobile_user';

    const { alerts, unreadCount, setAlerts, acknowledge, dismiss, markAllRead } = useAlertsStore();
    const [refreshing, setRefreshing] = useState(false);
    const { connected } = useGuardianWebSocket({ userId, autoConnect: true });

    async function loadAlerts() {
        try {
            setRefreshing(true);
            const res = await eventsAPI.getAlerts(userId, { limit: 50 });
            const list = res.data?.alerts ?? [];
            setAlerts(list);
        } catch (e) {
            // noop
        } finally {
            setRefreshing(false);
        }
    }

    useEffect(() => {
        loadAlerts();
    }, []);

    const renderItem = ({ item }: any) => {
        return (
            <View style={{ padding: 12, borderBottomWidth: 1, borderBottomColor: '#e5e7eb', gap: 8 }}>
                <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8, justifyContent: 'space-between' }}>
                    <Text style={{ fontSize: 16, fontWeight: '700' }}>{item.title}</Text>
                    <PriorityPill priority={item.priority || 2} />
                </View>
                <Text style={{ color: '#374151' }}>{item.message}</Text>
                <View style={{ flexDirection: 'row', gap: 12, marginTop: 4 }}>
                    <TouchableOpacity
                        onPress={async () => {
                            try {
                                await eventsAPI.acknowledgeAlert(item.alert_id, userId);
                            } catch { }
                            acknowledge(item.alert_id);
                        }}
                        style={{ paddingHorizontal: 10, paddingVertical: 6, backgroundColor: '#e5e7eb', borderRadius: 8 }}
                    >
                        <Text style={{ fontWeight: '600' }}>Acknowledge</Text>
                    </TouchableOpacity>
                    <TouchableOpacity
                        onPress={async () => {
                            try {
                                await eventsAPI.dismissAlert(item.alert_id, userId);
                            } catch { }
                            dismiss(item.alert_id);
                        }}
                        style={{ paddingHorizontal: 10, paddingVertical: 6, backgroundColor: '#fee2e2', borderRadius: 8 }}
                    >
                        <Text style={{ fontWeight: '600', color: '#991b1b' }}>Dismiss</Text>
                    </TouchableOpacity>
                </View>
            </View>
        );
    };

    return (
        <View style={{ flex: 1, backgroundColor: 'white' }}>
            <View style={{ padding: 16, borderBottomWidth: 1, borderBottomColor: '#e5e7eb', backgroundColor: 'white', gap: 10 }}>
                <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>
                    <View>
                        <Text style={{ fontSize: 20, fontWeight: '800' }}>Notifications</Text>
                        <Text style={{ color: '#6b7280' }}>{connected ? 'Live updates on' : 'Connecting...'}</Text>
                    </View>
                    <TouchableOpacity onPress={markAllRead} style={{ paddingHorizontal: 10, paddingVertical: 6, backgroundColor: '#e5e7eb', borderRadius: 8 }}>
                        <Text style={{ fontWeight: '600' }}>Mark all read</Text>
                    </TouchableOpacity>
                </View>

                {/* Quick Actions */}
                <View style={{ flexDirection: 'row', gap: 10 }}>
                    <TouchableOpacity
                        onPress={async () => {
                            try { await eventsAPI.startMonitoring(userId, { check_interval_seconds: 60 }); } catch { }
                        }}
                        style={{ paddingHorizontal: 10, paddingVertical: 6, backgroundColor: '#d1fae5', borderRadius: 8 }}
                    >
                        <Text style={{ fontWeight: '600', color: '#065f46' }}>Start Monitoring</Text>
                    </TouchableOpacity>
                    <TouchableOpacity
                        onPress={async () => { try { await eventsAPI.stopMonitoring(userId); } catch { } }}
                        style={{ paddingHorizontal: 10, paddingVertical: 6, backgroundColor: '#fee2e2', borderRadius: 8 }}
                    >
                        <Text style={{ fontWeight: '600', color: '#7f1d1d' }}>Stop Monitoring</Text>
                    </TouchableOpacity>
                    <TouchableOpacity
                        onPress={async () => {
                            try {
                                await eventsAPI.emitEvent({
                                    event_type: 'surge_detected',
                                    severity: 'medium',
                                    user_id: userId,
                                    data: { multiplier: 1.5, area: 'Downtown' },
                                });
                                // Reload alerts
                                loadAlerts();
                            } catch { }
                        }}
                        style={{ paddingHorizontal: 10, paddingVertical: 6, backgroundColor: '#e0e7ff', borderRadius: 8 }}
                    >
                        <Text style={{ fontWeight: '600', color: '#3730a3' }}>Emit Test</Text>
                    </TouchableOpacity>
                </View>
            </View>

            <FlatList
                data={alerts}
                keyExtractor={(item) => item.alert_id}
                renderItem={renderItem}
                refreshControl={<RefreshControl refreshing={refreshing} onRefresh={loadAlerts} />}
                ListEmptyComponent={
                    <View style={{ padding: 24 }}>
                        <Text style={{ textAlign: 'center', color: '#6b7280' }}>No notifications yet. You're all set!</Text>
                    </View>
                }
            />
        </View>
    );
}
