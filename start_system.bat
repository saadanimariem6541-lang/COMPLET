@echo off
echo ========================================
echo SYSTEME DE GESTION D'ACCES VEHICULES
echo ========================================
echo.

echo Demarrage du backend...
start "Backend Server" python backend/app.py

timeout /t 3 /nobreak >nul

echo Ouverture du dashboard...
start "" "frontend/dashboard_no_logo.html"

echo.
echo ========================================
echo SYSTEME DEMARRE !
echo ========================================
echo.
echo Pour capturer une plaque:
echo   python main.py
echo.
echo Pour arreter le backend, fermez la fenetre "Backend Server"
echo.
pause