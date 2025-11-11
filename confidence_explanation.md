# 📊 Giải thích Độ Tin Cậy theo Phần Trăm (%)

## 🎯 **Ví dụ về độ tin cậy 31% (0.31)**

| **Độ tin cậy** | **Ý nghĩa** | **Mức độ** | **Khuyến nghị** |
|----------------|-------------|------------|-----------------|
| **31%** | Mô hình chỉ 31% tự tin | 🔴 Thấp | ⚠️ Cần kiểm tra kỹ |
| **50%** | Mô hình 50% tự tin | 🟠 Trung bình | ✅ Có thể chấp nhận |
| **70%** | Mô hình 70% tự tin | 🟡 Cao | ✅ Tin cậy tốt |
| **90%** | Mô hình 90% tự tin | 🟢 Rất cao | ✅ Tin cậy tuyệt đối |

## 📈 **Thang đo chi tiết:**

### 🟢 **80-100%**: Rất cao
- **Ý nghĩa**: Mô hình rất tự tin
- **Khuyến nghị**: Tin tưởng hoàn toàn
- **Ví dụ**: Người, xe hơi rõ ràng

### 🟡 **60-80%**: Cao  
- **Ý nghĩa**: Mô hình tự tin
- **Khuyến nghị**: Tin tưởng tốt
- **Ví dụ**: Đối tượng hơi mờ nhưng vẫn nhận ra

### 🟠 **40-60%**: Trung bình
- **Ý nghĩa**: Mô hình không chắc chắn
- **Khuyến nghị**: Cần xem xét kỹ
- **Ví dụ**: Đối tượng bị che khuất một phần

### 🔴 **20-40%**: Thấp
- **Ý nghĩa**: Mô hình không tự tin
- **Khuyến nghị**: Có thể sai
- **Ví dụ**: Đối tượng nhỏ, mờ, góc chụp xấu

### ⚫ **0-20%**: Rất thấp
- **Ý nghĩa**: Mô hình rất không chắc chắn
- **Khuyến nghị**: Có thể bỏ qua
- **Ví dụ**: Nhiễu, false positive

## 🔧 **Cách điều chỉnh:**

```bash
# Hiển thị tất cả (kể cả độ tin cậy thấp)
py -3.12 simple_detect.py image.jpg

# Chỉ hiển thị độ tin cậy cao (70% trở lên)
py -3.12 adjust_confidence.py image.jpg 0.7

# Hiển thị chi tiết với phần trăm
py -3.12 confidence_percent_demo.py image.jpg
```

## 💡 **Lời khuyên:**

- **31%**: Có thể là **phát hiện sai** - nên kiểm tra thủ công
- **Tăng ngưỡng lên 50-70%** để giảm false positive
- **Giảm ngưỡng xuống 20-30%** nếu muốn phát hiện nhiều hơn
- **Luôn kiểm tra kết quả** với độ tin cậy dưới 50%
