from sqlalchemy.orm import Session
from app.models.models import Vehicle, WorkSession, Trip, PlatformCommission
from app.schemas.schemas import (
    VehicleCreate, WorkSessionCreate, TripCreate, PlatformCommissionCreate,
    ProfitabilitySummary, TripAnalysis
)


class VehicleService:
    @staticmethod
    def create_vehicle(db: Session, vehicle: VehicleCreate):
        db_vehicle = Vehicle(**vehicle.model_dump())
        db.add(db_vehicle)
        db.commit()
        db.refresh(db_vehicle)
        return db_vehicle

    @staticmethod
    def get_vehicles(db: Session):
        return db.query(Vehicle).all()

    @staticmethod
    def get_vehicle(db: Session, vehicle_id: int):
        return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    @staticmethod
    def delete_vehicle(db: Session, vehicle_id: int):
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if vehicle:
            db.delete(vehicle)
            db.commit()
            return True
        return False

    @staticmethod
    def update_vehicle(db: Session, vehicle_id: int, data: dict):
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            return None
        for k, v in data.items():
            if v is not None:
                setattr(vehicle, k, v)
        db.commit()
        db.refresh(vehicle)
        return vehicle

    @staticmethod
    def set_active_vehicle(db: Session, vehicle_id: int):
        db.query(Vehicle).update({Vehicle.is_active: 0})
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if vehicle:
            vehicle.is_active = 1
            db.commit()
            db.refresh(vehicle)
        return vehicle


class WorkSessionService:
    @staticmethod
    def create_session(db: Session, session_data: WorkSessionCreate):
        db_session = WorkSession(**session_data.model_dump())
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session

    @staticmethod
    def get_sessions(db: Session, vehicle_id: int = None):
        query = db.query(WorkSession)
        if vehicle_id:
            query = query.filter(WorkSession.vehicle_id == vehicle_id)
        return query.all()

    @staticmethod
    def get_session(db: Session, session_id: int):
        return db.query(WorkSession).filter(WorkSession.id == session_id).first()

    @staticmethod
    def delete_session(db: Session, session_id: int):
        session = db.query(WorkSession).filter(WorkSession.id == session_id).first()
        if session:
            db.delete(session)
            db.commit()
            return True
        return False

    @staticmethod
    def update_session(db: Session, session_id: int, data: dict):
        session = db.query(WorkSession).filter(WorkSession.id == session_id).first()
        if not session:
            return None
        for k, v in data.items():
            if v is not None:
                setattr(session, k, v)
        db.commit()
        db.refresh(session)
        return session


class TripService:
    @staticmethod
    def create_trip(db: Session, trip: TripCreate):
        db_trip = Trip(**trip.model_dump())
        db.add(db_trip)
        db.commit()
        db.refresh(db_trip)
        return db_trip

    @staticmethod
    def get_trips(db: Session, session_id: int):
        return db.query(Trip).filter(Trip.session_id == session_id).all()


class PlatformCommissionService:
    @staticmethod
    def create_commission(db: Session, commission: PlatformCommissionCreate):
        db_commission = PlatformCommission(**commission.model_dump())
        db.add(db_commission)
        db.commit()
        db.refresh(db_commission)
        return db_commission

    @staticmethod
    def get_commission(db: Session, platform_name: str):
        return db.query(PlatformCommission).filter(
            PlatformCommission.platform_name == platform_name
        ).first()

    @staticmethod
    def get_all_commissions(db: Session):
        return db.query(PlatformCommission).all()

    @staticmethod
    def update_commission(db: Session, platform_name: str, percentage: float):
        commission = db.query(PlatformCommission).filter(
            PlatformCommission.platform_name == platform_name
        ).first()
        if commission:
            commission.commission_percentage = percentage
            db.commit()
            db.refresh(commission)
            return commission
        return None


class ProfitabilityService:
    @staticmethod
    def calculate_session_profitability(
        db: Session, session_id: int
    ) -> ProfitabilitySummary:
        session = db.query(WorkSession).filter(WorkSession.id == session_id).first()
        if not session:
            return None

        vehicle = db.query(Vehicle).filter(Vehicle.id == session.vehicle_id).first()
        commission = db.query(PlatformCommission).filter(
            PlatformCommission.platform_name == session.platform
        ).first()

        fuel_cost = (session.km_driven / vehicle.consumption_km_per_gallon) * vehicle.fuel_price_per_gallon
        commission_cost = session.total_income * (commission.commission_percentage / 100) if commission else 0
        wear_cost = session.km_driven * vehicle.maintenance_cost_per_km
        net_profit = session.total_income - fuel_cost - commission_cost - wear_cost
        profit_per_hour = net_profit / session.hours_worked if session.hours_worked > 0 else 0
        profit_per_km = net_profit / session.km_driven if session.km_driven > 0 else 0

        return ProfitabilitySummary(
            total_income=session.total_income,
            fuel_cost=round(fuel_cost, 2),
            commission_cost=round(commission_cost, 2),
            wear_cost=round(wear_cost, 2),
            net_profit=round(net_profit, 2),
            profit_per_hour=round(profit_per_hour, 2),
            profit_per_km=round(profit_per_km, 2)
        )

    @staticmethod
    def analyze_trip(
        db: Session, vehicle_id: int, platform: str,
        distance_km: float, payment: float, duration_minutes: float
    ) -> TripAnalysis:
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        commission = db.query(PlatformCommission).filter(
            PlatformCommission.platform_name == platform
        ).first()

        fuel_cost = (distance_km / vehicle.consumption_km_per_gallon) * vehicle.fuel_price_per_gallon
        commission_cost = payment * (commission.commission_percentage / 100) if commission else 0
        net_profit = payment - fuel_cost - commission_cost
        profit_per_km = net_profit / distance_km if distance_km > 0 else 0

        if profit_per_km >= 0.50:
            rating = "Excelente"
        elif profit_per_km >= 0.30:
            rating = "Buena"
        elif profit_per_km >= 0.15:
            rating = "Regular"
        else:
            rating = "Mala"

        return TripAnalysis(
            distance_km=distance_km,
            payment=payment,
            duration_minutes=duration_minutes,
            fuel_cost=round(fuel_cost, 2),
            commission_cost=round(commission_cost, 2),
            net_profit=round(net_profit, 2),
            profitability_rating=rating,
            profit_per_km=round(profit_per_km, 2)
        )
