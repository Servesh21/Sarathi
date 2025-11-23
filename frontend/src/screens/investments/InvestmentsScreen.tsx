import React, { useEffect } from 'react';
import { View, Text, ScrollView, ActivityIndicator, TouchableOpacity } from 'react-native';
import { useFinancialStore } from '../../store/financialStore';

export default function InvestmentsScreen() {
    const { investments, portfolio, surplus, recommendations, fetchInvestments, fetchPortfolio, fetchSurplus, fetchRecommendations, isLoading } = useFinancialStore();

    useEffect(() => {
        fetchInvestments();
        fetchPortfolio();
        fetchSurplus();
        fetchRecommendations();
    }, []);

    if (isLoading && !portfolio) {
        return (
            <View className="flex-1 justify-center items-center bg-gray-50">
                <ActivityIndicator size="large" color="#10b981" />
            </View>
        );
    }

    return (
        <ScrollView className="flex-1 bg-gray-50">
            <View className="px-4 py-6">
                <Text className="text-3xl font-bold text-gray-900 mb-6">Growth Engine</Text>

                {/* Portfolio Summary */}
                {portfolio && (
                    <View className="bg-gradient-to-r from-green-500 to-emerald-600 rounded-2xl p-5 mb-6 shadow-lg">
                        <Text className="text-white text-lg font-semibold mb-4">Portfolio Overview</Text>
                        <View className="space-y-2">
                            <View className="flex-row justify-between">
                                <Text className="text-white opacity-90">Total Invested</Text>
                                <Text className="text-white font-bold text-xl">₹{portfolio.total_invested.toFixed(0)}</Text>
                            </View>
                            <View className="flex-row justify-between">
                                <Text className="text-white opacity-90">Current Value</Text>
                                <Text className="text-white font-bold text-xl">₹{portfolio.current_portfolio_value.toFixed(0)}</Text>
                            </View>
                            <View className="flex-row justify-between">
                                <Text className="text-white opacity-90">Total Returns</Text>
                                <Text className="text-white font-bold text-2xl">
                                    +₹{portfolio.total_returns.toFixed(0)} ({portfolio.returns_percentage.toFixed(1)}%)
                                </Text>
                            </View>
                        </View>
                    </View>
                )}

                {/* Surplus Analysis */}
                {surplus && (
                    <View className="bg-white rounded-xl p-5 mb-6 shadow-sm">
                        <Text className="text-lg font-semibold text-gray-900 mb-4">Monthly Surplus Analysis</Text>
                        <View className="space-y-2">
                            <View className="flex-row justify-between">
                                <Text className="text-gray-600">Monthly Income</Text>
                                <Text className="font-semibold text-gray-900">₹{surplus.monthly_income.toFixed(0)}</Text>
                            </View>
                            <View className="flex-row justify-between">
                                <Text className="text-gray-600">Monthly Expenses</Text>
                                <Text className="font-semibold text-red-600">₹{surplus.monthly_expenses.toFixed(0)}</Text>
                            </View>
                            <View className="h-px bg-gray-200 my-2" />
                            <View className="flex-row justify-between">
                                <Text className="text-gray-900 font-semibold">Surplus</Text>
                                <Text className="font-bold text-green-600 text-xl">
                                    ₹{surplus.monthly_surplus.toFixed(0)} ({surplus.surplus_percentage.toFixed(1)}%)
                                </Text>
                            </View>
                        </View>

                        {surplus.insights && surplus.insights.length > 0 && (
                            <View className="mt-4 bg-blue-50 rounded-lg p-3">
                                <Text className="font-semibold text-blue-900 mb-2">💡 Insights</Text>
                                {surplus.insights.map((insight, idx) => (
                                    <Text key={idx} className="text-blue-800 text-sm mb-1">• {insight}</Text>
                                ))}
                            </View>
                        )}
                    </View>
                )}

                {/* AI Recommendations */}
                {recommendations.length > 0 && (
                    <View className="mb-6">
                        <Text className="text-xl font-semibold text-gray-900 mb-4">🤖 AI Investment Recommendations</Text>
                        {recommendations.map((rec) => (
                            <View key={rec.id} className="bg-white rounded-xl p-5 mb-3 shadow-sm">
                                <View className="flex-row justify-between items-start mb-2">
                                    <Text className="text-lg font-semibold text-gray-900 flex-1">{rec.title}</Text>
                                    <View className={`px-3 py-1 rounded-full ${rec.risk_level === 'low' ? 'bg-green-100' :
                                            rec.risk_level === 'medium' ? 'bg-yellow-100' : 'bg-red-100'
                                        }`}>
                                        <Text className={`font-semibold text-xs ${rec.risk_level === 'low' ? 'text-green-700' :
                                                rec.risk_level === 'medium' ? 'text-yellow-700' : 'text-red-700'
                                            }`}>
                                            {rec.risk_level.toUpperCase()}
                                        </Text>
                                    </View>
                                </View>

                                <Text className="text-gray-600 mb-3">{rec.description}</Text>

                                <View className="space-y-1">
                                    <View className="flex-row justify-between">
                                        <Text className="text-gray-600">Suggested Amount</Text>
                                        <Text className="font-semibold text-primary">₹{rec.suggested_amount.toFixed(0)}</Text>
                                    </View>
                                    {rec.expected_return_rate && (
                                        <View className="flex-row justify-between">
                                            <Text className="text-gray-600">Expected Return</Text>
                                            <Text className="font-semibold text-green-600">{rec.expected_return_rate}%</Text>
                                        </View>
                                    )}
                                    {rec.tenure_months && (
                                        <View className="flex-row justify-between">
                                            <Text className="text-gray-600">Tenure</Text>
                                            <Text className="font-semibold text-gray-900">{rec.tenure_months} months</Text>
                                        </View>
                                    )}
                                </View>

                                {rec.ai_reasoning && (
                                    <View className="mt-3 bg-purple-50 rounded-lg p-3">
                                        <Text className="text-purple-900 text-sm">{rec.ai_reasoning}</Text>
                                    </View>
                                )}
                            </View>
                        ))}
                    </View>
                )}

                {/* Active Investments */}
                {investments.length > 0 && (
                    <View>
                        <Text className="text-xl font-semibold text-gray-900 mb-4">Active Investments</Text>
                        {investments.map((inv) => (
                            <View key={inv.id} className="bg-white rounded-xl p-4 mb-3 shadow-sm">
                                <Text className="font-semibold text-gray-900">{inv.investment_name}</Text>
                                <Text className="text-gray-600 text-sm mb-2">{inv.investment_type}</Text>
                                <View className="flex-row justify-between">
                                    <View>
                                        <Text className="text-gray-600 text-sm">Invested</Text>
                                        <Text className="font-semibold text-gray-900">₹{inv.invested_amount.toFixed(0)}</Text>
                                    </View>
                                    <View>
                                        <Text className="text-gray-600 text-sm">Current Value</Text>
                                        <Text className="font-semibold text-gray-900">₹{inv.current_value.toFixed(0)}</Text>
                                    </View>
                                    <View>
                                        <Text className="text-gray-600 text-sm">Returns</Text>
                                        <Text className="font-semibold text-green-600">
                                            {inv.returns_percentage > 0 ? '+' : ''}{inv.returns_percentage.toFixed(1)}%
                                        </Text>
                                    </View>
                                </View>
                            </View>
                        ))}
                    </View>
                )}
            </View>
        </ScrollView>
    );
}
