# 📁 Video Results - Kết quả Video

Thư mục này chứa các video đã được xử lý bởi YOLOv5.

## 📋 Cấu trúc file:

- `video_processed_YYYYMMDD_HHMMSS.mp4` - Video đã xử lý với khoanh vùng
- `video_processed_YYYYMMDD_HHMMSS_report.txt` - Báo cáo đi kèm

## 🎯 Đặc điểm video đã xử lý:

- ✅ Khoanh vùng màu sắc theo loại đối tượng
- ✅ ID đánh số từng đối tượng (#1, #2, #3...)
- ✅ Độ tin cậy hiển thị rõ ràng (%)
- ✅ Điểm trung tâm đối tượng
- ✅ Thông tin tổng quan và timestamp

## 🎨 Màu sắc khoanh vùng:

- 🟢 Xanh lá: Con người (person)
- 🔴 Đỏ: Xe hơi (car)
- 🟠 Cam: Xe tải (truck)
- 🟡 Vàng: Xe buýt (bus)
- 🟣 Tím: Xe máy (motorcycle)
- 🔵 Cyan: Xe đạp (bicycle)

Được tạo bởi YOLOv5 Traffic Detection GUI
