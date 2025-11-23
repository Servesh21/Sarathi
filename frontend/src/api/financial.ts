import api from './client';

export interface Goal {
    id: number;
    goal_name: string;
    description?: string;
    goal_type: string;
    target_amount: number;
    current_amount: number;
    monthly_contribution: number;
    target_date?: string;
    status: string;
    completion_percentage: number;
    percentage_complete: number;
    created_at: string;
}

export interface Investment {
    id: number;
    investment_name: string;
    investment_type: string;
    principal_amount: number;
    current_value: number;
    invested_amount: number;
    expected_return_rate?: number;
    actual_return: number;
    returns_percentage: number;
    is_recurring: boolean;
    status: string;
    created_at: string;
}

export interface InvestmentRecommendation {
    id: number;
    recommendation_type: string;
    title: string;
    description: string;
    suggested_amount: number;
    expected_return_rate?: number;
    tenure_months?: number;
    risk_level: string;
    ai_reasoning?: string;
    user_profile_match_score?: number;
    created_at: string;
}

export interface PortfolioSummary {
    total_invested: number;
    current_portfolio_value: number;
    total_returns: number;
    returns_percentage: number;
    active_investments: number;
    monthly_recurring_total: number;
    investment_breakdown: Record<string, number>;
    risk_distribution: Record<string, number>;
}

export interface SurplusAnalysis {
    monthly_income: number;
    monthly_expenses: number;
    monthly_surplus: number;
    surplus_percentage: number;
    recommended_savings: number;
    recommended_investments: number;
    emergency_fund_status: string;
    insights: string[];
}

export const goalsAPI = {
    getGoals: async (): Promise<Goal[]> => {
        const response = await api.get<Goal[]>('/goals');
        return response.data;
    },

    createGoal: async (data: {
        goal_name: string;
        target_amount: number;
        target_date?: string;
        monthly_contribution?: number;
    }): Promise<Goal> => {
        const response = await api.post<Goal>('/goals', data);
        return response.data;
    },

    addProgress: async (goalId: number, amount: number, notes?: string): Promise<any> => {
        const response = await api.post(`/goals/${goalId}/progress`, {
            goal_id: goalId,
            amount_added: amount,
            notes,
        });
        return response.data;
    },
};

export const investmentsAPI = {
    getInvestments: async (): Promise<Investment[]> => {
        const response = await api.get<Investment[]>('/investments');
        return response.data;
    },

    getPortfolio: async (): Promise<PortfolioSummary> => {
        const response = await api.get<PortfolioSummary>('/investments/portfolio');
        return response.data;
    },

    getSurplusAnalysis: async (): Promise<SurplusAnalysis> => {
        const response = await api.get<SurplusAnalysis>('/investments/surplus-analysis');
        return response.data;
    },

    getRecommendations: async (): Promise<InvestmentRecommendation[]> => {
        const response = await api.get<InvestmentRecommendation[]>('/investments/recommendations');
        return response.data;
    },

    createInvestment: async (data: any): Promise<Investment> => {
        const response = await api.post<Investment>('/investments', data);
        return response.data;
    },
};
