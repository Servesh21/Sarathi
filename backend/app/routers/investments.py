from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from datetime import datetime
from app.database import get_db
from app.models.user import User
from app.models.investment import Investment, InvestmentRecommendation
from app.models.trip import Trip
from app.auth import get_current_active_user
from app.schemas.investment import (
    InvestmentCreate, InvestmentResponse, InvestmentUpdate,
    InvestmentRecommendationCreate, InvestmentRecommendationResponse,
    InvestmentRecommendationUpdate, PortfolioSummary, SurplusAnalysis
)
from app.services import financial_service
from datetime import timedelta

router = APIRouter(prefix="/investments", tags=["Investments"])


@router.post("", response_model=InvestmentResponse, status_code=status.HTTP_201_CREATED)
async def create_investment(
    investment_data: InvestmentCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new investment"""
    
    new_investment = Investment(
        user_id=current_user.id,
        current_value=investment_data.principal_amount,
        invested_amount=investment_data.principal_amount,
        **investment_data.model_dump()
    )
    
    db.add(new_investment)
    await db.commit()
    await db.refresh(new_investment)
    
    return new_investment


@router.get("", response_model=List[InvestmentResponse])
async def get_investments(
    status_filter: str = "active",
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's investments"""
    
    query = select(Investment).filter(Investment.user_id == current_user.id)
    
    if status_filter:
        query = query.filter(Investment.status == status_filter)
    
    query = query.order_by(Investment.created_at.desc())
    
    result = await db.execute(query)
    investments = result.scalars().all()
    
    return investments


@router.get("/portfolio", response_model=PortfolioSummary)
async def get_portfolio_summary(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get portfolio summary"""
    
    result = await db.execute(
        select(Investment)
        .filter(Investment.user_id == current_user.id)
        .filter(Investment.status == 'active')
    )
    investments = result.scalars().all()
    
    total_invested = sum(inv.invested_amount for inv in investments)
    current_portfolio_value = sum(inv.current_value for inv in investments)
    total_returns = current_portfolio_value - total_invested
    returns_percentage = (total_returns / total_invested * 100) if total_invested > 0 else 0
    
    monthly_recurring_total = sum(
        inv.recurring_amount 
        for inv in investments 
        if inv.is_recurring and inv.recurring_amount
    )
    
    # Investment breakdown by type
    investment_breakdown = {}
    for inv in investments:
        inv_type = inv.investment_type
        investment_breakdown[inv_type] = investment_breakdown.get(inv_type, 0) + inv.current_value
    
    # Risk distribution
    risk_distribution = {}
    for inv in investments:
        risk_level = inv.risk_level
        risk_distribution[risk_level] = risk_distribution.get(risk_level, 0) + inv.current_value
    
    return PortfolioSummary(
        total_invested=total_invested,
        current_portfolio_value=current_portfolio_value,
        total_returns=total_returns,
        returns_percentage=returns_percentage,
        active_investments=len(investments),
        monthly_recurring_total=monthly_recurring_total,
        investment_breakdown=investment_breakdown,
        risk_distribution=risk_distribution
    )


@router.get("/surplus-analysis", response_model=SurplusAnalysis)
async def get_surplus_analysis(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get monthly surplus analysis"""
    
    # Calculate monthly income from trips
    start_date = datetime.now() - timedelta(days=30)
    
    result = await db.execute(
        select(
            func.sum(Trip.earnings).label('total_earnings'),
            func.sum(Trip.fuel_cost + Trip.toll_cost + Trip.other_expenses).label('total_expenses')
        )
        .filter(Trip.user_id == current_user.id)
        .filter(Trip.created_at >= start_date)
    )
    
    stats = result.first()
    
    monthly_income = float(stats.total_earnings or 0) - float(stats.total_expenses or 0)
    monthly_expenses = current_user.monthly_expense_average or monthly_income * 0.6
    
    monthly_surplus = monthly_income - monthly_expenses
    surplus_percentage = (monthly_surplus / monthly_income * 100) if monthly_income > 0 else 0
    
    # Recommended allocation (50-30-20 rule)
    recommended_savings = monthly_surplus * 0.5
    recommended_investments = monthly_surplus * 0.3
    
    # Emergency fund status
    emergency_fund_target = monthly_expenses * 6
    
    # Get current liquid investments
    inv_result = await db.execute(
        select(Investment)
        .filter(Investment.user_id == current_user.id)
        .filter(Investment.risk_level == 'low')
        .filter(Investment.status == 'active')
    )
    liquid_investments = inv_result.scalars().all()
    current_emergency_fund = sum(inv.current_value for inv in liquid_investments)
    
    emergency_fund_percentage = (current_emergency_fund / emergency_fund_target * 100) if emergency_fund_target > 0 else 0
    
    if emergency_fund_percentage >= 100:
        emergency_fund_status = "complete"
    elif emergency_fund_percentage >= 50:
        emergency_fund_status = "in_progress"
    else:
        emergency_fund_status = "needs_attention"
    
    # Generate insights
    insights = []
    
    if monthly_surplus <= 0:
        insights.append("⚠️ Your expenses exceed income. Focus on cost reduction.")
    elif monthly_surplus < 2000:
        insights.append("💡 Start with small recurring deposits to build savings habit.")
    elif monthly_surplus < 5000:
        insights.append("✅ Good surplus! Consider FD + Mutual fund SIP combination.")
    else:
        insights.append("🎯 Excellent surplus! Diversify across multiple instruments.")
    
    if emergency_fund_status == "needs_attention":
        insights.append(f"🚨 Priority: Build emergency fund (₹{emergency_fund_target:.0f} target)")
    elif emergency_fund_status == "in_progress":
        insights.append(f"📈 Good progress on emergency fund ({emergency_fund_percentage:.0f}% complete)")
    else:
        insights.append("✅ Emergency fund complete! Focus on wealth creation.")
    
    if surplus_percentage < 20:
        insights.append("📊 Aim to save at least 20% of your income.")
    elif surplus_percentage > 40:
        insights.append("🌟 Excellent savings rate! Consider higher-return investments.")
    
    return SurplusAnalysis(
        monthly_income=monthly_income,
        monthly_expenses=monthly_expenses,
        monthly_surplus=monthly_surplus,
        surplus_percentage=surplus_percentage,
        recommended_savings=recommended_savings,
        recommended_investments=recommended_investments,
        emergency_fund_status=emergency_fund_status,
        insights=insights
    )


@router.get("/recommendations", response_model=List[InvestmentRecommendationResponse])
async def get_investment_recommendations(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get personalized investment recommendations"""
    
    # Get active recommendations
    result = await db.execute(
        select(InvestmentRecommendation)
        .filter(InvestmentRecommendation.user_id == current_user.id)
        .filter(InvestmentRecommendation.is_acted_upon == False)
        .order_by(InvestmentRecommendation.created_at.desc())
        .limit(10)
    )
    recommendations = result.scalars().all()
    
    # If no recommendations, generate new ones
    if not recommendations:
        # Get surplus analysis
        surplus_analysis = await get_surplus_analysis(current_user, db)
        
        if surplus_analysis.monthly_surplus > 0:
            # Get investment suggestions from financial service
            suggestions = await financial_service.get_investment_suggestions(
                surplus_analysis.monthly_surplus,
                'low',  # Conservative for gig workers
                'wealth_creation'
            )
            
            # Create recommendation records
            for suggestion in suggestions[:5]:
                rec = InvestmentRecommendation(
                    user_id=current_user.id,
                    recommendation_type=suggestion['investment_type'],
                    title=f"{suggestion['provider']} - {suggestion['investment_type'].replace('_', ' ').title()}",
                    description=suggestion['reason'],
                    suggested_amount=suggestion['suggested_amount'],
                    expected_return_rate=suggestion['expected_return'],
                    tenure_months=suggestion.get('tenure_months'),
                    risk_level='low',
                    ai_reasoning=suggestion['reason'],
                    user_profile_match_score=80.0
                )
                
                db.add(rec)
            
            await db.commit()
            
            # Re-fetch recommendations
            result = await db.execute(
                select(InvestmentRecommendation)
                .filter(InvestmentRecommendation.user_id == current_user.id)
                .filter(InvestmentRecommendation.is_acted_upon == False)
                .order_by(InvestmentRecommendation.created_at.desc())
                .limit(10)
            )
            recommendations = result.scalars().all()
    
    return recommendations


@router.get("/{investment_id}", response_model=InvestmentResponse)
async def get_investment(
    investment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get specific investment"""
    
    result = await db.execute(
        select(Investment).filter(
            Investment.id == investment_id,
            Investment.user_id == current_user.id
        )
    )
    investment = result.scalar_one_or_none()
    
    if not investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found"
        )
    
    return investment


@router.patch("/{investment_id}", response_model=InvestmentResponse)
async def update_investment(
    investment_id: int,
    investment_update: InvestmentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update investment"""
    
    result = await db.execute(
        select(Investment).filter(
            Investment.id == investment_id,
            Investment.user_id == current_user.id
        )
    )
    investment = result.scalar_one_or_none()
    
    if not investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found"
        )
    
    update_data = investment_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(investment, field, value)
    
    # Calculate returns
    investment.actual_return = investment.total_returns
    
    # Check maturity
    if investment.status == 'matured':
        investment.matured_at = datetime.now()
    
    await db.commit()
    await db.refresh(investment)
    
    return investment


@router.patch("/recommendations/{recommendation_id}", response_model=InvestmentRecommendationResponse)
async def update_recommendation(
    recommendation_id: int,
    rec_update: InvestmentRecommendationUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update investment recommendation (mark as acted upon, provide feedback)"""
    
    result = await db.execute(
        select(InvestmentRecommendation).filter(
            InvestmentRecommendation.id == recommendation_id,
            InvestmentRecommendation.user_id == current_user.id
        )
    )
    recommendation = result.scalar_one_or_none()
    
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found"
        )
    
    update_data = rec_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(recommendation, field, value)
    
    if recommendation.is_acted_upon:
        recommendation.acted_upon_at = datetime.now()
    
    await db.commit()
    await db.refresh(recommendation)
    
    return recommendation
