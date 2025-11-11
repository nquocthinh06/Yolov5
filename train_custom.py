#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script training YOLOv5 cho biển báo giao thông Việt Nam
Tác giả: AI Assistant
Ngày tạo: 2025
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

def check_dataset_structure():
    """Kiểm tra cấu trúc dataset"""
    dataset_path = Path("datasets/traffic_signs_vietnam")
    
    required_dirs = [
        "images/train", "images/val", "images/test",
        "labels/train", "labels/val", "labels/test"
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        full_path = dataset_path / dir_path
        if not full_path.exists():
            missing_dirs.append(str(full_path))
    
    if missing_dirs:
        print("❌ Thiếu các thư mục sau:")
        for dir_path in missing_dirs:
            print(f"   - {dir_path}")
        return False
    
    print("✅ Cấu trúc dataset đã đúng")
    return True

def count_images():
    """Đếm số lượng ảnh trong dataset"""
    dataset_path = Path("datasets/traffic_signs_vietnam")
    
    train_images = len(list((dataset_path / "images/train").glob("*.jpg")))
    val_images = len(list((dataset_path / "images/val").glob("*.jpg")))
    test_images = len(list((dataset_path / "images/test").glob("*.jpg")))
    
    print(f"📊 Số lượng ảnh:")
    print(f"   - Training: {train_images}")
    print(f"   - Validation: {val_images}")
    print(f"   - Test: {test_images}")
    print(f"   - Tổng: {train_images + val_images + test_images}")
    
    return train_images, val_images, test_images

def copy_sample_images():
    """Copy ảnh mẫu từ my_images vào dataset"""
    my_images_path = Path("my_images")
    train_path = Path("datasets/traffic_signs_vietnam/images/train")
    
    if not my_images_path.exists():
        print("❌ Không tìm thấy thư mục my_images")
        return False
    
    # Copy tất cả ảnh jpg
    copied_count = 0
    for img_file in my_images_path.glob("*.jpg"):
        dest_file = train_path / img_file.name
        if not dest_file.exists():
            import shutil
            shutil.copy2(img_file, dest_file)
            copied_count += 1
            print(f"✅ Đã copy: {img_file.name}")
    
    print(f"📁 Đã copy {copied_count} ảnh vào thư mục training")
    return True

def train_model(model_size="s", epochs=100, batch_size=16, img_size=640, device="0"):
    """Training model YOLOv5"""
    
    # Kiểm tra dataset
    if not check_dataset_structure():
        print("❌ Vui lòng kiểm tra lại cấu trúc dataset")
        return False
    
    # Đếm ảnh
    train_count, val_count, test_count = count_images()
    
    if train_count == 0:
        print("❌ Không có ảnh training. Vui lòng copy ảnh vào thư mục train/")
        return False
    
    # Chọn model
    model_weights = f"yolov5{model_size}.pt"
    
    # Tạo command training
    cmd = [
        "python", "train.py",
        "--data", "data/traffic_signs_vietnam.yaml",
        "--weights", model_weights,
        "--img", str(img_size),
        "--epochs", str(epochs),
        "--batch-size", str(batch_size),
        "--device", device,
        "--name", f"traffic_signs_{model_size}",
        "--project", "runs/train"
    ]
    
    print(f"🚀 Bắt đầu training với:")
    print(f"   - Model: {model_weights}")
    print(f"   - Epochs: {epochs}")
    print(f"   - Batch size: {batch_size}")
    print(f"   - Image size: {img_size}")
    print(f"   - Device: {device}")
    print(f"   - Command: {' '.join(cmd)}")
    
    # Chạy training
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print("✅ Training hoàn thành!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi training: {e}")
        return False

def test_model(weights_path=None):
    """Test model đã training"""
    if weights_path is None:
        # Tìm model tốt nhất
        runs_path = Path("runs/train")
        if not runs_path.exists():
            print("❌ Không tìm thấy thư mục runs/train")
            return False
        
        # Tìm exp mới nhất
        exp_dirs = [d for d in runs_path.iterdir() if d.is_dir() and d.name.startswith("traffic_signs")]
        if not exp_dirs:
            print("❌ Không tìm thấy model đã training")
            return False
        
        latest_exp = max(exp_dirs, key=lambda x: x.stat().st_mtime)
        weights_path = latest_exp / "weights" / "best.pt"
    
    if not weights_path.exists():
        print(f"❌ Không tìm thấy file weights: {weights_path}")
        return False
    
    # Test command
    cmd = [
        "python", "detect.py",
        "--weights", str(weights_path),
        "--source", "my_images/",
        "--conf", "0.5",
        "--save-txt",
        "--save-conf"
    ]
    
    print(f"🧪 Testing model: {weights_path}")
    print(f"   - Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print("✅ Testing hoàn thành!")
        print("📁 Kết quả lưu trong: runs/detect/")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi testing: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Training YOLOv5 cho biển báo giao thông Việt Nam")
    parser.add_argument("--action", choices=["setup", "train", "test", "all"], default="all",
                       help="Hành động thực hiện")
    parser.add_argument("--model", choices=["n", "s", "m", "l", "x"], default="s",
                       help="Kích thước model (n=nano, s=small, m=medium, l=large, x=xlarge)")
    parser.add_argument("--epochs", type=int, default=100, help="Số epochs training")
    parser.add_argument("--batch-size", type=int, default=16, help="Batch size")
    parser.add_argument("--img-size", type=int, default=640, help="Kích thước ảnh")
    parser.add_argument("--device", default="0", help="Device (0,1,2,3 hoặc cpu)")
    parser.add_argument("--weights", help="Đường dẫn đến file weights để test")
    
    args = parser.parse_args()
    
    print("🚦 YOLOv5 Training cho Biển báo Giao thông Việt Nam")
    print("=" * 50)
    
    if args.action in ["setup", "all"]:
        print("\n📋 Bước 1: Setup dataset")
        if not check_dataset_structure():
            print("❌ Vui lòng tạo cấu trúc dataset trước")
            return
        
        copy_sample_images()
        count_images()
    
    if args.action in ["train", "all"]:
        print("\n🚀 Bước 2: Training model")
        success = train_model(
            model_size=args.model,
            epochs=args.epochs,
            batch_size=args.batch_size,
            img_size=args.img_size,
            device=args.device
        )
        
        if not success:
            print("❌ Training thất bại")
            return
    
    if args.action in ["test", "all"]:
        print("\n🧪 Bước 3: Testing model")
        test_model(args.weights)
    
    print("\n✅ Hoàn thành!")
    print("📖 Xem hướng dẫn chi tiết trong file TRAINING_GUIDE.md")

if __name__ == "__main__":
    main()

