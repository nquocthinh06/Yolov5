# Simple script to build and run Docker
# Usage: .\build-and-run.ps1

Write-Host "Step 1: Building Docker image..." -ForegroundColor Yellow
docker build -t thinh/traffic-cpu .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed! Check errors above." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 2: Running training..." -ForegroundColor Yellow
Write-Host ""

docker run --rm -it `
  -v "${PWD}/datasets:/app/datasets" `
  -v "${PWD}/runs:/app/runs" `
  -v "${PWD}/data:/app/data" `
  thinh/traffic-cpu python train_traffic_signs.py `
    --data data/traffic_signs_vietnam.yaml `
    --epochs 100

