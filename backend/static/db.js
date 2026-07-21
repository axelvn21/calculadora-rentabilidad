const DB_NAME = 'CalculadoraRentabilidad';
const DB_VERSION = 1;

let _db = null;

function openDB() {
    if (_db) return Promise.resolve(_db);
    return new Promise((resolve, reject) => {
        const req = indexedDB.open(DB_NAME, DB_VERSION);
        req.onupgradeneeded = e => {
            const db = e.target.result;
            if (!db.objectStoreNames.contains('vehicles')) db.createObjectStore('vehicles', { keyPath: 'id', autoIncrement: true });
            if (!db.objectStoreNames.contains('sessions')) db.createObjectStore('sessions', { keyPath: 'id', autoIncrement: true });
            if (!db.objectStoreNames.contains('trips')) db.createObjectStore('trips', { keyPath: 'id', autoIncrement: true });
            if (!db.objectStoreNames.contains('catalog')) db.createObjectStore('catalog', { keyPath: 'id', autoIncrement: true });
            if (!db.objectStoreNames.contains('fuel_prices')) db.createObjectStore('fuel_prices', { keyPath: 'id', autoIncrement: true });
            if (!db.objectStoreNames.contains('commissions')) db.createObjectStore('commissions', { keyPath: 'id', autoIncrement: true });
        };
        req.onsuccess = e => { _db = e.target.result; resolve(_db); };
        req.onerror = e => reject(e.target.error);
    });
}

function tx(store, mode) {
    return openDB().then(db => db.transaction(store, mode).objectStore(store));
}

function getAll(store) {
    return tx(store, 'readonly').then(s => new Promise((res, rej) => { const r = s.getAll(); r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error); }));
}

function getById(store, id) {
    return tx(store, 'readonly').then(s => new Promise((res, rej) => { const r = s.get(id); r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error); }));
}

function put(store, data) {
    return tx(store, 'readwrite').then(s => new Promise((res, rej) => { const r = s.put(data); r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error); }));
}

function add(store, data) {
    return tx(store, 'readwrite').then(s => new Promise((res, rej) => { const r = s.add(data); r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error); }));
}

function del(store, id) {
    return tx(store, 'readwrite').then(s => new Promise((res, rej) => { const r = s.delete(id); r.onsuccess = () => res(); r.onerror = () => rej(r.error); }));
}

function clearStore(store) {
    return tx(store, 'readwrite').then(s => new Promise((res, rej) => { const r = s.clear(); r.onsuccess = () => res(); r.onerror = () => rej(r.error); }));
}

function searchCatalog(query) {
    return getAll('catalog').then(items => {
        if (!query) return items;
        const q = query.toLowerCase();
        return items.filter(i => i.brand.toLowerCase().includes(q) || i.model.toLowerCase().includes(q));
    });
}

async function seedData() {
    const existing = await getAll('catalog');
    if (existing.length > 0) return;

    const vehicles = [
        {brand:"Chevrolet",model:"Spark GT",year_start:2006,year_end:2016,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:40,maintenance_cost_per_km:0.05},
        {brand:"Chevrolet",model:"Spark 1.0",year_start:2016,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:38,maintenance_cost_per_km:0.05},
        {brand:"Chevrolet",model:"Aveo",year_start:2006,year_end:2014,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:32,maintenance_cost_per_km:0.06},
        {brand:"Chevrolet",model:"Sail",year_start:2013,year_end:2019,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:34,maintenance_cost_per_km:0.06},
        {brand:"Chevrolet",model:"Onix",year_start:2012,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:35,maintenance_cost_per_km:0.07},
        {brand:"Chevrolet",model:"Beat",year_start:2011,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:38,maintenance_cost_per_km:0.05},
        {brand:"Hyundai",model:"Atos",year_start:2003,year_end:2014,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:36,maintenance_cost_per_km:0.04},
        {brand:"Hyundai",model:"i10",year_start:2014,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:37,maintenance_cost_per_km:0.05},
        {brand:"Hyundai",model:"Grand i10",year_start:2017,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:36,maintenance_cost_per_km:0.05},
        {brand:"Hyundai",model:"Accent",year_start:2006,year_end:2017,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:33,maintenance_cost_per_km:0.06},
        {brand:"Hyundai",model:"Elantra",year_start:2012,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:34,maintenance_cost_per_km:0.07},
        {brand:"Hyundai",model:"Tucson",year_start:2010,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:26,maintenance_cost_per_km:0.09},
        {brand:"Kia",model:"Morning",year_start:2005,year_end:2017,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:38,maintenance_cost_per_km:0.05},
        {brand:"Kia",model:"Picanto",year_start:2017,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:40,maintenance_cost_per_km:0.05},
        {brand:"Kia",model:"Rio",year_start:2006,year_end:2017,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:34,maintenance_cost_per_km:0.06},
        {brand:"Kia",model:"Forte",year_start:2014,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:35,maintenance_cost_per_km:0.07},
        {brand:"Kia",model:"Sportage",year_start:2011,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:25,maintenance_cost_per_km:0.09},
        {brand:"Toyota",model:"Yaris",year_start:2006,year_end:2018,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:36,maintenance_cost_per_km:0.05},
        {brand:"Toyota",model:"Corolla",year_start:2003,year_end:2019,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:34,maintenance_cost_per_km:0.06},
        {brand:"Toyota",model:"Hilux",year_start:2005,year_end:2022,fuel_type:"Diésel Premium",consumption_km_per_gallon:28,maintenance_cost_per_km:0.08},
        {brand:"Toyota",model:"Fortuner",year_start:2006,year_end:2022,fuel_type:"Diésel Premium",consumption_km_per_gallon:22,maintenance_cost_per_km:0.10},
        {brand:"Toyota",model:"Prius",year_start:2004,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:55,maintenance_cost_per_km:0.07},
        {brand:"Nissan",model:"March",year_start:2011,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:40,maintenance_cost_per_km:0.05},
        {brand:"Nissan",model:"Versa",year_start:2012,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:36,maintenance_cost_per_km:0.06},
        {brand:"Nissan",model:"Sentra",year_start:2007,year_end:2019,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:34,maintenance_cost_per_km:0.06},
        {brand:"Nissan",model:"Tiida",year_start:2006,year_end:2015,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:33,maintenance_cost_per_km:0.06},
        {brand:"Nissan",model:"X-Trail",year_start:2008,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:24,maintenance_cost_per_km:0.09},
        {brand:"Suzuki",model:"Alto",year_start:2009,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:42,maintenance_cost_per_km:0.04},
        {brand:"Suzuki",model:"Swift",year_start:2005,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:38,maintenance_cost_per_km:0.05},
        {brand:"Suzuki",model:"Celerio",year_start:2014,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:40,maintenance_cost_per_km:0.05},
        {brand:"Suzuki",model:"Vitara",year_start:2005,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:28,maintenance_cost_per_km:0.08},
        {brand:"Mitsubishi",model:"Lancer",year_start:2003,year_end:2017,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:32,maintenance_cost_per_km:0.07},
        {brand:"Mitsubishi",model:"Outlander",year_start:2007,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:24,maintenance_cost_per_km:0.09},
        {brand:"Mitsubishi",model:"Montero Sport",year_start:2009,year_end:2022,fuel_type:"Diésel Premium",consumption_km_per_gallon:24,maintenance_cost_per_km:0.10},
        {brand:"Mazda",model:"2",year_start:2011,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:38,maintenance_cost_per_km:0.05},
        {brand:"Mazda",model:"3",year_start:2004,year_end:2018,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:34,maintenance_cost_per_km:0.06},
        {brand:"Mazda",model:"CX-5",year_start:2012,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:28,maintenance_cost_per_km:0.08},
        {brand:"Renault",model:"Clio",year_start:2005,year_end:2019,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:38,maintenance_cost_per_km:0.05},
        {brand:"Renault",model:"Sandero",year_start:2008,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:36,maintenance_cost_per_km:0.05},
        {brand:"Renault",model:"Logan",year_start:2005,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:35,maintenance_cost_per_km:0.05},
        {brand:"Renault",model:"Duster",year_start:2010,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:28,maintenance_cost_per_km:0.07},
        {brand:"Renault",model:"Captur",year_start:2014,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:30,maintenance_cost_per_km:0.07},
        {brand:"Fiat",model:"Uno",year_start:2004,year_end:2018,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:36,maintenance_cost_per_km:0.05},
        {brand:"Fiat",model:"Palio",year_start:2004,year_end:2018,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:34,maintenance_cost_per_km:0.05},
        {brand:"Fiat",model:"Mobi",year_start:2016,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:37,maintenance_cost_per_km:0.05},
        {brand:"Ford",model:"Fiesta",year_start:2004,year_end:2019,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:35,maintenance_cost_per_km:0.06},
        {brand:"Ford",model:"Escape",year_start:2008,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:24,maintenance_cost_per_km:0.09},
        {brand:"Volkswagen",model:"Gol",year_start:2005,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:34,maintenance_cost_per_km:0.05},
        {brand:"Volkswagen",model:"Polo",year_start:2010,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:36,maintenance_cost_per_km:0.06},
        {brand:"Volkswagen",model:"Jetta",year_start:2006,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:32,maintenance_cost_per_km:0.07},
        {brand:"Volkswagen",model:"T-Cross",year_start:2019,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:33,maintenance_cost_per_km:0.07},
        {brand:"Honda",model:"Civic",year_start:2006,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:35,maintenance_cost_per_km:0.06},
        {brand:"Honda",model:"Fit",year_start:2009,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:38,maintenance_cost_per_km:0.05},
        {brand:"Honda",model:"CR-V",year_start:2007,year_end:2022,fuel_type:"Extra / Ecopaís",consumption_km_per_gallon:27,maintenance_cost_per_km:0.09}
    ];
    for (const v of vehicles) { await add('catalog', { ...v, user_added: 0 }); }

    const fuelPrices = [
        {fuel_type:"Extra / Ecopaís",price_per_gallon:3.26,unit:"galón"},
        {fuel_type:"Súper Premium 95",price_per_gallon:5.61,unit:"galón"},
        {fuel_type:"Diésel Premium",price_per_gallon:3.20,unit:"galón"},
        {fuel_type:"Gas GLP",price_per_gallon:1.33,unit:"galón"},
        {fuel_type:"Eléctrico",price_per_gallon:0.10,unit:"kWh"}
    ];
    for (const f of fuelPrices) { await add('fuel_prices', f); }

    const commissions = [
        {platform_name:"InDrive",commission_percentage:13.79},
        {platform_name:"Uber",commission_percentage:25.0},
        {platform_name:"Taxi",commission_percentage:0.0},
        {platform_name:"Didi",commission_percentage:20.0}
    ];
    for (const c of commissions) { await add('commissions', c); }
}

async function offlineApi(path, options = {}) {
    await seedData();
    const method = (options.method || 'GET').toUpperCase();
    const parts = path.replace(/^\//, '').split('/');
    const resource = parts[0];

    if (resource === 'vehicles') {
        if (parts.length === 1) {
            if (method === 'GET') return await getAll('vehicles');
            if (method === 'POST') {
                const body = typeof options.body === 'string' ? JSON.parse(options.body) : options.body;
                const id = await add('vehicles', body);
                return { ...body, id };
            }
        }
        if (parts.length === 2 && parts[1] === 'activate') {
            const id = parseInt(parts[0].replace('vehicles/', '') || parts[0]);
            const vehicles = await getAll('vehicles');
            for (const v of vehicles) { v.is_active = v.id === id ? 1 : 0; await put('vehicles', v); }
            return vehicles.find(v => v.id === id);
        }
        if (parts.length === 2 && method === 'PUT') {
            const id = parseInt(parts[1]);
            const body = typeof options.body === 'string' ? JSON.parse(options.body) : options.body;
            const existing = await getById('vehicles', id);
            const updated = { ...existing, ...body, id };
            await put('vehicles', updated);
            return updated;
        }
        if (parts.length === 2 && method === 'DELETE') {
            const id = parseInt(parts[1]);
            await del('vehicles', id);
            return { message: "Vehículo eliminado" };
        }
    }

    if (resource === 'vehicle-catalog') {
        const url = new URL('https://x' + path);
        const search = url.searchParams.get('search') || '';
        return await searchCatalog(search);
    }

    if (resource === 'sessions') {
        if (parts.length === 1) {
            if (method === 'GET') return await getAll('sessions');
            if (method === 'POST') {
                const body = typeof options.body === 'string' ? JSON.parse(options.body) : options.body;
                const id = await add('sessions', body);
                return { ...body, id };
            }
        }
        if (parts.length === 2 && method === 'PUT') {
            const id = parseInt(parts[1]);
            const body = typeof options.body === 'string' ? JSON.parse(options.body) : options.body;
            const existing = await getById('sessions', id);
            const updated = { ...existing, ...body, id };
            await put('sessions', updated);
            return updated;
        }
        if (parts.length === 2 && method === 'DELETE') {
            const id = parseInt(parts[1]);
            await del('sessions', id);
            return { message: "Sesión eliminada" };
        }
    }

    if (resource === 'profitability' && parts.length === 2) {
        const sessionId = parseInt(parts[1]);
        const session = await getById('sessions', sessionId);
        if (!session) return null;
        const vehicles = await getAll('vehicles');
        const v = vehicles.find(x => x.id === session.vehicle_id);
        if (!v) return null;
        const fuel = (session.km_driven / v.consumption_km_per_gallon) * v.fuel_price_per_gallon;
        const comm = session.total_income * (commissions_find(session.platform) / 100);
        const wear = session.km_driven * v.maintenance_cost_per_km;
        const net = session.total_income - fuel - comm - wear;
        return {
            total_income: session.total_income,
            fuel_cost: fuel,
            commission_cost: comm,
            wear_cost: wear,
            net_profit: net,
            profit_per_hour: session.hours_worked > 0 ? net / session.hours_worked : 0,
            profit_per_km: session.km_driven > 0 ? net / session.km_driven : 0
        };
    }

    if (resource === 'fuel-prices') {
        return await getAll('fuel_prices');
    }

    if (resource === 'commissions') {
        return await getAll('commissions');
    }

    return null;
}

function commissions_find(platform) {
    const rates = { 'InDrive': 13.79, 'Uber': 25.0, 'Taxi': 0.0, 'Didi': 20.0 };
    return rates[platform] || 0;
}
