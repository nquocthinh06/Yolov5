# 🚗 YOLOv5 Traffic Detection - Hướng dẫn sử dụng

## 🎯 **Tổng quan**
Ứng dụng phát hiện phương tiện giao thông và con người sử dụng YOLOv5 với độ chính xác cao nhất.

---

## 🚀 **Cài đặt và chạy**

### **1. Cài đặt dependencies:**
```bash
pip install torch torchvision ultralytics opencv-python pillow
```

### **2. Chạy ứng dụng:**
```bash
python traffic_detection_gui.py
```

---

## 📱 **Giao diện chính**

### **🖼️ Khu vực hiển thị:**
- **Ảnh gốc** (trái): Upload ảnh cần phân tích
- **Kết quả** (phải): Ảnh đã được phát hiện đối tượng

### **⚙️ Cài đặt:**
- **Độ tin cậy**: 30-95% (khuyến nghị: 60%)
- **IoU**: 30-70% (khuyến nghị: 45%)
- **Model**: Chọn từ YOLOv5n đến YOLOv5x (khuyến nghị: YOLOv5x)

### **📊 Kết quả phân tích:**
- **Tab 1**: 🚗 Phân tích giao thông
- **Tab 2**: 🚙 Chi tiết phương tiện  
- **Tab 3**: 👥 Phân tích con người

---

## 🎯 **Các chức năng chính**

### **📂 Chọn ảnh:**
1. Click "📂 Chọn ảnh"
2. Chọn file ảnh (.jpg, .png, .bmp, etc.)
3. Ảnh sẽ hiển thị ở panel trái

### **🎬 Chọn video:**
1. Click "🎬 Chọn video"
2. Chọn file video (.mp4, .avi, .mov, etc.)
3. Cửa sổ xử lý video sẽ mở ra

### **📹 Xử lý video:**
1. Điều chỉnh độ tin cậy và IoU nếu cần
2. Click "▶️ Bắt đầu" để bắt đầu xử lý
3. Sử dụng "⏸️ Tạm dừng" để tạm dừng
4. Sử dụng "⏹️ Dừng" để dừng hoàn toàn
5. Xem kết quả real-time trong 2 tab:
   - **🎞️ Kết quả từng frame**: Chi tiết mỗi frame
   - **📈 Thống kê tổng hợp**: Phân tích tổng quan

### **💾 Lưu video nâng cao:**
- **📊 Lưu báo cáo**: Lưu kết quả phân tích chi tiết (.txt)
- **🎬 Xuất video đã xử lý**: Lưu video với khoanh vùng nâng cao (.mp4)
  - Tự động tạo thư mục `video_results/`
  - Tên file với timestamp: `video_processed_20241004_143022.mp4`
  - Khoanh vùng màu sắc theo loại đối tượng:
    - 🟢 **Xanh lá**: Con người
    - 🔴 **Đỏ**: Xe hơi  
    - 🟠 **Cam**: Xe tải
    - 🟡 **Vàng**: Xe buýt
    - 🟣 **Tím**: Xe máy
    - 🔵 **Cyan**: Xe đạp
  - ID đánh số từng đối tượng (#1, #2, #3...)
  - Độ tin cậy hiển thị rõ ràng (%)
  - Điểm trung tâm đối tượng
  - Thông tin tổng quan và timestamp

### **📊 Báo cáo video chi tiết:**
Mỗi video xuất sẽ có báo cáo đi kèm bao gồm:
- 📹 **Thông tin video**: Resolution, FPS, thời lượng
- ⚙️ **Cấu hình model**: Model sử dụng, confidence, IoU
- 📊 **Thống kê phát hiện**: Số người, phương tiện, frame có đối tượng
- 🎯 **Phân tích mật độ**: Mật độ trung bình, đánh giá giao thông
- 💡 **Khuyến nghị**: Dựa trên phân tích tự động

### **💾 Lưu kết quả:**
- **Lưu ảnh**: Lưu ảnh đã phát hiện
- **Xuất dữ liệu**: Lưu báo cáo phân tích (.txt)

---

## 📊 **Hiểu kết quả**

### **🎯 Độ tin cậy:**
- **🟢 80-100%**: Rất chính xác
- **🟡 60-80%**: Chính xác tốt
- **🟠 40-60%**: Cần xem xét
- **🔴 <40%**: Không tin cậy

### **📋 Thông tin hiển thị:**
- **Loại đối tượng**: person, car, motorcycle, bus, truck, etc.
- **Độ tin cậy**: Phần trăm chính xác
- **Vị trí**: Tọa độ trên ảnh
- **Kích thước**: Pixel width x height

---

## 🚗 **Đối tượng được phát hiện**

### **👥 Con người:**
- Người đi bộ
- Người lái xe
- Phân tích kích thước và vị trí

### **🚗 Phương tiện:**
- **Xe cá nhân**: car, motorcycle, bicycle
- **Xe công cộng**: bus, train
- **Xe tải**: truck
- **Khác**: airplane, boat

### **🚦 Biển báo:**
- Đèn giao thông
- Biển báo dừng
- Đồng hồ đỗ xe

---

## ⚙️ **Tối ưu hóa**

### **🎯 Để có kết quả tốt nhất:**
1. **Sử dụng YOLOv5x** (chính xác nhất)
2. **Độ tin cậy 60-70%** (cân bằng)
3. **Ảnh rõ nét**, độ phân giải cao
4. **Ánh sáng tốt**, không bị mờ

### **🚀 Tăng tốc độ:**
1. **Sử dụng YOLOv5s** (nhanh hơn)
2. **Giảm độ tin cậy** xuống 40-50%
3. **Ảnh nhỏ hơn** (<1MB)

### **🎯 Tăng độ chính xác:**
1. **Tăng độ tin cậy** lên 70-80%
2. **IoU thấp hơn** (30-40%)
3. **Ảnh chất lượng cao**

---

## 🔧 **Xử lý sự cố**

### **❌ Không phát hiện được:**
- Giảm độ tin cậy xuống 30-40%
- Kiểm tra ảnh có rõ nét không
- Thử model khác (YOLOv5s, YOLOv5m)

### **❌ Phát hiện sai (false positive):**
- Tăng độ tin cậy lên 70-80%
- Tăng IoU lên 50-60%
- Sử dụng YOLOv5x cho độ chính xác cao

### **❌ Chạy chậm:**
- Sử dụng YOLOv5n hoặc YOLOv5s
- Giảm kích thước ảnh
- Đóng các ứng dụng khác

---

## 📞 **Hỗ trợ**

### **🔍 Các file quan trọng:**
- `traffic_detection_gui.py`: Ứng dụng chính ⭐
- `fullscreen_results_gui.py`: Phiên bản fullscreen
- `improved_yolo_gui.py`: Phiên bản cải tiến
- `simple_yolo_gui.py`: Phiên bản đơn giản

### **📊 Model files:**
- `yolov5x.pt`: Model chính xác nhất (khuyến nghị)
- `yolov5s.pt`: Model cân bằng
- `yolov5su.pt`: Phiên bản cải tiến

### **📋 Documentation:**
- `MODEL_OPTIMIZATION.md`: Tối ưu hóa model
- `yolo_classes_summary.md`: Danh sách đối tượng
- `confidence_explanation.md`: Giải thích độ tin cậy

---

## 🎉 **Kết luận**

Ứng dụng YOLOv5 Traffic Detection cung cấp:
- ✅ **Độ chính xác cao** với YOLOv5x (50.7% mAP)
- ✅ **Giao diện thân thiện** và dễ sử dụng
- ✅ **Phân tích chi tiết** phương tiện và con người
- ✅ **Tối ưu cho giao thông** Việt Nam
- ✅ **Xuất báo cáo** và lưu kết quả

**Chúc bạn sử dụng hiệu quả!** 🚀

---

## 🎬 **Test với Video Demo**

### **Video demo cơ bản:**
```bash
# Tạo video demo 5 giây (640x480)
python create_demo_video.py
# Kết quả: demo_traffic_video.mp4 (0.33 MB)
```

### **Video demo nâng cao:**
```bash
# Tạo video demo 10 giây HD (1280x720)
python create_advanced_demo.py
# Kết quả: advanced_traffic_demo.mp4 (2.58 MB)
```

**Video demo nâng cao bao gồm:**
- 🚗 **Nhiều loại xe**: car, truck, bus, motorcycle
- 👥 **Người đi bộ**: Di chuyển tự nhiên, nhóm người
- 🚦 **Đèn giao thông**: Nhấp nháy xanh/đỏ
- 🛑 **Biển báo**: Stop sign
- 🏙️ **Background**: Đường phố, cây cối, tòa nhà
- ⏱️ **Timestamp**: Thông tin thời gian thực

### **Cách test:**
```bash
# 1. Tạo video demo
python create_advanced_demo.py

# 2. Chạy ứng dụng
python traffic_detection_gui.py

# 3. Chọn video: advanced_traffic_demo.mp4
# 4. Xử lý và xuất kết quả với khoanh vùng nâng cao
```

### **Kết quả mong đợi:**
- ✅ Video được lưu trong thư mục `video_results/`
- ✅ Báo cáo chi tiết `.txt` đi kèm
- ✅ Khoanh vùng màu sắc theo loại đối tượng
- ✅ Thống kê đầy đủ và khuyến nghị an toàn
