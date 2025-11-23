@echo off
REM ============================================================================
REM AssessNex AI Streamlit App - Automated Setup Script (Batch)
REM ============================================================================
REM Usage: setup.bat [command] [port]
REM Commands: run (default), install, clean, dev
REM ============================================================================

setlocal enabledelayedexpansion

REM Colors (using escape sequences for Windows 10+)
set "GREEN=[32m"
set "BLUE=[34m"
set "YELLOW=[33m"
set "RED=[31m"
set "RESET=[0m"

REM Default values
set ACTION=run
set PORT=8501

REM Parse command line arguments
if not "%1"=="" set ACTION=%1
if not "%2"=="" set PORT=%2

REM Print header
cls
echo.
echo %BLUE%      ╔═══════════════════════════════════════════╗%RESET%
echo %BLUE%      ║     AssessNex AI - Streamlit App         ║%RESET%
echo %BLUE%      ║     Setup ^& Installation Script          ║%RESET%
echo %BLUE%      ╚═══════════════════════════════════════════╝%RESET%
echo.

REM Get paths
for /f "delims=" %%i in ('cd') do set CURRENT_DIR=%%i
set VENV_PATH=%CURRENT_DIR%\venv

REM Main logic
if /i "%ACTION%"=="run" goto RUN
if /i "%ACTION%"=="install" goto INSTALL
if /i "%ACTION%"=="clean" goto CLEAN
if /i "%ACTION%"=="dev" goto DEV
goto USAGE

:RUN
cls
echo %BLUE%╔════════════════════════════════════════╗%RESET%
echo %BLUE%║ 🚀 STARTING STREAMLIT APP              ║%RESET%
echo %BLUE%╚════════════════════════════════════════╝%RESET%
echo.

if exist "%VENV_PATH%" (
    echo %YELLOW%→ Virtual environment found, activating...%RESET%
    call "%VENV_PATH%\Scripts\activate.bat"
    echo %GREEN%✓ Virtual environment activated%RESET%
) else (
    echo %YELLOW%→ Virtual environment not found, installing...%RESET%
    python -m venv "%VENV_PATH%"
    call "%VENV_PATH%\Scripts\activate.bat"
    echo %GREEN%✓ Virtual environment created and activated%RESET%
    
    echo %YELLOW%→ Installing dependencies...%RESET%
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    echo %GREEN%✓ Dependencies installed%RESET%
)

echo.
echo %BLUE%╔════════════════════════════════════════╗%RESET%
echo %BLUE%║ ✨ LAUNCHING STREAMLIT                  ║%RESET%
echo %BLUE%╚════════════════════════════════════════╝%RESET%
echo.
echo %GREEN%✓ App is starting at http://localhost:%PORT%%RESET%
echo %YELLOW%→ Press Ctrl+C to stop the server%RESET%
echo.

streamlit run main.py --server.port %PORT%
goto END

:INSTALL
cls
echo %BLUE%╔════════════════════════════════════════╗%RESET%
echo %BLUE%║ 📦 INSTALLING DEPENDENCIES             ║%RESET%
echo %BLUE%╚════════════════════════════════════════╝%RESET%
echo.

if not exist "%VENV_PATH%" (
    echo %YELLOW%→ Creating virtual environment...%RESET%
    python -m venv "%VENV_PATH%"
    echo %GREEN%✓ Virtual environment created%RESET%
)

call "%VENV_PATH%\Scripts\activate.bat"
echo %GREEN%✓ Virtual environment activated%RESET%

echo %YELLOW%→ Upgrading pip...%RESET%
python -m pip install --upgrade pip
echo %GREEN%✓ Pip upgraded%RESET%

echo %YELLOW%→ Installing requirements...%RESET%
pip install -r requirements.txt
echo %GREEN%✓ All dependencies installed%RESET%

echo.
echo %BLUE%╔════════════════════════════════════════╗%RESET%
echo %BLUE%║ ✅ INSTALLATION COMPLETE               ║%RESET%
echo %BLUE%╚════════════════════════════════════════╝%RESET%
echo.
echo %YELLOW%→ To start the app, run: setup.bat run%RESET%
echo.
goto END

:CLEAN
cls
echo %BLUE%╔════════════════════════════════════════╗%RESET%
echo %BLUE%║ 🧹 CLEANING UP                         ║%RESET%
echo %BLUE%╚════════════════════════════════════════╝%RESET%
echo.

if exist "%VENV_PATH%" (
    echo %YELLOW%→ Removing virtual environment...%RESET%
    rmdir /s /q "%VENV_PATH%"
    echo %GREEN%✓ Virtual environment removed%RESET%
) else (
    echo %YELLOW%→ No virtual environment found%RESET%
)

for /d /r . %%d in (__pycache__) do (
    echo %YELLOW%→ Removing %%d%RESET%
    rmdir /s /q "%%d"
)

echo %GREEN%✓ Cache cleared%RESET%

echo.
echo %BLUE%╔════════════════════════════════════════╗%RESET%
echo %BLUE%║ ✅ CLEANUP COMPLETE                    ║%RESET%
echo %BLUE%╚════════════════════════════════════════╝%RESET%
echo.
goto END

:DEV
cls
echo %BLUE%╔════════════════════════════════════════╗%RESET%
echo %BLUE%║ 🛠️ DEVELOPMENT MODE                    ║%RESET%
echo %BLUE%╚════════════════════════════════════════╝%RESET%
echo.

if not exist "%VENV_PATH%" (
    echo %YELLOW%→ Creating virtual environment...%RESET%
    python -m venv "%VENV_PATH%"
    call "%VENV_PATH%\Scripts\activate.bat"
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    call "%VENV_PATH%\Scripts\activate.bat"
)

echo.
echo %BLUE%╔════════════════════════════════════════╗%RESET%
echo %BLUE%║ ✨ LAUNCHING IN DEV MODE                ║%RESET%
echo %BLUE%╚════════════════════════════════════════╝%RESET%
echo.
echo %GREEN%✓ Debug logging enabled%RESET%
echo %YELLOW%→ Press Ctrl+C to stop%RESET%
echo.

streamlit run main.py ^
    --server.port %PORT% ^
    --logger.level=debug ^
    --client.showErrorDetails=true
goto END

:USAGE
cls
echo %BLUE%╔════════════════════════════════════════╗%RESET%
echo %BLUE%║ ❓ USAGE                               ║%RESET%
echo %BLUE%╚════════════════════════════════════════╝%RESET%
echo.
echo %YELLOW%Available commands:%RESET%
echo   setup.bat run      %GREEN%→ Run the app%RESET%
echo   setup.bat install  %GREEN%→ Install dependencies%RESET%
echo   setup.bat dev      %GREEN%→ Run in dev mode%RESET%
echo   setup.bat clean    %GREEN%→ Clean environment%RESET%
echo.
echo %YELLOW%Optional parameters:%RESET%
echo   setup.bat run 8502    %GREEN%→ Run on port 8502%RESET%
echo.
goto END

:END
endlocal
