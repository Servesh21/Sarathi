from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from datetime import datetime
from app.database import get_db
from app.models.user import User
from app.models.alert import Alert
from app.auth import get_current_active_user
from app.schemas.alert import AlertCreate, AlertResponse, AlertUpdate, AlertStats

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.post("", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
async def create_alert(
    alert_data: AlertCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new alert (internal use)"""
    
    new_alert = Alert(**alert_data.model_dump())
    
    db.add(new_alert)
    await db.commit()
    await db.refresh(new_alert)
    
    return new_alert


@router.get("", response_model=List[AlertResponse])
async def get_alerts(
    status_filter: str = "active",
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's alerts"""
    
    query = select(Alert).filter(Alert.user_id == current_user.id)
    
    if status_filter:
        query = query.filter(Alert.status == status_filter)
    
    query = query.order_by(Alert.created_at.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    alerts = result.scalars().all()
    
    return alerts


@router.get("/stats", response_model=AlertStats)
async def get_alert_stats(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get alert statistics"""
    
    result = await db.execute(
        select(
            func.count(Alert.id).label('total_alerts'),
            func.count(Alert.id).filter(Alert.is_read == False).label('unread_alerts'),
            func.count(Alert.id).filter(Alert.priority == 'critical').label('critical_alerts'),
            func.count(Alert.id).filter(Alert.status == 'active').label('active_alerts')
        )
        .filter(Alert.user_id == current_user.id)
    )
    
    stats = result.first()
    
    # Get alert counts by type
    type_result = await db.execute(
        select(Alert.alert_type, func.count(Alert.id))
        .filter(Alert.user_id == current_user.id)
        .filter(Alert.status == 'active')
        .group_by(Alert.alert_type)
    )
    
    alerts_by_type = {row[0]: row[1] for row in type_result.all()}
    
    return {
        'total_alerts': stats.total_alerts or 0,
        'unread_alerts': stats.unread_alerts or 0,
        'critical_alerts': stats.critical_alerts or 0,
        'active_alerts': stats.active_alerts or 0,
        'alerts_by_type': alerts_by_type
    }


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get specific alert"""
    
    result = await db.execute(
        select(Alert).filter(Alert.id == alert_id, Alert.user_id == current_user.id)
    )
    alert = result.scalar_one_or_none()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    return alert


@router.patch("/{alert_id}", response_model=AlertResponse)
async def update_alert(
    alert_id: int,
    alert_update: AlertUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update alert (mark as read, dismiss, etc.)"""
    
    result = await db.execute(
        select(Alert).filter(Alert.id == alert_id, Alert.user_id == current_user.id)
    )
    alert = result.scalar_one_or_none()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    update_data = alert_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(alert, field, value)
    
    if alert.status == 'resolved':
        alert.resolved_at = datetime.now()
    
    await db.commit()
    await db.refresh(alert)
    
    return alert


@router.post("/{alert_id}/mark-read", response_model=AlertResponse)
async def mark_alert_read(
    alert_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark alert as read"""
    
    result = await db.execute(
        select(Alert).filter(Alert.id == alert_id, Alert.user_id == current_user.id)
    )
    alert = result.scalar_one_or_none()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    alert.is_read = True
    await db.commit()
    await db.refresh(alert)
    
    return alert


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alert(
    alert_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete alert"""
    
    result = await db.execute(
        select(Alert).filter(Alert.id == alert_id, Alert.user_id == current_user.id)
    )
    alert = result.scalar_one_or_none()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    await db.delete(alert)
    await db.commit()
    
    return None
