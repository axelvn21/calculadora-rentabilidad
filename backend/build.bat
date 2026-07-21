@echo off
echo ========================================
echo  Construyendo Ejecutable...
echo ========================================

cd /d "%~dp0"

echo.
echo [1/3] Instalando PyInstaller...
pip install pyinstaller --quiet

echo.
echo [2/3] Construyendo ejecutable...
pyinstaller calculadora.spec --clean --noconfirm

echo.
echo [3/3] Listo!
echo.
echo El ejecutable se encuentra en: dist\CalculadoraRentabilidad\CalculadoraRentabilidad.exe
echo.
echo Para ejecutar: dist\CalculadoraRentabilidad\CalculadoraRentabilidad.exe
echo.
pause
