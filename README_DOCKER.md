# 🐳 Docker Quick Start Guide

## ✅ Bước 1: Build Image (CPU) - BẮT BUỘC TRƯỚC KHI CHẠY

```powershell
# Di chuyển vào thư mục dự án
cd "C:\Users\Thinh Nguyen\Downloads\yolov5-master\yolov5-master"

# Build image (mất vài phút lần đầu)
docker build -t thinh/traffic-cpu .
```

**Lưu ý:** Bạn PHẢI build image trước khi chạy. Nếu không sẽ gặp lỗi "Unable to find image".

## 🚀 Bước 2: Chạy Training

**Cách 1: Lệnh đơn giản (1 dòng)**

```powershell
docker run --rm -it -v "${PWD}/datasets:/app/datasets" -v "${PWD}/runs:/app/runs" -v "${PWD}/data:/app/data" thinh/traffic-cpu python train_traffic_signs.py --data data/traffic_signs_vietnam.yaml --epochs 100
```

**Cách 2: Lệnh nhiều dòng (dễ đọc hơn)**

Trong PowerShell, dùng backtick `` ` `` (không phải `^`):

```powershell
docker run --rm -it `
  -v "${PWD}/datasets:/app/datasets" `
  -v "${PWD}/runs:/app/runs" `
  -v "${PWD}/data:/app/data" `
  thinh/traffic-cpu python train_traffic_signs.py `
    --data data/traffic_signs_vietnam.yaml `
    --epochs 100
```

**Lưu ý:** 
- Dùng backtick `` ` `` (phím bên trái số 1) để xuống dòng trong PowerShell
- Kết quả sẽ lưu trong thư mục `runs/` trên máy bạn

## 📦 Bước 3: Dùng Docker Compose (Khuyên dùng)

```powershell
docker compose up --build
```

Hoặc chạy ở background:

```powershell
docker compose up -d --build
```

Xem logs:

```powershell
docker compose logs -f
```

## 🎮 GPU Mode (Tùy chọn)

**Build GPU image:**

```powershell
docker build -f Dockerfile.gpu -t thinh/traffic-gpu .
```

**Chạy với GPU:**

```powershell
docker run --rm -it --gpus all -v "${PWD}/datasets:/app/datasets" -v "${PWD}/runs:/app/runs" -v "${PWD}/data:/app/data" thinh/traffic-gpu python3 train_traffic_signs.py --data data/traffic_signs_vietnam.yaml --epochs 100
```

Hoặc nhiều dòng:

```powershell
docker run --rm -it --gpus all `
  -v "${PWD}/datasets:/app/datasets" `
  -v "${PWD}/runs:/app/runs" `
  -v "${PWD}/data:/app/data" `
  thinh/traffic-gpu python3 train_traffic_signs.py `
    --data data/traffic_signs_vietnam.yaml `
    --epochs 100
```

## 🔍 Kiểm tra Image đã build

```powershell
docker images | findstr thinh
```

## 🗑️ Xóa container/image (nếu cần)

```powershell
# Xóa container đã dừng
docker container prune

# Xóa image
docker rmi thinh/traffic-cpu
```

## ⚠️ Xử lý lỗi thường gặp

**Lỗi "invalid reference format":**
- Đảm bảo dùng backtick `` ` `` thay vì `^` trong PowerShell
- Hoặc viết lệnh trên 1 dòng

**Lỗi "path not found":**
- Đảm bảo đang ở đúng thư mục dự án
- Kiểm tra đường dẫn có khoảng trắng phải bọc trong dấu ngoặc kép `"${PWD}/..."`

**Lỗi "permission denied":**
- Chạy PowerShell với quyền Administrator (nếu cần)

