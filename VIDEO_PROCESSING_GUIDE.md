# 🎬 Hướng dẫn xử lý Video - YOLOv5

## 🚀 Các bước xử lý video:

### **1. Mở video:**
- Click "🎬 Chọn video" trong ứng dụng chính
- Chọn file video (.mp4, .avi, .mov, etc.)
- Cửa sổ xử lý video sẽ mở ra

### **2. Các nút luôn hiển thị:**
Sau khi mở video, bạn sẽ thấy 4 nút quan trọng:

#### 🔧 **Thao tác sau xử lý:**
- **📋 Tạo báo cáo ngay**: Tạo báo cáo từ dữ liệu hiện có (có thể dùng ngay)
- **📊 Lưu báo cáo chi tiết**: Lưu báo cáo đầy đủ từ kết quả xử lý
- **🎬 Xuất video đã xử lý**: Xuất video với khoanh vùng màu sắc
- **📁 Mở thư mục kết quả**: Mở thư mục chứa các file đã tạo

### **3. Xử lý video:**
- Điều chỉnh độ tin cậy (Confidence) và IoU nếu cần
- Click "▶️ Bắt đầu" để bắt đầu xử lý
- Theo dõi tiến trình và kết quả real-time

### **4. Sau khi xử lý xong:**
- Thông báo hoàn thành sẽ xuất hiện
- Sử dụng các nút đã có để lưu kết quả

---

## 📁 **Cấu trúc thư mục kết quả:**

```
yolov5-master/
├── video_results/          # Video đã xử lý
│   ├── video_processed_20241004_143022.mp4
│   └── video_processed_20241004_143022_report.txt
│
├── video_reports/          # Báo cáo phân tích
│   ├── video_analysis_report_20241004_143022.txt
│   └── video_analysis_report_20241004_144530.txt
│
└── traffic_detection_gui.py  # Ứng dụng chính
```

---

## 🎯 **Chi tiết từng chức năng:**

### **📋 Tạo báo cáo ngay:**
- ✅ Hoạt động ngay lập tức
- ✅ Không cần chờ xử lý hoàn tất
- ✅ Tạo file `.txt` trong thư mục `video_reports/`
- ✅ Bao gồm: thống kê hiện tại, cấu hình model, kết quả từng frame

### **📊 Lưu báo cáo chi tiết:**
- ✅ Lưu toàn bộ dữ liệu từ 2 tab
- ✅ Cho phép chọn định dạng (.txt, .csv)
- ✅ Bao gồm: kết quả chi tiết, thống kê tổng hợp

### **🎬 Xuất video đã xử lý:**
- ✅ Tạo video với khoanh vùng màu sắc
- ✅ Tự động tạo thư mục `video_results/`
- ✅ Tên file với timestamp
- ✅ Báo cáo đi kèm
- ✅ Khoanh vùng nâng cao:
  - 🟢 Xanh lá: Con người
  - 🔴 Đỏ: Xe hơi
  - 🟠 Cam: Xe tải
  - 🟡 Vàng: Xe buýt
  - 🟣 Tím: Xe máy
  - 🔵 Cyan: Xe đạp

### **📁 Mở thư mục kết quả:**
- ✅ Tự động tạo thư mục nếu chưa có
- ✅ Mở Windows Explorer
- ✅ Hiển thị thông tin các thư mục

---

## 🔧 **Xử lý sự cố:**

### **❓ Không thấy các nút:**
- Đảm bảo đã mở video (click "🎬 Chọn video")
- Các nút sẽ hiển thị ngay sau khi cửa sổ video mở

### **❓ Không tạo được báo cáo:**
- Thử click "📋 Tạo báo cáo ngay" (hoạt động ngay lập tức)
- Kiểm tra quyền ghi file trong thư mục

### **❓ Video không xuất được:**
- Đảm bảo đã xử lý video (click "▶️ Bắt đầu" trước)
- Kiểm tra dung lượng ổ đĩa

### **❓ Không mở được thư mục:**
- Click "📁 Mở thư mục kết quả" để tự động tạo thư mục
- Thư mục sẽ được tạo trong cùng folder với ứng dụng

---

## 💡 **Tips sử dụng:**

1. **Tạo báo cáo ngay**: Sử dụng ngay cả khi chưa xử lý xong
2. **Theo dõi tiến trình**: Xem tab "Kết quả từng frame" để theo dõi
3. **Điều chỉnh tham số**: Thay đổi confidence/IoU trước khi xử lý
4. **Backup kết quả**: Các file được lưu với timestamp, không bị ghi đè
5. **Kiểm tra thư mục**: Sử dụng "📁 Mở thư mục kết quả" để xem các file đã tạo

**Chúc bạn sử dụng thành công!** 🚀
