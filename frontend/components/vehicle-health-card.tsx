/**
 * Vehicle Health Card - Simple vehicle status indicator
 * Shows service status, alerts, and quick action
 */
import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Typography, Spacing, Radius } from '@/constants/theme';
import { useColorScheme } from '@/hooks/use-color-scheme';

interface VehicleHealthCardProps {
    serviceStatus: 'good' | 'due-soon' | 'overdue';
    kmSinceService: number;
    kmUntilService: number;
    onFindMechanic?: () => void;
}

export function VehicleHealthCard({
    serviceStatus,
    kmSinceService,
    kmUntilService,
    onFindMechanic,
}: VehicleHealthCardProps) {
    const colorScheme = useColorScheme();
    const colors = Colors[colorScheme ?? 'light'];

    const getStatusColor = () => {
        switch (serviceStatus) {
            case 'good':
                return colors.success;
            case 'due-soon':
                return colors.warning;
            case 'overdue':
                return colors.danger;
        }
    };

    const getStatusIcon = () => {
        switch (serviceStatus) {
            case 'good':
                return 'checkmark-circle';
            case 'due-soon':
                return 'alert-circle';
            case 'overdue':
                return 'warning';
        }
    };

    const getStatusText = () => {
        if (serviceStatus === 'good') return 'Vehicle Healthy';
        if (serviceStatus === 'due-soon') return `Service Due in ${kmUntilService}km`;
        return 'Service Overdue!';
    };

    return (
        <TouchableOpacity
            style={[styles.card, { backgroundColor: colors.backgroundCard }]}
            onPress={onFindMechanic}
            activeOpacity={0.7}
        >
            <View style={styles.header}>
                <View style={styles.titleRow}>
                    <Ionicons name="bicycle" size={24} color={colors.primary} />
                    <Text style={[styles.title, { color: colors.text }]}>My Vehicle</Text>
                </View>
                <View style={[styles.statusBadge, { backgroundColor: getStatusColor() + '20' }]}>
                    <Ionicons name={getStatusIcon()} size={16} color={getStatusColor()} />
                    <Text style={[styles.statusText, { color: getStatusColor() }]}>
                        {getStatusText()}
                    </Text>
                </View>
            </View>

            <View style={styles.details}>
                <View style={styles.detailRow}>
                    <Ionicons name="speedometer" size={16} color={colors.textSecondary} />
                    <Text style={[styles.detailText, { color: colors.textSecondary }]}>
                        {kmSinceService.toLocaleString()}km since last service
                    </Text>
                </View>

                {serviceStatus !== 'good' && (
                    <View style={[styles.alertBox, { backgroundColor: getStatusColor() + '10' }]}>
                        <Text style={[styles.alertText, { color: getStatusColor() }]}>
                            {serviceStatus === 'due-soon'
                                ? 'Book a service appointment soon to avoid issues'
                                : 'Your vehicle needs immediate attention'}
                        </Text>
                    </View>
                )}
            </View>

            <View style={[styles.footer, { borderTopColor: colors.border }]}>
                <Text style={[styles.actionText, { color: colors.primary }]}>Find Nearby Mechanic</Text>
                <Ionicons name="chevron-forward" size={20} color={colors.primary} />
            </View>
        </TouchableOpacity>
    );
}

const styles = StyleSheet.create({
    card: {
        borderRadius: Radius.lg,
        padding: Spacing.md,
        gap: Spacing.md,
    },
    header: {
        gap: Spacing.sm,
    },
    titleRow: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: Spacing.sm,
    },
    title: {
        fontSize: Typography.lg,
        fontWeight: '600',
    },
    statusBadge: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: Spacing.xs,
        paddingHorizontal: Spacing.sm,
        paddingVertical: Spacing.xs,
        borderRadius: Radius.full,
        alignSelf: 'flex-start',
    },
    statusText: {
        fontSize: Typography.sm,
        fontWeight: '600',
    },
    details: {
        gap: Spacing.sm,
    },
    detailRow: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: Spacing.xs,
    },
    detailText: {
        fontSize: Typography.sm,
    },
    alertBox: {
        padding: Spacing.sm,
        borderRadius: Radius.sm,
    },
    alertText: {
        fontSize: Typography.sm,
        fontWeight: '500',
    },
    footer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingTop: Spacing.sm,
        borderTopWidth: 1,
    },
    actionText: {
        fontSize: Typography.md,
        fontWeight: '600',
    },
});