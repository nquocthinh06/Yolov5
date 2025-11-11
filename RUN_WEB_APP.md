# 🚀 Hướng Dẫn Chạy Ứng Dụng Web

## 📋 Yêu Cầu

- Python 3.8 trở lên
- pip (Python package manager)
- Terminal/PowerShell

## 🔧 Cài Đặt

### Bước 1: Cài Đặt Dependencies

Chạy lệnh sau trong Terminal/PowerShell:

```bash
pip install streamlit plotly pillow pandas torch torchvision opencv-python
```

### Bước 2: Xác Nhận Cài Đặt

Kiểm tra Streamlit đã cài đặt thành công:

```bash
streamlit --version
```

Kết quả sẽ hiển thị phiên bản, ví dụ: `Streamlit, version 1.28.1`

## ▶️ Chạy Ứng Dụng

### Cách 1: Chạy Trực Tiếp

```bash
streamlit run app_web.py
```

### Cách 2: Chạy Tại Cổng Cụ Thể (Nếu 8501 Bị Chiếm)

```bash
streamlit run app_web.py --server.port 8502
```

### Cách 3: Chạy Ở Host Khác

```bash
streamlit run app_web.py --server.address 0.0.0.0
```

## 🌐 Truy Cập Ứng Dụng

Sau khi chạy, ứng dụng sẽ tự động mở trong trình duyệt:

```
http://localhost:8501
```

Nếu không tự động mở, truy cập URL trên bằng tay.

## 🎯 Các Module Chính

### 1️⃣ Detect & Surveillance (🎯)
- **Chức năng:** Phát hiện biển báo giao thông real-time
- **Cách sử dụng:**
  1. Chọn nguồn: Tải ảnh, video, hoặc dùng webcam
  2. Điều chỉnh confidence threshold (0-1)
  3. Điều chỉnh IoU threshold (0-1)
  4. Click "🚀 Run Detection"
  5. Xem kết quả và thống kê

### 2️⃣ Train Model (🎓)
- **Chức năng:** Huấn luyện mô hình YOLOv5
- **Cách sử dụng:**
  1. Tải file YAML của dataset
  2. Cài đặt hyperparameters:
     - Epochs: số lần training (default: 100)
     - Batch Size: kích thước batch (default: 16)
     - Image Size: kích thước ảnh (default: 640)
  3. Chọn Optimizer (SGD/Adam/AdamW)
  4. Click "▶️ Start Training"
  5. Theo dõi logs và charts

### 3️⃣ Validate System (✅)
- **Chức năng:** So sánh hiệu suất các thuật toán AID
- **Cách sử dụng:**
  1. Điều chỉnh DR, FAR, MTTD weights
  2. Xem bảng so sánh thuật toán
  3. Kiểm tra validation metrics

### 4️⃣ Export Model (📦)
- **Chức năng:** Export mô hình sang nhiều format
- **Cách sử dụng:**
  1. Tải file .pt weights
  2. Chọn device (CPU/GPU)
  3. Chọn format export (ONNX/TensorRT/CoreML/TFLite)
  4. Click "🚀 Export Model"
  5. Download models đã export

## 🎨 Giao Diện

### Màu Sắc
- **Nền:** Xanh đen (#0f172a)
- **Card:** Xanh tối (#1e293b)
- **Accent:** Xanh dương (#3b82f6)
- **Text:** Trắng (#ffffff)

### Layout
```
┌──────────────────────────────────────┐
│  🚦 YOLOv5 Traffic Detection        │
├────────────┬──────────────────────────┤
│            │                          │
│  SIDEBAR   │   MAIN CONTENT           │
│            │   (Tab Content)          │
│  • Tabs    │   • Input Controls       │
│  • Status  │   • Preview/Results      │
│  • Settings│   • Charts/Tables        │
│            │   • Buttons              │
└────────────┴──────────────────────────┘
```

## ⌨️ Phím Tắt

| Phím | Chức Năng |
|------|----------|
| `Ctrl+C` | Dừng ứng dụng |
| `R` | Refresh trang |
| `S` | Save kết quả |

## 🐛 Troubleshooting

### ❌ Lỗi: "Port 8501 already in use"

**Giải pháp:**
```bash
streamlit run app_web.py --server.port 8502
```

### ❌ Lỗi: "ModuleNotFoundError: No module named 'streamlit'"

**Giải pháp:**
```bash
pip install streamlit
```

### ❌ Lỗi: "torch not found"

**Giải pháp:**
```bash
pip install torch torchvision
```

### ❌ Ứng dụng chạy chậm

**Giải pháp:**
1. Giảm kích thước ảnh
2. Dùng batch size nhỏ hơn
3. Đóng các ứng dụng khác
4. Bật GPU nếu có (trong Settings)

### ❌ File upload không hoạt động

**Kiểm tra:**
1. File có định dạng đúng không? (JPG, PNG, MP4, AVI)
2. File không bị hỏng
3. File size < 200MB

## 📊 Tệp Cấu Hình

### Cần chuẩn bị trước
```
data/traffic_signs_vietnam.yaml    # Dataset config
datasets/traffic_signs_vietnam/    # Training data folder
```

### Sẽ tự tạo
```
results/models/                    # Saved models
results/predictions/               # Detection results
```

## 🔧 Cài Đặt Nâng Cao

### Thay đổi cỡ font

Mở `app_web.py`, tìm dòng:
```python
font-size: 16px !important;
```

Thay đổi `16` sang số khác (ví dụ: `18`, `20`)

### Thay đổi màu sắc

Tìm các dòng:
```python
--primary: #3b82f6;
--bg-dark: #0f172a;
```

Thay đổi giá trị hex color

### Thay đổi cổng mặc định

Chỉnh sửa khi chạy:
```bash
streamlit run app_web.py --server.port YOUR_PORT
```

## 💾 Lưu Kết Quả

Tất cả kết quả sẽ được lưu tại:
```
results/
├── models/          # Các mô hình đã train/export
├── predictions/     # Kết quả detection
└── metrics/         # Các chỉ số đánh giá
```

## 📚 Tài Liệu Liên Quan

- [Streamlit Docs](https://docs.streamlit.io/)
- [YOLOv5 Documentation](https://docs.ultralytics.com/yolov5/)
- [COMPLETE_PROJECT_DOCUMENTATION.md](docs/COMPLETE_PROJECT_DOCUMENTATION.md)
- [WEB_INTERFACE_GUIDE.md](WEB_INTERFACE_GUIDE.md)

## 🚀 Tôi Đã Sẵn Sàng!

```bash
streamlit run app_web.py
```

Gõ lệnh trên và khám phá ứng dụng! 🎉

---

## 📝 Ghi Chú

- Lần đầu chạy có thể mất chút thời gian để tải dependencies
- Ứng dụng sẽ lưu cache trên máy cục bộ
- Có thể sử dụng trên cùng một máy với detect.py
- Web interface không yêu cầu kết nối internet (chạy local)

## 🆘 Cần Hỗ Trợ?

1. Kiểm tra lại requirements
2. Xóa cache: `streamlit cache clear`
3. Khởi động lại terminal
4. Cập nhật Streamlit: `pip install --upgrade streamlit`

---

**Version:** 1.0.0  
**Last Updated:** 2025-01-11  
**Status:** ✅ Ready to Use

Happy Detecting! 🚦

