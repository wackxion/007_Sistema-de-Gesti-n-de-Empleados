@echo off
chcp 65001 >nul
echo ========================================
echo   Sistema de Gestion de Empleados
echo ========================================
echo.
echo Selecciona el modo:
echo   1 - Interfaz Grafica (botones)
echo   2 - Consola (terminal)
echo.

set /p opcion="Opcion (1/2): "

if "%opcion%"=="1" goto GUI
if "%opcion%"=="2" goto CONSOLA
goto FIN

:GUI
echo.
echo Ejecutando interfaz grafica...
python src\gui.py
goto FIN

:CONSOLA
echo.
echo Ejecutando en consola...
python src\main.py
goto FIN

:FIN
pause
