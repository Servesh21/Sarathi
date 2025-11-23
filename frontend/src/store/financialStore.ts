import { create } from 'zustand';
import { Goal, goalsAPI, Investment, investmentsAPI, PortfolioSummary, SurplusAnalysis } from '../api/financial';

interface FinancialState {
    goals: Goal[];
    investments: Investment[];
    portfolio: PortfolioSummary | null;
    surplus: SurplusAnalysis | null;
    recommendations: any[];
    isLoading: boolean;
    error: string | null;

    fetchGoals: () => Promise<void>;
    fetchInvestments: () => Promise<void>;
    fetchPortfolio: () => Promise<void>;
    fetchSurplus: () => Promise<void>;
    fetchRecommendations: () => Promise<void>;
    addGoalProgress: (goalId: number, amount: number) => Promise<void>;
}

export const useFinancialStore = create<FinancialState>((set) => ({
    goals: [],
    investments: [],
    portfolio: null,
    surplus: null,
    recommendations: [],
    isLoading: false,
    error: null,

    fetchGoals: async () => {
        set({ isLoading: true, error: null });
        try {
            const goals = await goalsAPI.getGoals();
            set({ goals, isLoading: false });
        } catch (error: any) {
            set({
                error: error.response?.data?.detail || 'Failed to fetch goals',
                isLoading: false
            });
        }
    },

    fetchInvestments: async () => {
        set({ isLoading: true, error: null });
        try {
            const investments = await investmentsAPI.getInvestments();
            set({ investments, isLoading: false });
        } catch (error: any) {
            set({
                error: error.response?.data?.detail || 'Failed to fetch investments',
                isLoading: false
            });
        }
    },

    fetchPortfolio: async () => {
        set({ isLoading: true, error: null });
        try {
            const portfolio = await investmentsAPI.getPortfolio();
            set({ portfolio, isLoading: false });
        } catch (error: any) {
            set({
                error: error.response?.data?.detail || 'Failed to fetch portfolio',
                isLoading: false
            });
        }
    },

    fetchSurplus: async () => {
        set({ isLoading: true, error: null });
        try {
            const surplus = await investmentsAPI.getSurplusAnalysis();
            set({ surplus, isLoading: false });
        } catch (error: any) {
            set({
                error: error.response?.data?.detail || 'Failed to fetch surplus',
                isLoading: false
            });
        }
    },

    fetchRecommendations: async () => {
        set({ isLoading: true, error: null });
        try {
            const recommendations = await investmentsAPI.getRecommendations();
            set({ recommendations, isLoading: false });
        } catch (error: any) {
            set({
                error: error.response?.data?.detail || 'Failed to fetch recommendations',
                isLoading: false
            });
        }
    },

    addGoalProgress: async (goalId: number, amount: number) => {
        set({ isLoading: true, error: null });
        try {
            await goalsAPI.addProgress(goalId, amount);
            // Refetch goals
            const goals = await goalsAPI.getGoals();
            set({ goals, isLoading: false });
        } catch (error: any) {
            set({
                error: error.response?.data?.detail || 'Failed to add progress',
                isLoading: false
            });
            throw error;
        }
    },
}));
