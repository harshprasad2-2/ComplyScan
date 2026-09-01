@echo off
REM ComplyScan GitHub Deployment Script
REM Run this after installing Git: https://git-scm.com/download/win

echo.
echo ======================================
echo ComplyScan - GitHub Deployment Script
echo ======================================
echo.

REM Check if git is installed
where git >nul 2>nul
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo Download from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo ✅ Git found

REM Configure git (replace with your details)
git config user.name "Team Nexus"
git config user.email "team@nexus.dev"

echo.
echo Step 1: Initializing git repository...
git init

echo.
echo Step 2: Adding all files...
git add .

echo.
echo Step 3: Creating initial commit...
git commit -m "Initial commit: ComplyScan v1.0.0 - SIH 2026"

echo.
echo ======================================
echo ✅ Local repository ready!
echo ======================================
echo.
echo Next steps:
echo 1. Create repository on GitHub: https://github.com/new
echo 2. Copy the HTTPS URL
echo 3. Run these commands:
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/ComplyScan.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo Then visit:
echo https://github.com/YOUR_USERNAME/ComplyScan
echo.
pause
