# Script setup Git và kiểm tra cấu hình
# Usage: .\setup-git.ps1

# Refresh PATH để đảm bảo Git có thể được tìm thấy
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Kiểm tra cấu hình Git                " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Kiểm tra Git
Write-Host "Kiểm tra Git..." -ForegroundColor Yellow
try {
    $gitVersion = git --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Git: $gitVersion" -ForegroundColor Green
    } else {
        throw "Git not found"
    }
} catch {
    Write-Host "✗ Git chưa được cài đặt!" -ForegroundColor Red
    Write-Host "Đang cài đặt Git..." -ForegroundColor Yellow
    winget install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements
    Write-Host "Vui lòng đóng và mở lại PowerShell sau khi cài đặt xong!" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Kiểm tra cấu hình user
Write-Host "Kiểm tra cấu hình Git user..." -ForegroundColor Yellow
$userName = git config --global user.name
$userEmail = git config --global user.email

if ([string]::IsNullOrEmpty($userName)) {
    Write-Host "⚠ Git user.name chưa được cấu hình" -ForegroundColor Yellow
    $newName = Read-Host "Nhập tên của bạn"
    if (-not [string]::IsNullOrEmpty($newName)) {
        git config --global user.name $newName
        Write-Host "✓ Đã cấu hình user.name: $newName" -ForegroundColor Green
    }
} else {
    Write-Host "✓ User name: $userName" -ForegroundColor Green
}

if ([string]::IsNullOrEmpty($userEmail)) {
    Write-Host "⚠ Git user.email chưa được cấu hình" -ForegroundColor Yellow
    $newEmail = Read-Host "Nhập email của bạn"
    if (-not [string]::IsNullOrEmpty($newEmail)) {
        git config --global user.email $newEmail
        Write-Host "✓ Đã cấu hình user.email: $newEmail" -ForegroundColor Green
    }
} else {
    Write-Host "✓ User email: $userEmail" -ForegroundColor Green
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "  Cấu hình Git hoàn tất!               " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Bạn có thể tiếp tục với:" -ForegroundColor Yellow
Write-Host "  .\push-to-github.ps1" -ForegroundColor Cyan
Write-Host ""

