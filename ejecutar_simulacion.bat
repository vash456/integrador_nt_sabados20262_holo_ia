@echo off
chcp 65001 >nul
title Simulacion de Usuarios - Entorno Virtual

:: 1. Asegurar que el directorio de trabajo sea la carpeta del script
cd /d "%~dp0"

echo ========================================================
echo        INICIANDO ENTORNO Y SCRIPT DE SIMULACION
echo ========================================================
echo.

:: 2. Identificar la ruta del interprete de Python en el entorno virtual
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
    if errorlevel 1 (
        echo [ERROR] No se pudo crear el entorno virtual.
        echo Asegurate de tener Python instalado y anadido al PATH de Windows.
        goto FIN
    )
    set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
    set "ACTIVATE_BAT=%~dp0.venv\Scripts\activate.bat"
    echo [+] Activando nuevo entorno virtual...
    call "%ACTIVATE_BAT%"
    if exist "requirements.txt" (
        echo [*] Instalando dependencias desde requirements.txt...
        "%PYTHON_EXE%" -m pip install -r requirements.txt
    )
)

:: 3. Activar el entorno en la sesion actual
if defined ACTIVATE_BAT call "%ACTIVATE_BAT%"

echo.
echo ========================================================
echo  Interprete: %PYTHON_EXE%
echo  Ejecutando: python src/simular_usuarios.py
echo ========================================================
echo.

:: 4. Ejecutar el script usando directamente el binario del entorno virtual
"%PYTHON_EXE%" src/simular_usuarios.py

:FIN
echo.
echo ========================================================
echo                  PROCESO FINALIZADO
echo ========================================================
pause
