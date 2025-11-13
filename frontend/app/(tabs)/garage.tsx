/**
 * Garage Screen - Vehicle Health & Management
 * Makes invisible risks visible with simple vehicle tracking
 * 
 * Features:
 * - Vehicle Health Score (large percentage)
 * - Diagnostic Log (service history)
 * - Find Mechanic (Google Maps integration)
 * - Simple alerts for maintenance
 */
import React, { useState } from 'react';
import {
    StyleSheet,
    View,
    Text,
    ScrollView,
    TouchableOpacity,
    RefreshControl,
    Platform,
    StatusBar,
    Linking,
    Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Typography, Spacing, Radius } from '@/constants/theme';
import { useColorScheme } from '@/hooks/use-color-scheme';
import { VoiceFAB } from '@/components/voice-fab';

interface MaintenanceItem {
    id: string;
    type: 'service' | 'tire' | 'oil' | 'brake' | 'other';
    status: 'good' | 'warning' | 'alert';
    title: string;
    description: string;
    kmAgo?: number;
    kmUntil?: number;
    date?: string;
}

export default function GarageScreen() {
    const colorScheme = useColorScheme();
    const colors = Colors[colorScheme ?? 'light'];
    const [refreshing, setRefreshing] = useState(false);

    // Mock vehicle data - replace with real API
    const vehicleData = {
        healthScore: 85,
        make: 'Honda',
        model: 'Activa',
        year: 2021,
        totalKm: 34800,
        lastServiceKm: 31400,
        nextServiceKm: 35000,
    };

    const maintenanceLog: MaintenanceItem[] = [
        {
            id: '1',
            type: 'service',
            status: 'good',
            title: 'Last Service',
            description: 'General service completed',
            kmAgo: 3400,
            date: 'Oct 15, 2024',
        },
        {
            id: '2',
            type: 'tire',
            status: 'warning',
            title: 'Tire Tread',
            description: 'Based on last photo - Good for ~800km',
            kmUntil: 800,
        },
        {
            id: '3',
            type: 'oil',
            status: 'warning',
            title: 'Engine Oil',
            description: 'Service recommended soon',
            kmUntil: 200,
        },
        {
            id: '4',
            type: 'brake',
            status: 'good',
            title: 'Brake Pads',
            description: 'Replaced during last service',
            kmAgo: 3400,
            date: 'Oct 15, 2024',
        },
    ];

    const onRefresh = async () => {
        setRefreshing(true);
        // TODO: Fetch fresh vehicle data
        setTimeout(() => setRefreshing(false), 1500);
    };

    const findNearbyMechanic = () => {
        // Open Google Maps with "bike mechanic near me"
        const query = 'bike+mechanic+near+me';
        const url = Platform.select({
            ios: `maps://app?q=${query}`,
            android: `geo:0,0?q=${query}`,
            default: `https://www.google.com/maps/search/${query}`,
        });

        Linking.canOpenURL(url).then((supported) => {
            if (supported) {
                Linking.openURL(url);
            } else {
                Alert.alert('Error', 'Unable to open maps');
            }
        });
    };

    const getHealthColor = () => {
        if (vehicleData.healthScore >= 80) return colors.success;
        if (vehicleData.healthScore >= 60) return colors.warning;
        return colors.danger;
    };

    const getHealthLabel = () => {
        if (vehicleData.healthScore >= 80) return 'Excellent';
        if (vehicleData.healthScore >= 60) return 'Good';
        return 'Needs Attention';
    };

    const getStatusIcon = (status: MaintenanceItem['status']) => {
        switch (status) {
            case 'good':
                return { name: 'checkmark-circle' as const, color: colors.success };
            case 'warning':
                return { name: 'alert-circle' as const, color: colors.warning };
            case 'alert':
                return { name: 'warning' as const, color: colors.danger };
        }
    };

    const getTypeIcon = (type: MaintenanceItem['type']) => {
        const iconMap = {
            service: 'build',
            tire: 'disc',
            oil: 'water',
            brake: 'hand-left',
            other: 'information-circle',
        };
        return iconMap[type] as keyof typeof Ionicons.glyphMap;
    };

    return (
        <View style={[styles.container, { backgroundColor: colors.background }]}>
            <StatusBar barStyle={colorScheme === 'dark' ? 'light-content' : 'dark-content'} />

            <ScrollView
                style={styles.scrollView}
                contentContainerStyle={styles.scrollContent}
                refreshControl={
                    <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={colors.primary} />
                }
                showsVerticalScrollIndicator={false}
            >
                {/* Header */}
                <View style={styles.header}>
                    <Text style={[styles.title, { color: colors.text }]}>My Vehicle</Text>
                    <Text style={[styles.subtitle, { color: colors.textSecondary }]}>
                        {vehicleData.make} {vehicleData.model} ({vehicleData.year})
                    </Text>
                </View>

                {/* Vehicle Health Score - Hero Section */}
                <View style={[styles.healthCard, { backgroundColor: colors.backgroundCard }]}>
                    <View style={styles.healthHeader}>
                        <View style={[styles.vehicleIcon, { backgroundColor: colors.primary + '15' }]}>
                            <Ionicons name="bicycle" size={40} color={colors.primary} />
                        </View>
                        <View style={styles.healthTextContainer}>
                            <Text style={[styles.healthLabel, { color: colors.textSecondary }]}>
                                Vehicle Health
                            </Text>
                            <View style={styles.scoreRow}>
                                <Text style={[styles.healthScore, { color: getHealthColor() }]}>
                                    {vehicleData.healthScore}%
                                </Text>
                                <View style={[styles.statusBadge, { backgroundColor: getHealthColor() + '20' }]}>
                                    <Text style={[styles.statusText, { color: getHealthColor() }]}>
                                        {getHealthLabel()}
                                    </Text>
                                </View>
                            </View>
                        </View>
                    </View>

                    {/* Mileage Info */}
                    <View style={[styles.mileageSection, { borderTopColor: colors.border }]}>
                        <View style={styles.mileageItem}>
                            <Ionicons name="speedometer" size={20} color={colors.textSecondary} />
                            <View>
                                <Text style={[styles.mileageLabel, { color: colors.textSecondary }]}>
                                    Total Mileage
                                </Text>
                                <Text style={[styles.mileageValue, { color: colors.text }]}>
                                    {vehicleData.totalKm.toLocaleString()} km
                                </Text>
                            </View>
                        </View>
                        <View style={styles.mileageItem}>
                            <Ionicons name="calendar" size={20} color={colors.textSecondary} />
                            <View>
                                <Text style={[styles.mileageLabel, { color: colors.textSecondary }]}>
                                    Next Service
                                </Text>
                                <Text style={[styles.mileageValue, { color: colors.text }]}>
                                    {vehicleData.nextServiceKm.toLocaleString()} km
                                </Text>
                            </View>
                        </View>
                    </View>
                </View>

                {/* Diagnostic Log */}
                <View style={styles.section}>
                    <Text style={[styles.sectionTitle, { color: colors.text }]}>Diagnostic Log</Text>
                    <Text style={[styles.sectionSubtitle, { color: colors.textSecondary }]}>
                        Service history and maintenance alerts
                    </Text>

                    <View style={styles.logContainer}>
                        {maintenanceLog.map((item, index) => {
                            const statusIcon = getStatusIcon(item.status);
                            const typeIcon = getTypeIcon(item.type);

                            return (
                                <View
                                    key={item.id}
                                    style={[
                                        styles.logItem,
                                        { backgroundColor: colors.backgroundCard, borderLeftColor: statusIcon.color },
                                        index === maintenanceLog.length - 1 && styles.logItemLast,
                                    ]}
                                >
                                    <View style={styles.logHeader}>
                                        <View style={styles.logTitleRow}>
                                            <Ionicons name={typeIcon} size={20} color={statusIcon.color} />
                                            <Text style={[styles.logTitle, { color: colors.text }]}>{item.title}</Text>
                                        </View>
                                        <Ionicons name={statusIcon.name} size={24} color={statusIcon.color} />
                                    </View>

                                    <Text style={[styles.logDescription, { color: colors.textSecondary }]}>
                                        {item.description}
                                    </Text>

                                    {(item.kmAgo || item.kmUntil || item.date) && (
                                        <View style={styles.logMetadata}>
                                            {item.kmAgo && (
                                                <Text style={[styles.logMeta, { color: colors.textLight }]}>
                                                    {item.kmAgo.toLocaleString()}km ago
                                                </Text>
                                            )}
                                            {item.kmUntil && (
                                                <Text style={[styles.logMeta, { color: statusIcon.color }]}>
                                                    {item.kmUntil.toLocaleString()}km remaining
                                                </Text>
                                            )}
                                            {item.date && (
                                                <Text style={[styles.logMeta, { color: colors.textLight }]}>
                                                    {item.date}
                                                </Text>
                                            )}
                                        </View>
                                    )}
                                </View>
                            );
                        })}
                    </View>
                </View>

                {/* Find Mechanic Button */}
                <TouchableOpacity
                    style={[styles.mechanicButton, { backgroundColor: colors.action }]}
                    onPress={findNearbyMechanic}
                    activeOpacity={0.8}
                >
                    <Ionicons name="location" size={24} color={colors.textInverse} />
                    <Text style={[styles.mechanicButtonText, { color: colors.textInverse }]}>
                        Find Nearby Mechanic
                    </Text>
                    <Ionicons name="chevron-forward" size={24} color={colors.textInverse} />
                </TouchableOpacity>

                {/* Bottom spacing for FAB */}
                <View  style={styles.fabSpacer} />
            </ScrollView>

            {/* Persistent Voice FAB */}
            <VoiceFAB />
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    scrollView: {
        flex: 1,
    },
    scrollContent: {
        padding: Spacing.lg,
        paddingTop: Platform.OS === 'ios' ? 60 : Spacing.lg,
    },
    header: {
        marginBottom: Spacing.xl,
    },
    title: {
        fontSize: Typography.xxl,
        fontWeight: '800',
        marginBottom: Spacing.xs,
    },
    subtitle: {
        fontSize: Typography.md,
    },
    healthCard: {
        borderRadius: Radius.xl,
        padding: Spacing.xl,
        marginBottom: Spacing.xl,
        elevation: 2,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 1 },
        shadowOpacity: 0.05,
        shadowRadius: 4,
    },
    healthHeader: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: Spacing.md,
        marginBottom: Spacing.lg,
    },
    vehicleIcon: {
        width: 80,
        height: 80,
        borderRadius: Radius.full,
        justifyContent: 'center',
        alignItems: 'center',
    },
    healthTextContainer: {
        flex: 1,
    },
    healthLabel: {
        fontSize: Typography.md,
        marginBottom: Spacing.xs,
    },
    scoreRow: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: Spacing.md,
    },
    healthScore: {
        fontSize: Typography.hero,
        fontWeight: '900',
    },
    statusBadge: {
        paddingHorizontal: Spacing.md,
        paddingVertical: Spacing.xs,
        borderRadius: Radius.full,
    },
    statusText: {
        fontSize: Typography.md,
        fontWeight: '600',
    },
    mileageSection: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        paddingTop: Spacing.lg,
        borderTopWidth: 1,
    },
    mileageItem: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: Spacing.sm,
    },
    mileageLabel: {
        fontSize: Typography.sm,
    },
    mileageValue: {
        fontSize: Typography.lg,
        fontWeight: '700',
    },
    section: {
        marginBottom: Spacing.xl,
    },
    sectionTitle: {
        fontSize: Typography.xl,
        fontWeight: '700',
        marginBottom: Spacing.xs,
    },
    sectionSubtitle: {
        fontSize: Typography.sm,
        marginBottom: Spacing.md,
    },
    logContainer: {
        gap: Spacing.md,
    },
    logItem: {
        borderRadius: Radius.md,
        padding: Spacing.md,
        borderLeftWidth: 4,
    },
    logItemLast: {
        marginBottom: 0,
    },
    logHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: Spacing.sm,
    },
    logTitleRow: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: Spacing.sm,
    },
    logTitle: {
        fontSize: Typography.lg,
        fontWeight: '600',
    },
    logDescription: {
        fontSize: Typography.md,
        marginBottom: Spacing.sm,
    },
    logMetadata: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        gap: Spacing.md,
    },
    logMeta: {
        fontSize: Typography.sm,
    },
    mechanicButton: {
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        gap: Spacing.sm,
        paddingVertical: Spacing.lg,
        borderRadius: Radius.lg,
        marginBottom: Spacing.md,
        elevation: 4,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.15,
        shadowRadius: 8
    },
    mechanicButtonText: {
        fontSize: Typography.md,
        fontWeight: '600',
    },  
    fabSpacer: {
        height: 80,
    },
}); 
