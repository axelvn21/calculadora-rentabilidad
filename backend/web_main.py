import os
import sys
from pathlib import Path

def get_base_path():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent

BASE_PATH = get_base_path()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import settings
from app.core.database import init_db
from app.api.routes.routes import router


def seed_default_data():
    from app.core.database import SessionLocal
    from app.models.models import PlatformCommission, VehicleCatalog, FuelPrice

    db = SessionLocal()
    try:
        existing = db.query(PlatformCommission).first()
        if not existing:
            defaults = [
                PlatformCommission(platform_name="InDrive", commission_percentage=13.79),
                PlatformCommission(platform_name="Uber", commission_percentage=25.0),
                PlatformCommission(platform_name="Taxi", commission_percentage=0.0),
                PlatformCommission(platform_name="Didi", commission_percentage=20.0),
            ]
            db.add_all(defaults)
            db.commit()

        existing_catalog = db.query(VehicleCatalog).first()
        if not existing_catalog:
            vehicles = [
                VehicleCatalog(brand="Chevrolet", model="Spark GT", year_start=2006, year_end=2016, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=40, maintenance_cost_per_km=0.05),
                VehicleCatalog(brand="Chevrolet", model="Spark 1.0", year_start=2016, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=38, maintenance_cost_per_km=0.05),
                VehicleCatalog(brand="Chevrolet", model="Aveo", year_start=2006, year_end=2014, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=32, maintenance_cost_per_km=0.06),
                VehicleCatalog(brand="Chevrolet", model="Sail", year_start=2013, year_end=2019, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=34, maintenance_cost_per_km=0.06),
                VehicleCatalog(brand="Chevrolet", model="Onix", year_start=2012, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=35, maintenance_cost_per_km=0.07),
                VehicleCatalog(brand="Chevrolet", model="Beat", year_start=2011, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=38, maintenance_cost_per_km=0.05),
                VehicleCatalog(brand="Hyundai", model="Atos", year_start=2003, year_end=2014, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=36, maintenance_cost_per_km=0.04),
                VehicleCatalog(brand="Hyundai", model="i10", year_start=2014, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=37, maintenance_cost_per_km=0.05),
                VehicleCatalog(brand="Hyundai", model="Grand i10", year_start=2017, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=36, maintenance_cost_per_km=0.05),
                VehicleCatalog(brand="Hyundai", model="Accent", year_start=2006, year_end=2017, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=33, maintenance_cost_per_km=0.06),
                VehicleCatalog(brand="Hyundai", model="Elantra", year_start=2012, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=34, maintenance_cost_per_km=0.07),
                VehicleCatalog(brand="Hyundai", model="Tucson", year_start=2010, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=26, maintenance_cost_per_km=0.09),
                VehicleCatalog(brand="Kia", model="Morning", year_start=2005, year_end=2017, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=38, maintenance_cost_per_km=0.05),
                VehicleCatalog(brand="Kia", model="Picanto", year_start=2017, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=40, maintenance_cost_per_km=0.05),
                VehicleCatalog(brand="Kia", model="Rio", year_start=2006, year_end=2017, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=34, maintenance_cost_per_km=0.06),
                VehicleCatalog(brand="Kia", model="Forte", year_start=2014, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=35, maintenance_cost_per_km=0.07),
                VehicleCatalog(brand="Kia", model="Sportage", year_start=2011, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=25, maintenance_cost_per_km=0.09),
                VehicleCatalog(brand="Toyota", model="Yaris", year_start=2006, year_end=2018, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=36, maintenance_cost_per_km=0.05),
                VehicleCatalog(brand="Toyota", model="Corolla", year_start=2003, year_end=2019, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=34, maintenance_cost_per_km=0.06),
                VehicleCatalog(brand="Toyota", model="Hilux", year_start=2005, year_end=2022, fuel_type="Diésel Premium", consumption_km_per_gallon=28, maintenance_cost_per_km=0.08),
                VehicleCatalog(brand="Toyota", model="Fortuner", year_start=2006, year_end=2022, fuel_type="Diésel Premium", consumption_km_per_gallon=22, maintenance_cost_per_km=0.10),
                VehicleCatalog(brand="Toyota", model="Prius", year_start=2004, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=55, maintenance_cost_per_km=0.07),
                VehicleCatalog(brand="Nissan", model="March", year_start=2011, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=40, maintenance_cost_per_km=0.05),
                VehicleCatalog(brand="Nissan", model="Versa", year_start=2012, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=36, maintenance_cost_per_km=0.06),
                VehicleCatalog(brand="Nissan", model="Sentra", year_start=2007, year_end=2019, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=34, maintenance_cost_per_km=0.06),
                VehicleCatalog(brand="Nissan", model="Tiida", year_start=2006, year_end=2015, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=33, maintenance_cost_per_km=0.06),
                VehicleCatalog(brand="Nissan", model="X-Trail", year_start=2008, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=24, maintenance_cost_per_km=0.09),
                VehicleCatalog(brand="Suzuki", model="Alto", year_start=2009, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=42, maintenance_cost_per_km=0.04),
                VehicleCatalog(brand="Suzuki", model="Swift", year_start=2005, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=38, maintenance_cost_per_km=0.05),
                VehicleCatalog(brand="Suzuki", model="Celerio", year_start=2014, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=40, maintenance_cost_per_km=0.05),
                VehicleCatalog(brand="Suzuki", model="Vitara", year_start=2005, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=28, maintenance_cost_per_km=0.08),
                VehicleCatalog(brand="Mitsubishi", model="Lancer", year_start=2003, year_end=2017, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=32, maintenance_cost_per_km=0.07),
                VehicleCatalog(brand="Mitsubishi", model="Outlander", year_start=2007, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=24, maintenance_cost_per_km=0.09),
                VehicleCatalog(brand="Mitsubishi", model="Montero Sport", year_start=2009, year_end=2022, fuel_type="Diésel Premium", consumption_km_per_gallon=24, maintenance_cost_per_km=0.10),
                VehicleCatalog(brand="Mazda", model="2", year_start=2011, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=38, maintenance_cost_per_km=0.05),
                VehicleCatalog(brand="Mazda", model="3", year_start=2004, year_end=2018, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=34, maintenance_cost_per_km=0.06),
                VehicleCatalog(brand="Mazda", model="CX-5", year_start=2012, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=28, maintenance_cost_per_km=0.08),
                VehicleCatalog(brand="Renault", model="Clio", year_start=2005, year_end=2019, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=38, maintenance_cost_per_km=0.05),
                VehicleCatalog(brand="Renault", model="Sandero", year_start=2008, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=36, maintenance_cost_per_km=0.05),
                VehicleCatalog(brand="Renault", model="Logan", year_start=2005, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=35, maintenance_cost_per_km=0.05),
                VehicleCatalog(brand="Renault", model="Duster", year_start=2010, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=28, maintenance_cost_per_km=0.07),
                VehicleCatalog(brand="Renault", model="Captur", year_start=2014, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=30, maintenance_cost_per_km=0.07),
                VehicleCatalog(brand="Fiat", model="Uno", year_start=2004, year_end=2018, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=36, maintenance_cost_per_km=0.05),
                VehicleCatalog(brand="Fiat", model="Palio", year_start=2004, year_end=2018, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=34, maintenance_cost_per_km=0.05),
                VehicleCatalog(brand="Fiat", model="Mobi", year_start=2016, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=37, maintenance_cost_per_km=0.05),
                VehicleCatalog(brand="Ford", model="Fiesta", year_start=2004, year_end=2019, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=35, maintenance_cost_per_km=0.06),
                VehicleCatalog(brand="Ford", model="Escape", year_start=2008, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=24, maintenance_cost_per_km=0.09),
                VehicleCatalog(brand="Volkswagen", model="Gol", year_start=2005, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=34, maintenance_cost_per_km=0.05),
                VehicleCatalog(brand="Volkswagen", model="Polo", year_start=2010, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=36, maintenance_cost_per_km=0.06),
                VehicleCatalog(brand="Volkswagen", model="Jetta", year_start=2006, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=32, maintenance_cost_per_km=0.07),
                VehicleCatalog(brand="Volkswagen", model="T-Cross", year_start=2019, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=33, maintenance_cost_per_km=0.07),
                VehicleCatalog(brand="Honda", model="Civic", year_start=2006, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=35, maintenance_cost_per_km=0.06),
                VehicleCatalog(brand="Honda", model="Fit", year_start=2009, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=38, maintenance_cost_per_km=0.05),
                VehicleCatalog(brand="Honda", model="CR-V", year_start=2007, year_end=2022, fuel_type="Extra / Ecopaís", consumption_km_per_gallon=27, maintenance_cost_per_km=0.09),
            ]
            db.add_all(vehicles)
            db.commit()

        existing_fuel = db.query(FuelPrice).first()
        if not existing_fuel:
            fuel_prices = [
                FuelPrice(fuel_type="Extra / Ecopaís", price_per_gallon=3.26, unit="galón"),
                FuelPrice(fuel_type="Súper Premium 95", price_per_gallon=5.61, unit="galón"),
                FuelPrice(fuel_type="Diésel Premium", price_per_gallon=3.20, unit="galón"),
                FuelPrice(fuel_type="Gas GLP", price_per_gallon=1.33, unit="galón (≈$0.35/litro)"),
                FuelPrice(fuel_type="Eléctrico", price_per_gallon=0.10, unit="kWh"),
            ]
            db.add_all(fuel_prices)
            db.commit()
    finally:
        db.close()


from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    init_db()
    seed_default_data()
    yield


webapp = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

webapp.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

webapp.include_router(router, prefix="/api")

STATIC_DIR = BASE_PATH / "static"
if not STATIC_DIR.exists():
    STATIC_DIR = BASE_PATH / "_internal" / "static"

if STATIC_DIR.exists():
    ASSETS_DIR = STATIC_DIR / "assets"
    if ASSETS_DIR.exists():
        webapp.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="static-assets")

    @webapp.get("/{full_path:path}")
    async def serve_spa(request: Request, full_path: str):
        file_path = STATIC_DIR / full_path
        if file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(STATIC_DIR / "index.html"))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(webapp, host="0.0.0.0", port=port, log_level="info")
