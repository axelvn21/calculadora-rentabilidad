from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    fuel_type = Column(String, nullable=False)
    consumption_km_per_gallon = Column(Float, nullable=False)
    fuel_price_per_gallon = Column(Float, nullable=False)
    maintenance_cost_per_km = Column(Float, default=0.05)
    is_active = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    work_sessions = relationship("WorkSession", back_populates="vehicle")


class WorkSession(Base):
    __tablename__ = "work_sessions"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    platform = Column(String, nullable=False)
    date = Column(String, nullable=False)
    hours_worked = Column(Float, nullable=False)
    km_driven = Column(Float, nullable=False)
    total_trips = Column(Integer, nullable=False)
    total_income = Column(Float, nullable=False)

    vehicle = relationship("Vehicle", back_populates="work_sessions")
    trips = relationship("Trip", back_populates="session")


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("work_sessions.id"), nullable=False)
    distance_km = Column(Float, nullable=False)
    payment = Column(Float, nullable=False)
    duration_minutes = Column(Float, nullable=False)

    session = relationship("WorkSession", back_populates="trips")


class VehicleCatalog(Base):
    __tablename__ = "vehicle_catalog"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year_start = Column(Integer, nullable=False)
    year_end = Column(Integer, nullable=True)
    fuel_type = Column(String, nullable=False)
    consumption_km_per_gallon = Column(Float, nullable=False)
    maintenance_cost_per_km = Column(Float, default=0.05)
    user_added = Column(Integer, default=0)


class FuelPrice(Base):
    __tablename__ = "fuel_prices"

    id = Column(Integer, primary_key=True, index=True)
    fuel_type = Column(String, unique=True, nullable=False)
    price_per_gallon = Column(Float, nullable=False)
    unit = Column(String, default="galón")
    last_updated = Column(DateTime, default=datetime.utcnow)


class PlatformCommission(Base):
    __tablename__ = "platform_commissions"

    id = Column(Integer, primary_key=True, index=True)
    platform_name = Column(String, unique=True, nullable=False)
    commission_percentage = Column(Float, nullable=False)
