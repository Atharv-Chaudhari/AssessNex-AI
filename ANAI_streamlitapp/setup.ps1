# ============================================================================
# AssessNex AI Streamlit App - Automated Setup Script
# ============================================================================
# Usage: .\setup.ps1
# This script will:
# 1. Create virtual environment
# 2. Activate it
# 3. Install dependencies
# 4. Run the Streamlit app
# ============================================================================

param(
    [string]$Action = "run",  # run, install, clean, dev
    [int]$Port = 8501
)

# Color output
$Green = "`e[32m"
$Blue = "`e[34m"
$Yellow = "`e[33m"
$Red = "`e[31m"
$Reset = "`e[0m"

# Helper functions
function Write-Header {
    param([string]$Text)
    Write-Host "`n$Blue╔════════════════════════════════════════╗$Reset"
    Write-Host "$Blue║ $Text$Reset"
    Write-Host "$Blue╚════════════════════════════════════════╝$Reset`n"
}

function Write-Success {
    param([string]$Text)
    Write-Host "$Green✓ $Text$Reset"
}

function Write-Error-Custom {
    param([string]$Text)
    Write-Host "$Red✗ $Text$Reset"
}

function Write-Info {
    param([string]$Text)
    Write-Host "$Yellow→ $Text$Reset"
}

# Main script starts
Write-Host "`n"
Write-Host "$Blue      ╔═══════════════════════════════════════════╗$Reset"
Write-Host "$Blue      ║     AssessNex AI - Streamlit App         ║$Reset"
Write-Host "$Blue      ║     Setup & Installation Script          ║$Reset"
Write-Host "$Blue      ╚═══════════════════════════════════════════╝$Reset`n"

# Get current directory
$CurrentDir = Get-Location
$VenvPath = Join-Path $CurrentDir "venv"

switch ($Action.ToLower()) {
    "run" {
        Write-Header "🚀 STARTING STREAMLIT APP"
        
        # Check if venv exists
        if (Test-Path $VenvPath) {
            Write-Info "Virtual environment found, activating..."
            & "$VenvPath\Scripts\Activate.ps1"
            Write-Success "Virtual environment activated"
        } else {
            Write-Info "Virtual environment not found, installing..."
            & python -m venv $VenvPath
            & "$VenvPath\Scripts\Activate.ps1"
            Write-Success "Virtual environment created and activated"
            
            # Install requirements
            Write-Info "Installing dependencies..."
            & pip install --upgrade pip
            & pip install -r requirements.txt
            Write-Success "Dependencies installed"
        }
        
        # Run Streamlit
        Write-Header "✨ LAUNCHING STREAMLIT"
        Write-Success "App is starting at http://localhost:$Port"
        Write-Info "Press Ctrl+C to stop the server"
        Write-Host ""
        
        & streamlit run main.py --server.port $Port
    }
    
    "install" {
        Write-Header "📦 INSTALLING DEPENDENCIES"
        
        # Create venv if not exists
        if (!(Test-Path $VenvPath)) {
            Write-Info "Creating virtual environment..."
            & python -m venv $VenvPath
            Write-Success "Virtual environment created"
        }
        
        # Activate venv
        & "$VenvPath\Scripts\Activate.ps1"
        Write-Success "Virtual environment activated"
        
        # Upgrade pip
        Write-Info "Upgrading pip..."
        & python -m pip install --upgrade pip
        Write-Success "Pip upgraded"
        
        # Install requirements
        Write-Info "Installing requirements..."
        & pip install -r requirements.txt
        Write-Success "All dependencies installed"
        
        Write-Header "✅ INSTALLATION COMPLETE"
        Write-Info "To start the app, run: .\setup.ps1 -Action run"
    }
    
    "clean" {
        Write-Header "🧹 CLEANING UP"
        
        # Remove venv
        if (Test-Path $VenvPath) {
            Write-Info "Removing virtual environment..."
            Remove-Item -Recurse -Force $VenvPath
            Write-Success "Virtual environment removed"
        } else {
            Write-Info "No virtual environment found"
        }
        
        # Remove cache directories
        Get-ChildItem -Recurse -Filter "__pycache__" -Directory | 
            ForEach-Object {
                Write-Info "Removing $_"
                Remove-Item -Recurse -Force $_
            }
        
        Write-Success "Cache cleared"
        
        Write-Header "✅ CLEANUP COMPLETE"
    }
    
    "dev" {
        Write-Header "🛠️ DEVELOPMENT MODE"
        
        # Ensure venv is active
        if (!(Test-Path $VenvPath)) {
            Write-Info "Creating virtual environment..."
            & python -m venv $VenvPath
            & "$VenvPath\Scripts\Activate.ps1"
            & pip install --upgrade pip
            & pip install -r requirements.txt
        } else {
            & "$VenvPath\Scripts\Activate.ps1"
        }
        
        # Run with debug logging
        Write-Header "✨ LAUNCHING IN DEV MODE"
        Write-Success "Debug logging enabled"
        Write-Info "Press Ctrl+C to stop"
        Write-Host ""
        
        & streamlit run main.py `
            --server.port $Port `
            --logger.level=debug `
            --client.showErrorDetails=true
    }
    
    default {
        Write-Header "❓ USAGE"
        Write-Host "$Yellow Available commands:$Reset"
        Write-Host "  .\setup.ps1 -Action run      $Green→ Run the app$Reset"
        Write-Host "  .\setup.ps1 -Action install  $Green→ Install dependencies$Reset"
        Write-Host "  .\setup.ps1 -Action dev      $Green→ Run in dev mode$Reset"
        Write-Host "  .\setup.ps1 -Action clean    $Green→ Clean environment$Reset"
        Write-Host "`n$Yellow Optional parameters:$Reset"
        Write-Host "  -Port 8501                   $Green→ Change server port (default: 8501)$Reset"
        Write-Host ""
    }
}

# Deactivate venv on script exit (optional)
# Write-Info "Deactivating virtual environment..."
# & deactivate
