# 🚀 Hướng dẫn nhanh - Chạy Docker Training

## ⚡ Cách nhanh nhất (Dùng script tự động)

```powershell
# Vào thư mục dự án
cd "C:\Users\Thinh Nguyen\Downloads\yolov5-master\yolov5-master"

# Chạy script (tự động build nếu chưa có image)
.\docker-run.ps1 -Epochs 100
```

Script sẽ tự động:
- ✅ Kiểm tra image đã có chưa
- ✅ Build image nếu chưa có
- ✅ Chạy training

---

## 📋 Cách thủ công (Từng bước)

### Bước 1: Vào thư mục dự án
```powershell
cd "C:\Users\Thinh Nguyen\Downloads\yolov5-master\yolov5-master"
```

### Bước 2: Build image (CHẠY LỆNH NÀY TRƯỚC)
```powershell
docker build -t thinh/traffic-cpu .
```

**⏱️ Mất khoảng 5-10 phút lần đầu tiên**

### Bước 3: Chạy training
```powershell
docker run --rm -it -v "${PWD}/datasets:/app/datasets" -v "${PWD}/runs:/app/runs" -v "${PWD}/data:/app/data" thinh/traffic-cpu python train_traffic_signs.py --data data/traffic_signs_vietnam.yaml --epochs 100
```

---

## 🎯 Hoặc dùng Docker Compose (1 lệnh)

```powershell
docker compose up --build
```

---

## ❌ Xử lý lỗi

**Lỗi: "Unable to find image 'thinh/traffic-cpu:latest' locally"**
→ **Giải pháp:** Chạy lệnh build trước:
```powershell
docker build -t thinh/traffic-cpu .
```

**Lỗi: "invalid reference format"**
→ **Giải pháp:** Dùng script `.\docker-run.ps1` hoặc viết lệnh trên 1 dòng

**Lỗi: "path not found"**
→ **Giải pháp:** Đảm bảo đang ở đúng thư mục dự án

---

## ✅ Kiểm tra image đã build

```powershell
docker images | findstr thinh
```

Nếu thấy `thinh/traffic-cpu` trong danh sách → OK, có thể chạy training.

