# PowerShell script to run Docker training
# Usage: .\docker-run.ps1 [-Epochs 100] [-GPU] [-DataFile "data/traffic_signs_vietnam.yaml"]

param(
    [int]$Epochs = 100,
    [string]$DataFile = "data/traffic_signs_vietnam.yaml",
    [switch]$GPU = $false,
    [switch]$SkipBuild = $false
)

$ImageName = if ($GPU) { "thinh/traffic-gpu" } else { "thinh/traffic-cpu" }
$PythonCmd = if ($GPU) { "python3" } else { "python" }
$GpuFlag = if ($GPU) { "--gpus all" } else { "" }
$Dockerfile = if ($GPU) { "Dockerfile.gpu" } else { "Dockerfile" }

Write-Host "Docker Training Script" -ForegroundColor Green
Write-Host "   Image: $ImageName" -ForegroundColor Cyan
Write-Host "   Data: $DataFile" -ForegroundColor Cyan
Write-Host "   Epochs: $Epochs" -ForegroundColor Cyan
Write-Host ""

# Check if image exists
$imageCheck = docker images --format "{{.Repository}}:{{.Tag}}" | Select-String -Pattern "^$ImageName"
$imageExists = $null -ne $imageCheck

if (-not $imageExists -and -not $SkipBuild) {
    Write-Host "Image not found. Building..." -ForegroundColor Yellow
    Write-Host "   Dockerfile: $Dockerfile" -ForegroundColor Cyan
    Write-Host ""
    
    if ($GPU) {
        & docker build -f $Dockerfile -t $ImageName .
    } else {
        & docker build -t $ImageName .
    }
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Build failed!" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Build successful!" -ForegroundColor Green
    Write-Host ""
} elseif ($imageExists) {
    Write-Host "Image exists: $ImageName" -ForegroundColor Green
    Write-Host ""
}

# Build command
$dockerCmd = "docker run --rm -it"
if ($GpuFlag) {
    $dockerCmd += " $GpuFlag"
}
$dockerCmd += " -v `"${PWD}/datasets:/app/datasets`""
$dockerCmd += " -v `"${PWD}/runs:/app/runs`""
$dockerCmd += " -v `"${PWD}/data:/app/data`""
$dockerCmd += " $ImageName $PythonCmd train_traffic_signs.py"
$dockerCmd += " --data $DataFile --epochs $Epochs"

Write-Host "Starting training..." -ForegroundColor Yellow
Write-Host ""

# Execute
Invoke-Expression $dockerCmd

