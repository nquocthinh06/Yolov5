# 🚦 Hướng dẫn Training YOLOv5 cho Biển báo Giao thông Việt Nam

## 📋 **Bước 1: Chuẩn bị Dataset**

### **1.1 Cấu trúc thư mục đã tạo:**

```
datasets/traffic_signs_vietnam/
├── images/
│   ├── train/     # Ảnh training (80%)
│   ├── val/       # Ảnh validation (15%)
│   └── test/      # Ảnh test (5%)
└── labels/
    ├── train/     # Labels training
    ├── val/       # Labels validation
    └── test/      # Labels test
```

### **1.2 Copy ảnh vào thư mục:**

```bash
# Copy ảnh từ my_images vào thư mục train
copy my_images\*.jpg datasets\traffic_signs_vietnam\images\train\
```

## 📝 **Bước 2: Annotation (Gắn nhãn)**

### **2.1 Cài đặt LabelImg:**

```bash
pip install labelimg
```

### **2.2 Sử dụng LabelImg:**

1. Mở LabelImg: `labelimg`
2. Chọn thư mục: `datasets/traffic_signs_vietnam/images/train`
3. Chọn format: **YOLO** (không phải PascalVOC)
4. Bắt đầu gắn nhãn từng ảnh

### **2.3 Các class cần gắn nhãn:**

```
0: cam_di_nguoc_chieu      # Cấm đi ngược chiều
1: cam_dung_do             # Cấm dừng đỗ
2: cam_re_trai             # Cấm rẽ trái
3: cam_re_phai             # Cấm rẽ phải
4: cam_vuot                # Cấm vượt
5: gioi_han_toc_do         # Giới hạn tốc độ
6: bien_bao_nguy_hiem      # Biển báo nguy hiểm
7: bien_bao_chi_dan        # Biển báo chỉ dẫn
8: den_giao_thong          # Đèn giao thông
9: bien_bao_phu            # Biển báo phụ
10: cam_quay_dau           # Cấm quay đầu
11: cam_vao                # Cấm vào
12: duong_cam              # Đường cấm
13: bien_bao_ket_thuc      # Biển báo kết thúc
14: bien_bao_tam_thoi      # Biển báo tạm thời
```

### **2.4 Format file label (.txt):**

```
class_id center_x center_y width height
```

Ví dụ: `0 0.5 0.5 0.2 0.3`

## 🚀 **Bước 3: Training**

### **3.1 Training cơ bản:**

```bash
python train.py --data data/traffic_signs_vietnam.yaml --weights yolov5s.pt --img 640 --epochs 100 --batch-size 16
```

### **3.2 Training với model lớn hơn (chính xác hơn):**

```bash
python train.py --data data/traffic_signs_vietnam.yaml --weights yolov5x.pt --img 640 --epochs 200 --batch-size 8
```

### **3.3 Training với GPU:**

```bash
python train.py --data data/traffic_signs_vietnam.yaml --weights yolov5s.pt --img 640 --epochs 100 --batch-size 16 --device 0
```

## 📊 **Bước 4: Kiểm tra kết quả**

### **4.1 Xem kết quả training:**

- Kết quả lưu trong: `runs/train/exp/`
- Xem biểu đồ: `runs/train/exp/results.png`
- Model tốt nhất: `runs/train/exp/weights/best.pt`

### **4.2 Test model:**

```bash
python detect.py --weights runs/train/exp/weights/best.pt --source my_images/ --conf 0.5
```

## ⚙️ **Bước 5: Tối ưu hóa**

### **5.1 Tăng độ chính xác:**

- Tăng số epochs: `--epochs 300`
- Sử dụng model lớn: `--weights yolov5x.pt`
- Tăng image size: `--img 1280`

### **5.2 Tăng tốc độ:**

- Sử dụng model nhỏ: `--weights yolov5n.pt`
- Giảm image size: `--img 320`
- Tăng batch size: `--batch-size 32`

## 🎯 **Lưu ý quan trọng:**

1. **Chia dataset đúng tỷ lệ**: 80% train, 15% val, 5% test
2. **Gắn nhãn chính xác**: Mỗi biển báo phải được gắn nhãn đúng class
3. **Đa dạng ảnh**: Cần ảnh ở nhiều góc độ, ánh sáng khác nhau
4. **Số lượng ảnh**: Ít nhất 100 ảnh mỗi class để có kết quả tốt
5. **Kiểm tra kỹ**: Sau khi training, test trên ảnh mới để đánh giá

## 🔧 **Troubleshooting:**

### **Lỗi thường gặp:**

- **CUDA out of memory**: Giảm batch-size
- **Low mAP**: Tăng số epochs, kiểm tra labels
- **Overfitting**: Thêm data augmentation, giảm epochs

### **Cải thiện kết quả:**

- Sử dụng data augmentation
- Fine-tuning với learning rate thấp
- Ensemble nhiều model
