# Script para PowerShell: Activar entorno virtual y ejecutar la simulacion
$ErrorActionPreference = "Stop"

# Ubicarse en el directorio del script
Set-Location $PSScriptRoot

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "       INICIANDO ENTORNO Y SCRIPT DE SIMULACION (PS)   " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar existencia de .venv
$venvPath = Join-Path $PSScriptRoot ".venv"
$pythonVenv = Join-Path $venvPath "Scripts\python.exe"
$activatePs1 = Join-Path $venvPath "Scripts\Activate.ps1"

if (-not (Test-Path $pythonVenv)) {
    Write-Host "[!] Creando entorno virtual .venv..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "[*] Instalando dependencias de requirements.txt..." -ForegroundColor Yellow
    & $pythonVenv -m pip install -r requirements.txt
}

# Activar en la sesion actual de PowerShell
if (Test-Path $activatePs1) {
    Write-Host "[+] Activando entorno virtual (.venv)..." -ForegroundColor Green
    & $activatePs1
}

Write-Host ""
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host " Ejecutando: python simulacion_tutabla.py              " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

& $pythonVenv simulacion_tutabla.py

Write-Host ""
Write-Host "========================================================" -ForegroundColor Green
Write-Host "                  PROCESO FINALIZADO                    " -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green
