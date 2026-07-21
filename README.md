# Calculadora de Rentabilidad para Conductores

App para calcular la ganancia real de conductores de taxi, InDrive, Uber y Didi en Ecuador.

## Instalación (Escritorio)

Descarga `CalculadoraRentabilidad-Instalador.exe` o `CalculadoraRentabilidad.zip`.

## Desarrollo

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

## APK (Android)

1. Crear cuenta en GitHub
2. Subir este repositorio
3. El workflow genera el APK automáticamente en Actions → Artifacts

## Deploy Web (Render)

1. Subir a GitHub
2. Crear cuenta en Render.com
3. New → Web Service → Conectar repo
4. Seleccionar `render.yaml`
