from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.db.database import get_db
from app.db.models import User, Vehicle, Trip
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


class UserProfile(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    
    class Config:
        from_attributes = True


class VehicleCreate(BaseModel):
    make: str
    model: str
    year: int
    license_plate: str
    vehicle_type: Optional[str] = "car"


class VehicleResponse(BaseModel):
    id: int
    make: str
    model: str
    year: int
    license_plate: str
    vehicle_type: str
    
    class Config:
        from_attributes = True


class TripCreate(BaseModel):
    vehicle_id: int
    start_location: str
    end_location: str
    distance_km: float
    earnings: Optional[float] = 0.0


class TripResponse(BaseModel):
    id: int
    vehicle_id: int
    start_location: str
    end_location: str
    distance_km: float
    earnings: float
    trip_date: str
    
    class Config:
        from_attributes = True


@router.get("/profile", response_model=UserProfile)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """Get the current user's profile"""
    return current_user


@router.put("/profile")
async def update_user_profile(
    full_name: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update the current user's profile"""
    if full_name:
        current_user.full_name = full_name
    
    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/vehicles", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    vehicle: VehicleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a new vehicle to the user's garage"""
    new_vehicle = Vehicle(
        user_id=current_user.id,
        make=vehicle.make,
        model=vehicle.model,
        year=vehicle.year,
        license_plate=vehicle.license_plate,
        vehicle_type=vehicle.vehicle_type
    )
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle


@router.get("/vehicles", response_model=List[VehicleResponse])
async def get_user_vehicles(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all vehicles in the user's garage"""
    vehicles = db.query(Vehicle).filter(Vehicle.user_id == current_user.id).all()
    return vehicles


@router.post("/trips", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
async def create_trip(
    trip: TripCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log a new trip"""
    # Verify vehicle belongs to user
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == trip.vehicle_id,
        Vehicle.user_id == current_user.id
    ).first()
    
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found or does not belong to user"
        )
    
    new_trip = Trip(
        user_id=current_user.id,
        vehicle_id=trip.vehicle_id,
        start_location=trip.start_location,
        end_location=trip.end_location,
        distance_km=trip.distance_km,
        earnings=trip.earnings
    )
    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)
    return new_trip


@router.get("/trips", response_model=List[TripResponse])
async def get_user_trips(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50
):
    """Get the user's trip history"""
    trips = db.query(Trip).filter(
        Trip.user_id == current_user.id
    ).order_by(Trip.trip_date.desc()).limit(limit).all()
    return trips
