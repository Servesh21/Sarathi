from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime, timedelta
from app.database import get_db
from app.models.user import User
from app.models.goal import Goal, GoalProgress
from app.auth import get_current_active_user
from app.schemas.goal import (
    GoalCreate, GoalResponse, GoalUpdate,
    GoalProgressCreate, GoalProgressResponse, GoalInsights
)

router = APIRouter(prefix="/goals", tags=["Goals"])


@router.post("", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
async def create_goal(
    goal_data: GoalCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new financial goal"""
    
    new_goal = Goal(
        user_id=current_user.id,
        **goal_data.model_dump()
    )
    
    db.add(new_goal)
    await db.commit()
    await db.refresh(new_goal)
    
    return new_goal


@router.get("", response_model=List[GoalResponse])
async def get_goals(
    status_filter: str = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's goals"""
    
    query = select(Goal).filter(Goal.user_id == current_user.id)
    
    if status_filter:
        query = query.filter(Goal.status == status_filter)
    
    query = query.order_by(Goal.created_at.desc())
    
    result = await db.execute(query)
    goals = result.scalars().all()
    
    return goals


@router.get("/{goal_id}", response_model=GoalResponse)
async def get_goal(
    goal_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get specific goal"""
    
    result = await db.execute(
        select(Goal).filter(Goal.id == goal_id, Goal.user_id == current_user.id)
    )
    goal = result.scalar_one_or_none()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    
    return goal


@router.patch("/{goal_id}", response_model=GoalResponse)
async def update_goal(
    goal_id: int,
    goal_update: GoalUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update goal"""
    
    result = await db.execute(
        select(Goal).filter(Goal.id == goal_id, Goal.user_id == current_user.id)
    )
    goal = result.scalar_one_or_none()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    
    update_data = goal_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(goal, field, value)
    
    # Update completion percentage
    goal.completion_percentage = goal.percentage_complete
    
    # Mark as completed if target reached
    if goal.current_amount >= goal.target_amount and goal.status != 'completed':
        goal.status = 'completed'
        goal.completed_at = datetime.now()
    
    await db.commit()
    await db.refresh(goal)
    
    return goal


@router.post("/{goal_id}/progress", response_model=GoalProgressResponse, status_code=status.HTTP_201_CREATED)
async def add_goal_progress(
    goal_id: int,
    progress_data: GoalProgressCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Add progress to goal"""
    
    result = await db.execute(
        select(Goal).filter(Goal.id == goal_id, Goal.user_id == current_user.id)
    )
    goal = result.scalar_one_or_none()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    
    # Create progress entry
    progress = GoalProgress(
        goal_id=goal_id,
        amount_added=progress_data.amount_added,
        previous_total=goal.current_amount,
        new_total=goal.current_amount + progress_data.amount_added,
        notes=progress_data.notes,
        source=progress_data.source
    )
    
    # Update goal current amount
    goal.current_amount += progress_data.amount_added
    goal.completion_percentage = goal.percentage_complete
    
    # Check if goal completed
    if goal.current_amount >= goal.target_amount:
        goal.status = 'completed'
        goal.completed_at = datetime.now()
    
    db.add(progress)
    await db.commit()
    await db.refresh(progress)
    await db.refresh(goal)
    
    return progress


@router.get("/{goal_id}/progress", response_model=List[GoalProgressResponse])
async def get_goal_progress_history(
    goal_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get goal progress history"""
    
    # Verify goal ownership
    result = await db.execute(
        select(Goal).filter(Goal.id == goal_id, Goal.user_id == current_user.id)
    )
    goal = result.scalar_one_or_none()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    
    # Get progress history
    result = await db.execute(
        select(GoalProgress)
        .filter(GoalProgress.goal_id == goal_id)
        .order_by(GoalProgress.created_at.desc())
    )
    progress_history = result.scalars().all()
    
    return progress_history


@router.get("/{goal_id}/insights", response_model=GoalInsights)
async def get_goal_insights(
    goal_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get AI-powered insights for goal"""
    
    result = await db.execute(
        select(Goal).filter(Goal.id == goal_id, Goal.user_id == current_user.id)
    )
    goal = result.scalar_one_or_none()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    
    # Calculate insights
    remaining_amount = goal.target_amount - goal.current_amount
    
    if goal.target_date:
        days_to_target = (goal.target_date - datetime.now()).days
        
        if days_to_target > 0:
            required_daily_savings = remaining_amount / days_to_target
            required_monthly_savings = required_daily_savings * 30
        else:
            days_to_target = 0
            required_monthly_savings = remaining_amount
    else:
        days_to_target = 0
        required_monthly_savings = goal.monthly_contribution
    
    # Determine pace
    if goal.monthly_contribution > 0 and goal.target_date:
        months_to_target = days_to_target / 30
        projected_amount = goal.current_amount + (goal.monthly_contribution * months_to_target)
        
        if projected_amount >= goal.target_amount:
            pace = "ahead"
        elif projected_amount >= goal.target_amount * 0.9:
            pace = "on_track"
        else:
            pace = "behind"
    else:
        pace = "on_track"
    
    # Projected completion date
    if goal.monthly_contribution > 0:
        months_needed = remaining_amount / goal.monthly_contribution
        projected_completion = datetime.now() + timedelta(days=months_needed * 30)
    else:
        projected_completion = None
    
    # Generate recommendations
    recommendations = []
    
    if pace == "behind":
        recommendations.append(f"Increase monthly contribution to ₹{required_monthly_savings:.0f} to stay on track")
    elif pace == "ahead":
        recommendations.append("You're ahead of schedule! Consider increasing your target or starting a new goal")
    
    if goal.completion_percentage < 25:
        recommendations.append("Stay consistent with contributions to build momentum")
    elif goal.completion_percentage > 75:
        recommendations.append("Almost there! Keep going to reach your goal")
    
    if goal.monthly_contribution < required_monthly_savings:
        recommendations.append(f"Current pace: ₹{goal.monthly_contribution:.0f}/month · Needed: ₹{required_monthly_savings:.0f}/month")
    
    return GoalInsights(
        goal_id=goal.id,
        goal_name=goal.goal_name,
        days_to_target=max(days_to_target, 0),
        required_monthly_savings=required_monthly_savings,
        current_pace=pace,
        projected_completion_date=projected_completion,
        recommendations=recommendations
    )


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(
    goal_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete goal"""
    
    result = await db.execute(
        select(Goal).filter(Goal.id == goal_id, Goal.user_id == current_user.id)
    )
    goal = result.scalar_one_or_none()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    
    await db.delete(goal)
    await db.commit()
    
    return None
