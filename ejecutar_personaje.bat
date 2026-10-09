@echo off
chcp 65001 >nul
title Simulacion de Personajes - Entorno Virtual

cd /d "%~dp0"

echo ========================================================
echo       SIMULACION DE LA TABLA: PERSONAJES
echo ========================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
    set "ACTIVATE_BAT=%~dp0.venv\Scripts\activate.bat"
) else if exist "venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0venv\Scripts\python.exe"
    set "ACTIVATE_BAT=%~dp0venv\Scripts\activate.bat"
) else (
    echo [!] No se encontro un entorno virtual existente.
    echo [*] Creando entorno virtual en .venv automaticamente...
    python -m venv .venv
    set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
    set "ACTIVATE_BAT=%~dp0.venv\Scripts\activate.bat"
    call "%ACTIVATE_BAT%"
    if exist "requirements.txt" (
        "%PYTHON_EXE%" -m pip install -r requirements.txt
    )
)

if defined ACTIVATE_BAT call "%ACTIVATE_BAT%"

echo.
echo  Ejecutando: python simulacion_personaje.py
echo ========================================================
echo.

"%PYTHON_EXE%" simulacion_personaje.py

echo.
echo ========================================================
echo                  PROCESO FINALIZADO
echo ========================================================
pause
