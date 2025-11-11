# Hướng dẫn đẩy source code lên GitHub

## Bước 1: Cài đặt Git (nếu chưa có)

### Cách 1: Tải Git từ trang chính thức

1. Truy cập: https://git-scm.com/download/win
2. Tải và cài đặt Git cho Windows
3. Trong quá trình cài đặt, chọn các tùy chọn mặc định

### Cách 2: Cài đặt qua Chocolatey (nếu đã có Chocolatey)

```powershell
choco install git
```

### Cách 3: Cài đặt qua winget (Windows 10/11)

```powershell
winget install --id Git.Git -e --source winget
```

Sau khi cài đặt, mở lại PowerShell và kiểm tra:

```powershell
git --version
```

## Bước 2: Cấu hình Git (chỉ cần làm 1 lần)

Mở PowerShell và chạy các lệnh sau:

```powershell
git config --global user.name "Tên của bạn"
git config --global user.email "email@example.com"
```

## Bước 3: Tạo repository trên GitHub

1. Đăng nhập vào GitHub: https://github.com
2. Click nút **"+"** ở góc trên bên phải → chọn **"New repository"**
3. Đặt tên repository (ví dụ: `yolov5-traffic-detection`)
4. Chọn **Public** hoặc **Private**
5. **KHÔNG** tích chọn "Initialize this repository with a README" (vì bạn đã có code sẵn)
6. Click **"Create repository"**

## Bước 4: Khởi tạo Git repository và push code

### Cách 1: Sử dụng script tự động (Khuyến nghị)

Chạy script PowerShell:

```powershell
.\push-to-github.ps1
```

Script sẽ tự động:

- Kiểm tra Git đã được cài đặt chưa
- Khởi tạo git repository
- Thêm tất cả files
- Tạo commit
- Kết nối với GitHub
- Push code lên GitHub

### Cách 2: Thực hiện thủ công

Mở PowerShell tại thư mục dự án và chạy từng lệnh:

```powershell
# 1. Khởi tạo git repository
git init

# 2. Thêm tất cả files vào staging area
git add .

# 3. Tạo commit đầu tiên
git commit -m "Initial commit: YOLOv5 traffic detection project"

# 4. Đổi tên nhánh chính thành main (nếu cần)
git branch -M main

# 5. Thêm remote repository (thay YOUR_USERNAME và YOUR_REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 6. Push code lên GitHub
git push -u origin main
```

**Lưu ý:**

- Thay `YOUR_USERNAME` bằng tên GitHub của bạn
- Thay `YOUR_REPO_NAME` bằng tên repository bạn vừa tạo
- Nếu sử dụng SSH thay vì HTTPS, dùng: `git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git`

## Bước 5: Xác thực với GitHub

Khi push lần đầu, GitHub sẽ yêu cầu xác thực:

### Nếu dùng HTTPS:

- GitHub sẽ yêu cầu username và password
- **Lưu ý:** Từ năm 2021, GitHub không còn chấp nhận password thông thường
- Bạn cần tạo **Personal Access Token (PAT)**:
  1. Vào GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
  2. Click "Generate new token (classic)"
  3. Đặt tên token, chọn quyền `repo` (full control)
  4. Copy token và dùng nó thay cho password khi push

### Nếu dùng SSH (Khuyến nghị):

1. Tạo SSH key:

```powershell
ssh-keygen -t ed25519 -C "your_email@example.com"
```

2. Copy public key:

```powershell
cat ~/.ssh/id_ed25519.pub
```

3. Thêm vào GitHub: Settings → SSH and GPG keys → New SSH key
4. Dùng SSH URL khi add remote: `git@github.com:USERNAME/REPO.git`

## Các lệnh Git hữu ích

```powershell
# Xem trạng thái
git status

# Xem lịch sử commit
git log

# Thêm file cụ thể
git add ten_file.py

# Commit với message
git commit -m "Mô tả thay đổi"

# Push code lên GitHub
git push

# Pull code từ GitHub
git pull

# Xem các remote repository
git remote -v
```

## Xử lý lỗi thường gặp

### Lỗi: "fatal: not a git repository"

**Giải pháp:** Chạy `git init` trong thư mục dự án

### Lỗi: "remote origin already exists"

**Giải pháp:** Xóa remote cũ và thêm lại:

```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

### Lỗi: "failed to push some refs"

**Giải pháp:** Pull code từ GitHub trước rồi push lại:

```powershell
git pull origin main --allow-unrelated-histories
git push -u origin main
```

## Lưu ý quan trọng

1. **File .gitignore** đã được cấu hình để loại trừ:
   - File weights (\*.pt)
   - Ảnh và video (_.jpg, _.mp4)
   - Thư mục **pycache**
   - File dữ liệu lớn

2. **Kiểm tra trước khi push:**
   - Không push file nhạy cảm (API keys, passwords)
   - Không push file quá lớn (GitHub giới hạn 100MB/file)

3. **Sau khi push thành công:**
   - Code sẽ có sẵn trên GitHub
   - Bạn có thể chia sẻ link repository
   - Có thể clone về máy khác: `git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git`
