from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.vehicle import Vehicle, VehicleHealthCheck
from app.auth import get_current_active_user
from app.schemas.vehicle import (
    VehicleCreate, VehicleResponse, VehicleUpdate,
    VehicleHealthCheckCreate, VehicleHealthCheckResponse,
    VehicleHealthCheckUpdate, DiagnosticResult
)
from app.services import gemini_service
import aiofiles
import os
from datetime import datetime
from app.config import settings

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


@router.post("", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    vehicle_data: VehicleCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Add a new vehicle"""
    
    # Check if vehicle number already exists
    result = await db.execute(
        select(Vehicle).filter(Vehicle.vehicle_number == vehicle_data.vehicle_number)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vehicle number already registered"
        )
    
    new_vehicle = Vehicle(
        user_id=current_user.id,
        **vehicle_data.model_dump()
    )
    
    db.add(new_vehicle)
    await db.commit()
    await db.refresh(new_vehicle)
    
    return new_vehicle


@router.get("", response_model=List[VehicleResponse])
async def get_vehicles(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's vehicles"""
    
    result = await db.execute(
        select(Vehicle)
        .filter(Vehicle.user_id == current_user.id)
        .filter(Vehicle.is_active == True)
    )
    vehicles = result.scalars().all()
    
    return vehicles


@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(
    vehicle_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get specific vehicle"""
    
    result = await db.execute(
        select(Vehicle).filter(
            Vehicle.id == vehicle_id,
            Vehicle.user_id == current_user.id
        )
    )
    vehicle = result.scalar_one_or_none()
    
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    return vehicle


@router.patch("/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(
    vehicle_id: int,
    vehicle_update: VehicleUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update vehicle information"""
    
    result = await db.execute(
        select(Vehicle).filter(
            Vehicle.id == vehicle_id,
            Vehicle.user_id == current_user.id
        )
    )
    vehicle = result.scalar_one_or_none()
    
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    update_data = vehicle_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(vehicle, field, value)
    
    await db.commit()
    await db.refresh(vehicle)
    
    return vehicle


@router.post("/{vehicle_id}/health-check", response_model=VehicleHealthCheckResponse, status_code=status.HTTP_201_CREATED)
async def create_health_check_with_images(
    vehicle_id: int,
    images: List[UploadFile] = File(...),
    check_type: str = "image_diagnostic",
    odometer_reading: float = 0,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload vehicle images for AI diagnostic"""
    
    # Verify vehicle ownership
    result = await db.execute(
        select(Vehicle).filter(
            Vehicle.id == vehicle_id,
            Vehicle.user_id == current_user.id
        )
    )
    vehicle = result.scalar_one_or_none()
    
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    # Save images
    upload_dir = os.path.join(settings.UPLOAD_DIR, "vehicles")
    os.makedirs(upload_dir, exist_ok=True)
    
    image_urls = []
    image_bytes_list = []
    
    for idx, image_file in enumerate(images):
        file_path = os.path.join(
            upload_dir,
            f"vehicle_{vehicle_id}_{datetime.now().timestamp()}_{idx}.jpg"
        )
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await image_file.read()
            await f.write(content)
            image_bytes_list.append(content)
        
        image_urls.append(file_path)
    
    # Analyze images with Gemini
    try:
        analysis = await gemini_service.analyze_vehicle_images(
            image_bytes_list,
            context=f"Vehicle: {vehicle.make} {vehicle.model}, Odometer: {odometer_reading or vehicle.current_odometer_km}km"
        )
        
        # Create health check record
        health_check = VehicleHealthCheck(
            vehicle_id=vehicle_id,
            check_type=check_type,
            image_urls=image_urls,
            ai_analysis=str(analysis),
            detected_issues=analysis.get('detected_issues', []),
            severity_score=analysis.get('severity_score', 0),
            tire_condition=analysis.get('tire_condition'),
            engine_oil_level=analysis.get('engine_oil_level'),
            brake_condition=analysis.get('brake_condition'),
            battery_health=analysis.get('battery_health'),
            body_damage=analysis.get('body_damage'),
            immediate_action_required=analysis.get('immediate_action_required', False),
            recommendations='\n'.join(analysis.get('recommendations', [])),
            estimated_repair_cost=None,
            odometer_reading=odometer_reading or vehicle.current_odometer_km
        )
        
        db.add(health_check)
        await db.commit()
        await db.refresh(health_check)
        
        # Create alert if immediate action required
        if health_check.immediate_action_required:
            from app.models.alert import Alert
            
            alert = Alert(
                user_id=current_user.id,
                alert_type="vehicle_maintenance",
                priority="critical",
                title="🔴 Immediate Vehicle Attention Required",
                message=f"Your {vehicle.vehicle_number} needs urgent maintenance. {health_check.recommendations[:200]}",
                action_required=True,
                action_type="book_service",
                alert_metadata={'vehicle_id': vehicle_id, 'check_id': health_check.id}
            )
            
            db.add(alert)
            await db.commit()
            
            # Send WhatsApp alert
            if current_user.whatsapp_number:
                from app.services import whatsapp_service
                whatsapp_service.send_vehicle_alert(
                    current_user.whatsapp_number,
                    "Critical vehicle issues detected",
                    "critical",
                    health_check.recommendations[:200]
                )
        
        return health_check
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image analysis failed: {str(e)}"
        )


@router.get("/{vehicle_id}/health-checks", response_model=List[VehicleHealthCheckResponse])
async def get_health_checks(
    vehicle_id: int,
    limit: int = 10,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get vehicle health check history"""
    
    # Verify vehicle ownership
    result = await db.execute(
        select(Vehicle).filter(
            Vehicle.id == vehicle_id,
            Vehicle.user_id == current_user.id
        )
    )
    vehicle = result.scalar_one_or_none()
    
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    # Get health checks
    result = await db.execute(
        select(VehicleHealthCheck)
        .filter(VehicleHealthCheck.vehicle_id == vehicle_id)
        .order_by(VehicleHealthCheck.created_at.desc())
        .limit(limit)
    )
    checks = result.scalars().all()
    
    return checks


@router.get("/{vehicle_id}/health-checks/{check_id}", response_model=VehicleHealthCheckResponse)
async def get_health_check(
    vehicle_id: int,
    check_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get specific health check"""
    
    result = await db.execute(
        select(VehicleHealthCheck)
        .join(Vehicle)
        .filter(
            VehicleHealthCheck.id == check_id,
            VehicleHealthCheck.vehicle_id == vehicle_id,
            Vehicle.user_id == current_user.id
        )
    )
    check = result.scalar_one_or_none()
    
    if not check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health check not found"
        )
    
    return check
