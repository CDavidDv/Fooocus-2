@echo off
REM ============================================================================
REM Script para hacer push a GitHub de Fooocus (Windows)
REM Uso: push_to_github.bat
REM ============================================================================

setlocal enabledelayedexpansion

cls
echo.
echo ============================================================================
echo                        PUSH A GITHUB - Fooocus
echo ============================================================================
echo.

REM 1. Verificar que estamos en un repositorio git
if not exist .git (
    echo [ERROR] No estamos en un repositorio git
    echo.
    echo Ejecuta primero: git init
    pause
    exit /b 1
)

REM 2. Verificar que hay un remote configurado
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo [ERROR] No hay un remote 'origin' configurado
    echo.
    echo Configura el remote con:
    echo   git remote add origin https://github.com/tu-usuario/Fooocus.git
    echo.
    pause
    exit /b 1
)

REM 3. Mostrar remote actual
for /f "tokens=*" %%i in ('git remote get-url origin') do set REMOTE_URL=%%i
echo [INFO] Remote configurado: %REMOTE_URL%
echo.

REM 4. Verificar cambios
echo [INFO] Estado actual:
git status --short
echo.

REM 5. Preguntar si continuar
set /p CONTINUE="Continuar con el push? (s/n): "
if /i not "%CONTINUE%"=="s" (
    echo [CANCELADO] Operación cancelada por el usuario
    exit /b 0
)

REM 6. Agregar cambios
echo.
echo [INFO] Agregando cambios...
git add .

REM 7. Verificar si hay cambios pendientes
git diff-index --quiet HEAD --
if errorlevel 1 (
    REM Hay cambios
    echo [INFO] Hay cambios pendientes
    echo.
    set /p COMMIT_MSG="Mensaje de commit: "

    if "!COMMIT_MSG!"=="" (
        set COMMIT_MSG=update: Cambios generales
    )

    echo [INFO] Haciendo commit: '!COMMIT_MSG!'
    git commit -m "!COMMIT_MSG!"
) else (
    REM No hay cambios
    echo [INFO] No hay cambios pendientes
)

REM 8. Hacer push
echo.
echo [INFO] Enviando a GitHub...
echo.

for /f "tokens=*" %%i in ('git rev-parse --abbrev-ref HEAD') do set BRANCH=%%i

git push -u origin %BRANCH%

cls
echo.
echo ============================================================================
echo                         [OK] PUSH COMPLETADO
echo ============================================================================
echo.
echo [DETALLES]
echo   Remote: %REMOTE_URL%
echo   Rama: %BRANCH%
echo.
echo [ENLACES]
echo   Ver en GitHub: %REMOTE_URL%/tree/%BRANCH%
echo.
echo [COMMITS RECIENTES]
git log --oneline -5
echo.

pause
