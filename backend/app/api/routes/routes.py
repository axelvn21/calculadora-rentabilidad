from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.database import get_db
from app.schemas.schemas import (
    VehicleCreate, VehicleResponse,
    VehicleCatalogCreate, VehicleCatalogResponse,
    FuelPriceResponse, FuelPriceUpdate,
    WorkSessionCreate, WorkSessionResponse,
    TripCreate, TripResponse,
    PlatformCommissionCreate, PlatformCommissionResponse,
    ProfitabilitySummary, TripAnalysis
)
from app.services.services import (
    VehicleService, WorkSessionService, TripService,
    PlatformCommissionService, ProfitabilityService
)
from app.models.models import VehicleCatalog, FuelPrice

router = APIRouter()


@router.get("/vehicle-catalog", response_model=list[VehicleCatalogResponse])
def search_vehicle_catalog(
    search: str = Query("", description="Buscar por marca o modelo"),
    db: Session = Depends(get_db)
):
    query = db.query(VehicleCatalog)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                VehicleCatalog.brand.ilike(search_term),
                VehicleCatalog.model.ilike(search_term)
            )
        )
    return query.order_by(VehicleCatalog.brand, VehicleCatalog.model).all()


@router.post("/vehicle-catalog", response_model=VehicleCatalogResponse)
def create_vehicle_catalog(item: VehicleCatalogCreate, db: Session = Depends(get_db)):
    catalog_item = VehicleCatalog(**item.model_dump(), user_added=1)
    db.add(catalog_item)
    db.commit()
    db.refresh(catalog_item)
    return catalog_item


@router.delete("/vehicle-catalog/{item_id}")
def delete_vehicle_catalog(item_id: int, db: Session = Depends(get_db)):
    item = db.query(VehicleCatalog).filter(VehicleCatalog.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado en catálogo")
    db.delete(item)
    db.commit()
    return {"message": "Eliminado del catálogo"}


@router.get("/fuel-prices", response_model=list[FuelPriceResponse])
def get_fuel_prices(db: Session = Depends(get_db)):
    return db.query(FuelPrice).all()


@router.put("/fuel-prices/{fuel_type}")
def update_fuel_price(fuel_type: str, update: FuelPriceUpdate, db: Session = Depends(get_db)):
    price = db.query(FuelPrice).filter(FuelPrice.fuel_type == fuel_type).first()
    if not price:
        raise HTTPException(status_code=404, detail="Tipo de combustible no encontrado")
    price.price_per_gallon = update.price_per_gallon
    from datetime import datetime
    price.last_updated = datetime.utcnow()
    db.commit()
    return {"message": "Precio actualizado", "fuel_type": fuel_type, "price": update.price_per_gallon}


@router.post("/vehicles", response_model=VehicleResponse)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    return VehicleService.create_vehicle(db, vehicle)


@router.get("/vehicles", response_model=list[VehicleResponse])
def get_vehicles(db: Session = Depends(get_db)):
    return VehicleService.get_vehicles(db)


@router.get("/vehicles/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = VehicleService.get_vehicle(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehicle


@router.delete("/vehicles/{vehicle_id}")
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    if not VehicleService.delete_vehicle(db, vehicle_id):
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return {"message": "Vehículo eliminado"}


@router.put("/vehicles/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(vehicle_id: int, vehicle: VehicleCreate, db: Session = Depends(get_db)):
    updated = VehicleService.update_vehicle(db, vehicle_id, vehicle.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return updated


@router.put("/vehicles/{vehicle_id}/activate", response_model=VehicleResponse)
def activate_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    activated = VehicleService.set_active_vehicle(db, vehicle_id)
    if not activated:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return activated


@router.post("/sessions", response_model=WorkSessionResponse)
def create_session(session: WorkSessionCreate, db: Session = Depends(get_db)):
    return WorkSessionService.create_session(db, session)


@router.get("/sessions", response_model=list[WorkSessionResponse])
def get_sessions(vehicle_id: int = None, db: Session = Depends(get_db)):
    return WorkSessionService.get_sessions(db, vehicle_id)


@router.get("/sessions/{session_id}", response_model=WorkSessionResponse)
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = WorkSessionService.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return session


@router.delete("/sessions/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    if not WorkSessionService.delete_session(db, session_id):
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return {"message": "Sesión eliminada"}


@router.put("/sessions/{session_id}", response_model=WorkSessionResponse)
def update_session(session_id: int, session: WorkSessionCreate, db: Session = Depends(get_db)):
    updated = WorkSessionService.update_session(db, session_id, session.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return updated


@router.post("/trips", response_model=TripResponse)
def create_trip(trip: TripCreate, db: Session = Depends(get_db)):
    return TripService.create_trip(db, trip)


@router.get("/trips/{session_id}", response_model=list[TripResponse])
def get_trips(session_id: int, db: Session = Depends(get_db)):
    return TripService.get_trips(db, session_id)


@router.post("/commissions", response_model=PlatformCommissionResponse)
def create_commission(commission: PlatformCommissionCreate, db: Session = Depends(get_db)):
    return PlatformCommissionService.create_commission(db, commission)


@router.get("/commissions", response_model=list[PlatformCommissionResponse])
def get_commissions(db: Session = Depends(get_db)):
    return PlatformCommissionService.get_all_commissions(db)


@router.put("/commissions/{platform_name}", response_model=PlatformCommissionResponse)
def update_commission(platform_name: str, percentage: float, db: Session = Depends(get_db)):
    commission = PlatformCommissionService.update_commission(db, platform_name, percentage)
    if not commission:
        raise HTTPException(status_code=404, detail="Plataforma no encontrada")
    return commission


@router.get("/profitability/{session_id}", response_model=ProfitabilitySummary)
def get_session_profitability(session_id: int, db: Session = Depends(get_db)):
    result = ProfitabilityService.calculate_session_profitability(db, session_id)
    if not result:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return result


@router.post("/analyze-trip", response_model=TripAnalysis)
def analyze_trip(
    vehicle_id: int, platform: str,
    distance_km: float, payment: float, duration_minutes: float,
    db: Session = Depends(get_db)
):
    return ProfitabilityService.analyze_trip(
        db, vehicle_id, platform, distance_km, payment, duration_minutes
    )
