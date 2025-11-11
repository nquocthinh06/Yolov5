#!/usr/bin/env python3
"""
🎬 Tạo video demo cho test chức năng xử lý video
"""

import cv2
import numpy as np
import os

def create_demo_video():
    """Tạo video demo với các đối tượng di chuyển"""
    
    # Thông số video
    width, height = 640, 480
    fps = 30
    duration = 5  # 5 giây
    total_frames = fps * duration
    
    # Tạo video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('demo_traffic_video.mp4', fourcc, fps, (width, height))
    
    print("🎬 Đang tạo video demo...")
    
    for frame_num in range(total_frames):
        # Tạo background
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:] = (50, 50, 50)  # Màu xám đậm
        
        # Vẽ đường
        cv2.rectangle(frame, (0, height//2 - 30), (width, height//2 + 30), (80, 80, 80), -1)
        cv2.line(frame, (0, height//2), (width, height//2), (255, 255, 255), 2)
        
        # Xe di chuyển từ trái sang phải
        car_x = int((frame_num / total_frames) * (width + 100) - 50)
        car_y = height//2 - 15
        
        if 0 <= car_x <= width:
            # Vẽ xe (hình chữ nhật)
            cv2.rectangle(frame, (car_x, car_y), (car_x + 60, car_y + 30), (0, 100, 255), -1)
            cv2.rectangle(frame, (car_x + 5, car_y + 5), (car_x + 55, car_y + 15), (150, 200, 255), -1)
            # Bánh xe
            cv2.circle(frame, (car_x + 15, car_y + 30), 8, (0, 0, 0), -1)
            cv2.circle(frame, (car_x + 45, car_y + 30), 8, (0, 0, 0), -1)
        
        # Người đi bộ
        person_x = int(100 + 50 * np.sin(frame_num * 0.1))
        person_y = height//2 + 50
        
        # Vẽ người (đơn giản)
        cv2.circle(frame, (person_x, person_y - 20), 10, (0, 255, 0), -1)  # Đầu
        cv2.rectangle(frame, (person_x - 8, person_y - 10), (person_x + 8, person_y + 10), (0, 255, 0), -1)  # Thân
        cv2.line(frame, (person_x, person_y + 10), (person_x - 5, person_y + 25), (0, 255, 0), 3)  # Chân trái
        cv2.line(frame, (person_x, person_y + 10), (person_x + 5, person_y + 25), (0, 255, 0), 3)  # Chân phải
        
        # Xe thứ 2 di chuyển ngược chiều
        car2_x = int(width - (frame_num / total_frames) * (width + 80))
        car2_y = height//2 + 5
        
        if 0 <= car2_x <= width:
            cv2.rectangle(frame, (car2_x, car2_y), (car2_x + 50, car2_y + 25), (255, 100, 0), -1)
            cv2.rectangle(frame, (car2_x + 5, car2_y + 5), (car2_x + 45, car2_y + 15), (255, 200, 100), -1)
            cv2.circle(frame, (car2_x + 12, car2_y + 25), 6, (0, 0, 0), -1)
            cv2.circle(frame, (car2_x + 38, car2_y + 25), 6, (0, 0, 0), -1)
        
        # Thêm text thông tin
        cv2.putText(frame, f"Frame: {frame_num + 1}/{total_frames}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Demo Traffic Video", (10, height - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Ghi frame
        out.write(frame)
        
        # Progress
        if frame_num % 30 == 0:
            progress = (frame_num / total_frames) * 100
            print(f"⏳ Tiến trình: {progress:.1f}%")
    
    # Đóng video
    out.release()
    
    print("✅ Đã tạo video demo: demo_traffic_video.mp4")
    print(f"📊 Thông số: {width}x{height}, {fps}fps, {duration}s")
    
    return "demo_traffic_video.mp4"

if __name__ == "__main__":
    video_path = create_demo_video()
    
    # Kiểm tra kích thước file
    if os.path.exists(video_path):
        size_mb = os.path.getsize(video_path) / (1024 * 1024)
        print(f"📁 Kích thước file: {size_mb:.2f} MB")
        print(f"🚀 Có thể test video processing với: {video_path}")
    else:
        print("❌ Lỗi tạo video!")
