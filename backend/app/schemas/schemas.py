from pydantic import BaseModel
from typing import Optional


class VehicleCatalogCreate(BaseModel):
    brand: str
    model: str
    year_start: int
    year_end: Optional[int] = None
    fuel_type: str
    consumption_km_per_gallon: float
    maintenance_cost_per_km: Optional[float] = 0.05


class VehicleCatalogResponse(VehicleCatalogCreate):
    id: int
    user_added: int

    class Config:
        from_attributes = True


class FuelPriceResponse(BaseModel):
    id: int
    fuel_type: str
    price_per_gallon: float
    unit: str

    class Config:
        from_attributes = True


class FuelPriceUpdate(BaseModel):
    price_per_gallon: float


class VehicleCreate(BaseModel):
    brand: str
    model: str
    year: int
    fuel_type: str
    consumption_km_per_gallon: float
    fuel_price_per_gallon: float
    maintenance_cost_per_km: Optional[float] = 0.05
    is_active: Optional[int] = 0


class VehicleResponse(VehicleCreate):
    id: int

    class Config:
        from_attributes = True


class WorkSessionCreate(BaseModel):
    vehicle_id: int
    platform: str
    date: str
    hours_worked: float
    km_driven: Optional[float] = 0
    total_trips: Optional[int] = 0
    total_income: float


class WorkSessionResponse(WorkSessionCreate):
    id: int

    class Config:
        from_attributes = True


class TripCreate(BaseModel):
    session_id: int
    distance_km: float
    payment: float
    duration_minutes: float


class TripResponse(TripCreate):
    id: int

    class Config:
        from_attributes = True


class PlatformCommissionCreate(BaseModel):
    platform_name: str
    commission_percentage: float


class PlatformCommissionResponse(PlatformCommissionCreate):
    id: int

    class Config:
        from_attributes = True


class ProfitabilitySummary(BaseModel):
    total_income: float
    fuel_cost: float
    commission_cost: float
    wear_cost: float
    net_profit: float
    profit_per_hour: float
    profit_per_km: float


class TripAnalysis(BaseModel):
    distance_km: float
    payment: float
    duration_minutes: float
    fuel_cost: float
    commission_cost: float
    net_profit: float
    profitability_rating: str
    profit_per_km: float
