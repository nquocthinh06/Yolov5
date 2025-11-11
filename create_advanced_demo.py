#!/usr/bin/env python3
"""
🎬 Tạo video demo nâng cao với nhiều đối tượng và khoanh vùng rõ ràng
"""

import cv2
import numpy as np
import os
import random

def create_advanced_demo_video():
    """Tạo video demo nâng cao với nhiều loại đối tượng"""
    
    # Thông số video
    width, height = 1280, 720  # HD resolution
    fps = 30
    duration = 10  # 10 giây
    total_frames = fps * duration
    
    # Tạo video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('advanced_traffic_demo.mp4', fourcc, fps, (width, height))
    
    print("🎬 Đang tạo video demo nâng cao...")
    
    # Tạo background một lần
    background = create_background(width, height)
    
    for frame_num in range(total_frames):
        # Copy background
        frame = background.copy()
        
        # Thêm các đối tượng di chuyển
        frame = add_moving_cars(frame, frame_num, total_frames, width, height)
        frame = add_moving_people(frame, frame_num, total_frames, width, height)
        frame = add_traffic_elements(frame, frame_num, width, height)
        
        # Thêm thông tin frame
        add_frame_info(frame, frame_num, total_frames, width, height)
        
        # Ghi frame
        out.write(frame)
        
        # Progress
        if frame_num % 60 == 0:  # Mỗi 2 giây
            progress = (frame_num / total_frames) * 100
            print(f"⏳ Tiến trình: {progress:.1f}%")
    
    # Đóng video
    out.release()
    
    print("✅ Đã tạo video demo nâng cao: advanced_traffic_demo.mp4")
    print(f"📊 Thông số: {width}x{height}, {fps}fps, {duration}s")
    
    return "advanced_traffic_demo.mp4"

def create_background(width, height):
    """Tạo background đường phố"""
    
    bg = np.zeros((height, width, 3), dtype=np.uint8)
    bg[:] = (60, 80, 60)  # Màu xanh đậm
    
    # Vẽ đường chính
    road_y = height // 2
    road_height = 120
    cv2.rectangle(bg, (0, road_y - road_height//2), (width, road_y + road_height//2), (80, 80, 80), -1)
    
    # Vẽ vạch kẻ đường
    for x in range(0, width, 60):
        cv2.rectangle(bg, (x, road_y - 3), (x + 30, road_y + 3), (255, 255, 255), -1)
    
    # Vẽ vỉa hè
    cv2.rectangle(bg, (0, road_y + road_height//2), (width, road_y + road_height//2 + 40), (120, 120, 120), -1)
    cv2.rectangle(bg, (0, road_y - road_height//2 - 40), (width, road_y - road_height//2), (120, 120, 120), -1)
    
    # Vẽ cây và tòa nhà đơn giản
    for x in range(100, width, 200):
        # Cây
        cv2.rectangle(bg, (x, 50), (x + 20, 120), (139, 69, 19), -1)  # Thân cây
        cv2.circle(bg, (x + 10, 40), 25, (34, 139, 34), -1)  # Lá cây
        
        # Tòa nhà
        building_height = random.randint(80, 150)
        cv2.rectangle(bg, (x + 50, height - building_height), (x + 120, height), (100, 100, 150), -1)
        
        # Cửa sổ tòa nhà
        for window_y in range(height - building_height + 20, height - 20, 30):
            for window_x in range(x + 60, x + 110, 25):
                cv2.rectangle(bg, (window_x, window_y), (window_x + 15, window_y + 20), (255, 255, 200), -1)
    
    return bg

def add_moving_cars(frame, frame_num, total_frames, width, height):
    """Thêm xe hơi di chuyển"""
    
    road_y = height // 2
    
    # Xe 1: Di chuyển từ trái sang phải (màu đỏ)
    car1_x = int((frame_num / total_frames) * (width + 120) - 60)
    if -60 <= car1_x <= width:
        draw_car(frame, car1_x, road_y - 30, (0, 0, 255), "car")
    
    # Xe 2: Di chuyển từ phải sang trái (màu xanh)
    car2_x = int(width - (frame_num / total_frames) * (width + 100))
    if -100 <= car2_x <= width:
        draw_car(frame, car2_x, road_y + 10, (255, 0, 0), "car")
    
    # Xe tải: Di chuyển chậm hơn (màu cam)
    truck_x = int((frame_num / (total_frames * 1.5)) * (width + 150) - 75)
    if -75 <= truck_x <= width:
        draw_truck(frame, truck_x, road_y - 25, (0, 165, 255))
    
    # Xe buýt: Xuất hiện giữa video (màu vàng)
    if total_frames * 0.3 <= frame_num <= total_frames * 0.7:
        bus_progress = (frame_num - total_frames * 0.3) / (total_frames * 0.4)
        bus_x = int(bus_progress * (width + 200) - 100)
        if -100 <= bus_x <= width:
            draw_bus(frame, bus_x, road_y + 5, (0, 255, 255))
    
    # Xe máy: Di chuyển nhanh (màu tím)
    if frame_num % 150 < 75:  # Xuất hiện định kỳ
        motor_x = int(((frame_num % 150) / 75) * (width + 80) - 40)
        if -40 <= motor_x <= width:
            draw_motorcycle(frame, motor_x, road_y - 35, (255, 0, 255))
    
    return frame

def add_moving_people(frame, frame_num, total_frames, width, height):
    """Thêm người đi bộ"""
    
    sidewalk_y = height // 2 + 80
    
    # Người 1: Đi từ trái sang phải
    person1_x = int((frame_num / (total_frames * 2)) * (width + 40) - 20)
    if -20 <= person1_x <= width:
        draw_person(frame, person1_x, sidewalk_y, (0, 255, 0))
    
    # Người 2: Đi từ phải sang trái
    person2_x = int(width - (frame_num / (total_frames * 1.8)) * (width + 40))
    if -40 <= person2_x <= width:
        draw_person(frame, person2_x, sidewalk_y - 100, (0, 255, 0))
    
    # Nhóm người: Xuất hiện giữa video
    if total_frames * 0.4 <= frame_num <= total_frames * 0.8:
        group_progress = (frame_num - total_frames * 0.4) / (total_frames * 0.4)
        group_x = int(group_progress * (width + 80) - 40)
        if -40 <= group_x <= width:
            draw_person(frame, group_x, sidewalk_y, (0, 255, 0))
            draw_person(frame, group_x + 25, sidewalk_y, (0, 255, 0))
            draw_person(frame, group_x + 50, sidewalk_y, (0, 255, 0))
    
    return frame

def add_traffic_elements(frame, frame_num, width, height):
    """Thêm các yếu tố giao thông"""
    
    # Đèn giao thông (nhấp nháy)
    light_color = (0, 255, 0) if (frame_num // 90) % 2 == 0 else (0, 0, 255)  # Xanh/Đỏ
    draw_traffic_light(frame, width - 100, height // 2 - 150, light_color)
    
    # Biển báo dừng
    draw_stop_sign(frame, 50, height // 2 - 100)
    
    return frame

def draw_car(frame, x, y, color, car_type="car"):
    """Vẽ xe hơi"""
    # Thân xe
    cv2.rectangle(frame, (x, y), (x + 80, y + 35), color, -1)
    cv2.rectangle(frame, (x + 10, y - 15), (x + 70, y), (150, 150, 200), -1)  # Kính
    
    # Bánh xe
    cv2.circle(frame, (x + 15, y + 35), 8, (0, 0, 0), -1)
    cv2.circle(frame, (x + 65, y + 35), 8, (0, 0, 0), -1)
    
    # Đèn xe
    cv2.circle(frame, (x + 80, y + 10), 3, (255, 255, 255), -1)
    cv2.circle(frame, (x + 80, y + 25), 3, (255, 255, 255), -1)

def draw_truck(frame, x, y, color):
    """Vẽ xe tải"""
    # Thùng xe
    cv2.rectangle(frame, (x, y), (x + 120, y + 45), color, -1)
    # Cabin
    cv2.rectangle(frame, (x + 90, y - 20), (x + 120, y), (100, 100, 150), -1)
    # Bánh xe
    cv2.circle(frame, (x + 20, y + 45), 10, (0, 0, 0), -1)
    cv2.circle(frame, (x + 60, y + 45), 10, (0, 0, 0), -1)
    cv2.circle(frame, (x + 100, y + 45), 10, (0, 0, 0), -1)

def draw_bus(frame, x, y, color):
    """Vẽ xe buýt"""
    # Thân xe buýt
    cv2.rectangle(frame, (x, y), (x + 140, y + 50), color, -1)
    # Cửa sổ
    for window_x in range(x + 10, x + 130, 25):
        cv2.rectangle(frame, (window_x, y - 15), (window_x + 20, y), (200, 200, 255), -1)
    # Bánh xe
    cv2.circle(frame, (x + 25, y + 50), 12, (0, 0, 0), -1)
    cv2.circle(frame, (x + 115, y + 50), 12, (0, 0, 0), -1)

def draw_motorcycle(frame, x, y, color):
    """Vẽ xe máy"""
    # Thân xe
    cv2.rectangle(frame, (x, y), (x + 50, y + 20), color, -1)
    # Bánh xe
    cv2.circle(frame, (x + 10, y + 20), 6, (0, 0, 0), -1)
    cv2.circle(frame, (x + 40, y + 20), 6, (0, 0, 0), -1)
    # Người lái
    cv2.circle(frame, (x + 25, y - 10), 8, (0, 255, 0), -1)

def draw_person(frame, x, y, color):
    """Vẽ người"""
    # Đầu
    cv2.circle(frame, (x, y - 25), 8, color, -1)
    # Thân
    cv2.rectangle(frame, (x - 6, y - 15), (x + 6, y + 5), color, -1)
    # Chân
    cv2.line(frame, (x, y + 5), (x - 8, y + 20), color, 3)
    cv2.line(frame, (x, y + 5), (x + 8, y + 20), color, 3)
    # Tay
    cv2.line(frame, (x - 6, y - 5), (x - 15, y + 5), color, 2)
    cv2.line(frame, (x + 6, y - 5), (x + 15, y + 5), color, 2)

def draw_traffic_light(frame, x, y, light_color):
    """Vẽ đèn giao thông"""
    # Cột
    cv2.rectangle(frame, (x, y), (x + 15, y + 100), (100, 100, 100), -1)
    # Hộp đèn
    cv2.rectangle(frame, (x - 10, y - 30), (x + 25, y + 10), (50, 50, 50), -1)
    # Đèn
    cv2.circle(frame, (x + 7, y - 15), 5, light_color, -1)

def draw_stop_sign(frame, x, y):
    """Vẽ biển báo dừng"""
    # Cột
    cv2.rectangle(frame, (x + 15, y + 30), (x + 20, y + 80), (100, 100, 100), -1)
    # Biển báo (hình bát giác đơn giản hóa thành hình chữ nhật)
    cv2.rectangle(frame, (x, y), (x + 30, y + 30), (0, 0, 255), -1)
    cv2.putText(frame, "STOP", (x + 2, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

def add_frame_info(frame, frame_num, total_frames, width, height):
    """Thêm thông tin frame"""
    
    # Thông tin góc trên trái
    info_text = f"Frame: {frame_num + 1}/{total_frames}"
    cv2.putText(frame, info_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    # Thời gian giả lập
    seconds = (frame_num / 30) % 60
    minutes = int((frame_num / 30) // 60)
    time_text = f"Time: {minutes:02d}:{seconds:05.2f}"
    cv2.putText(frame, time_text, (10, height - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Tiêu đề
    cv2.putText(frame, "Advanced Traffic Demo - YOLOv5 Test", (10, height - 20), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Thông tin góc phải
    progress = (frame_num / total_frames) * 100
    progress_text = f"Progress: {progress:.1f}%"
    cv2.putText(frame, progress_text, (width - 200, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

if __name__ == "__main__":
    video_path = create_advanced_demo_video()
    
    # Kiểm tra kích thước file
    if os.path.exists(video_path):
        size_mb = os.path.getsize(video_path) / (1024 * 1024)
        print(f"📁 Kích thước file: {size_mb:.2f} MB")
        print(f"🚀 Video demo nâng cao sẵn sàng test: {video_path}")
        print("\n🎯 Video này bao gồm:")
        print("  • Nhiều loại xe: car, truck, bus, motorcycle")
        print("  • Người đi bộ với chuyển động tự nhiên")
        print("  • Đèn giao thông và biển báo")
        print("  • Background đường phố chi tiết")
        print("  • Resolution HD (1280x720)")
        print("  • Thời lượng 10 giây")
    else:
        print("❌ Lỗi tạo video!")
