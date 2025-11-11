# Hướng dẫn nhanh - Push code lên GitHub

## ✅ Git đã được cài đặt và cấu hình!

- **Git version:** 2.51.2.windows.1
- **User name:** Thinh Nguyen  
- **User email:** nquocthinh06@gmail.com

## Các bước tiếp theo:

### Bước 1: Tạo repository trên GitHub

1. Truy cập: https://github.com/new
2. Đặt tên repository (ví dụ: `yolov5-traffic-detection`)
3. Chọn **Public** hoặc **Private**
4. **KHÔNG** tích "Initialize with README"
5. Click **"Create repository"**

### Bước 2: Chạy script tự động

Sau khi tạo repository trên GitHub, chạy lệnh:

```powershell
# Refresh PATH và chạy script
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
.\push-to-github.ps1
```

Khi script hỏi URL repository, nhập URL bạn vừa tạo, ví dụ:
```
https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

### Bước 3: Xác thực GitHub (nếu cần)

**Nếu dùng HTTPS:**
- GitHub sẽ yêu cầu username và **Personal Access Token (PAT)**
- Tạo PAT tại: https://github.com/settings/tokens
- Chọn quyền `repo` (full control)
- Dùng token thay cho password

**Nếu dùng SSH (khuyến nghị):**
```powershell
# Tạo SSH key
ssh-keygen -t ed25519 -C "nquocthinh06@gmail.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub
```

Sau đó thêm SSH key vào GitHub: https://github.com/settings/keys

### Hoặc thực hiện thủ công:

```powershell
# Refresh PATH
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# 1. Khởi tạo git
git init

# 2. Thêm files
git add .

# 3. Commit
git commit -m "Initial commit: YOLOv5 traffic detection project"

# 4. Đổi nhánh thành main
git branch -M main

# 5. Thêm remote (thay YOUR_USERNAME và YOUR_REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 6. Push lên GitHub
git push -u origin main
```

## ⚠️ Lưu ý:

1. **File .gitignore** đã được cấu hình để loại trừ:
   - File weights (*.pt)
   - Ảnh và video lớn
   - Thư mục __pycache__

2. **Nếu gặp lỗi PATH:**
   - Đóng và mở lại PowerShell
   - Hoặc chạy script với PATH đã refresh

3. **Sau khi push thành công:**
   - Code sẽ có sẵn trên GitHub
   - Bạn có thể chia sẻ link repository
   - Clone về máy khác: `git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git`

## 📚 Xem thêm:

- `HUONG_DAN_PUSH_GITHUB.md` - Hướng dẫn chi tiết đầy đủ
- `push-to-github.ps1` - Script tự động push code
- `setup-git.ps1` - Script kiểm tra cấu hình Git

