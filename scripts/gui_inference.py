#!/usr/bin/env python3
"""
🚗 YOLOv5 Traffic & People Detection GUI - Phiên bản tối ưu
Chuyên dụng cho phát hiện phương tiện giao thông và con người
Sử dụng model YOLOv5x (độ chính xác cao nhất)
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import threading
import os
import cv2
from ultralytics import YOLO
import numpy as np

class TrafficPeopleDetectionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚗 YOLOv5 - Phát hiện Phương tiện & Con người")
        self.root.geometry("1920x1080")
        self.root.configure(bg='#f0f0f0')
        self.root.state('zoomed')  # Fullscreen on Windows
        
        # Khởi tạo model với độ chính xác cao nhất
        self.model = None
        self.input_path = None
        
        # Định nghĩa các class quan trọng
        self.traffic_classes = {
            # Phương tiện giao thông
            0: 'person',
            1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 
            5: 'bus', 6: 'train', 7: 'truck', 8: 'boat',
            # Biển báo giao thông
            9: 'traffic light', 11: 'stop sign', 12: 'parking meter'
        }
        
        # Tạo giao diện
        self.create_widgets()
        
        # Load model với độ chính xác cao nhất
        self.load_best_model()
    
    def create_widgets(self):
        """Tạo giao diện tối ưu"""
        
        # Header với thông tin model
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        header_frame.pack(fill='x', padx=10, pady=5)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🚗 YOLOv5x - Phát hiện Phương tiện & Con người (Độ chính xác cao nhất)", 
                              font=('Arial', 16, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Top frame for images (35% height)
        images_frame = tk.Frame(main_frame, bg='#f0f0f0', height=350)
        images_frame.pack(fill='x', pady=(0, 10))
        images_frame.pack_propagate(False)
        
        # Left panel - Input image
        left_frame = tk.LabelFrame(images_frame, text="📁 Ảnh gốc", font=('Arial', 12, 'bold'),
                                  bg='white', fg='#2c3e50', relief='raised', bd=2)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Right panel - Result image
        right_frame = tk.LabelFrame(images_frame, text="🎯 Kết quả phát hiện", font=('Arial', 12, 'bold'),
                                   bg='white', fg='#2c3e50', relief='raised', bd=2)
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Create image panels
        self.create_image_panel(left_frame, "input")
        self.create_image_panel(right_frame, "result")
        
        # Bottom frame for controls and results (65% height)
        bottom_frame = tk.Frame(main_frame, bg='#f0f0f0')
        bottom_frame.pack(fill='both', expand=True)
        
        # Controls frame
        controls_frame = tk.Frame(bottom_frame, bg='#34495e', height=80)
        controls_frame.pack(fill='x', pady=(0, 10))
        controls_frame.pack_propagate(False)
        
        # Results frame
        results_frame = tk.LabelFrame(bottom_frame, text="📊 Kết quả phân tích chi tiết", font=('Arial', 16, 'bold'),
                                     bg='white', fg='#2c3e50', relief='raised', bd=2)
        results_frame.pack(fill='both', expand=True)
        
        # Create controls and results
        self.create_advanced_controls(controls_frame)
        self.create_traffic_results_panel(results_frame)
    
    def create_image_panel(self, parent, panel_type):
        """Tạo panel hiển thị ảnh với tỷ lệ tối ưu"""
        
        if panel_type == "input":
            # Button frame
            btn_frame = tk.Frame(parent, bg='white')
            btn_frame.pack(pady=10)
            
            select_btn = tk.Button(btn_frame, text="📂 Chọn ảnh", font=('Arial', 12, 'bold'),
                                  bg='#3498db', fg='white', command=self.select_image,
                                  relief='flat', padx=20, pady=10)
            select_btn.pack(side='left', padx=5)
            
            video_btn = tk.Button(btn_frame, text="🎬 Chọn video", font=('Arial', 12, 'bold'),
                                 bg='#9b59b6', fg='white', command=self.select_video,
                                 relief='flat', padx=20, pady=10)
            video_btn.pack(side='left', padx=5)
        
        # Image display frame
        image_frame = tk.Frame(parent, bg='#ecf0f1', relief='solid', bd=2)
        image_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Image label
        if panel_type == "input":
            self.input_image_label = tk.Label(image_frame, text="Chưa có ảnh", 
                                             font=('Arial', 14), bg='#ecf0f1', fg='#7f8c8d')
            self.input_image_label.pack(expand=True)
            
            # File info
            self.file_info_label = tk.Label(parent, text="", font=('Arial', 10), 
                                           bg='white', fg='#7f8c8d')
            self.file_info_label.pack(pady=5)
        else:
            self.result_image_label = tk.Label(image_frame, text="Chờ xử lý...", 
                                              font=('Arial', 14), bg='#ecf0f1', fg='#7f8c8d')
            self.result_image_label.pack(expand=True)
            
            # Save buttons
            save_frame = tk.Frame(parent, bg='white')
            save_frame.pack(pady=5)
            
            save_img_btn = tk.Button(save_frame, text="💾 Lưu ảnh", font=('Arial', 10),
                                    bg='#27ae60', fg='white', command=self.save_result,
                                    relief='flat', padx=12, pady=4)
            save_img_btn.pack(side='left', padx=2)
            
            save_data_btn = tk.Button(save_frame, text="📊 Xuất dữ liệu", font=('Arial', 10),
                                     bg='#f39c12', fg='white', command=self.export_data,
                                     relief='flat', padx=12, pady=4)
            save_data_btn.pack(side='left', padx=2)
    
    def create_advanced_controls(self, parent):
        """Tạo controls nâng cao"""
        
        # Model status
        self.status_label = tk.Label(parent, text="⏳ Đang tải YOLOv5x (Model chính xác nhất)...", 
                                    font=('Arial', 12, 'bold'), fg='white', bg='#34495e')
        self.status_label.pack(side='left', padx=20, pady=20)
        
        # Advanced settings frame
        settings_frame = tk.Frame(parent, bg='#34495e')
        settings_frame.pack(side='left', padx=20, pady=20)
        
        # Confidence threshold
        tk.Label(settings_frame, text="Độ tin cậy:", font=('Arial', 11), 
                fg='white', bg='#34495e').grid(row=0, column=0, sticky='w')
        
        self.conf_var = tk.IntVar(value=60)  # Tăng độ tin cậy mặc định
        self.conf_scale = tk.Scale(settings_frame, from_=30, to=95, orient='horizontal',
                                  variable=self.conf_var, length=120, bg='#34495e', 
                                  fg='white', highlightthickness=0, font=('Arial', 9))
        self.conf_scale.grid(row=0, column=1, padx=10)
        
        # IoU threshold
        tk.Label(settings_frame, text="IoU:", font=('Arial', 11), 
                fg='white', bg='#34495e').grid(row=1, column=0, sticky='w')
        
        self.iou_var = tk.IntVar(value=45)
        self.iou_scale = tk.Scale(settings_frame, from_=30, to=70, orient='horizontal',
                                 variable=self.iou_var, length=120, bg='#34495e', 
                                 fg='white', highlightthickness=0, font=('Arial', 9))
        self.iou_scale.grid(row=1, column=1, padx=10)
        
        # Model selection
        model_frame = tk.Frame(parent, bg='#34495e')
        model_frame.pack(side='left', padx=20, pady=20)
        
        tk.Label(model_frame, text="Model:", font=('Arial', 11), 
                fg='white', bg='#34495e').pack()
        
        self.model_var = tk.StringVar(value="yolov5x.pt")
        model_combo = ttk.Combobox(model_frame, textvariable=self.model_var, 
                                  values=["yolov5n.pt", "yolov5s.pt", "yolov5m.pt", "yolov5l.pt", "yolov5x.pt"],
                                  state="readonly", width=12)
        model_combo.pack(pady=5)
        model_combo.bind('<<ComboboxSelected>>', self.on_model_change)
        
        # Process button
        self.process_btn = tk.Button(parent, text="🚀 Phát hiện (Độ chính xác cao)", 
                                    font=('Arial', 12, 'bold'), bg='#e74c3c', fg='white',
                                    command=self.process_image, state='disabled',
                                    relief='flat', padx=20)
        self.process_btn.pack(side='right', padx=20, pady=20)
    
    def create_traffic_results_panel(self, parent):
        """Tạo panel kết quả chuyên dụng cho giao thông"""
        
        # Create notebook for tabs
        notebook = ttk.Notebook(parent)
        notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Tab 1: Traffic Analysis
        traffic_tab = tk.Frame(notebook, bg='white')
        notebook.add(traffic_tab, text="🚗 Phân tích giao thông")
        
        # Create two columns
        columns_frame = tk.Frame(traffic_tab, bg='white')
        columns_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Left column - Detection results
        left_col = tk.Frame(columns_frame, bg='white')
        left_col.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        tk.Label(left_col, text="📋 Danh sách phát hiện:", font=('Arial', 14, 'bold'),
                bg='white', fg='#2c3e50').pack(anchor='w')
        
        results_text_frame = tk.Frame(left_col, bg='white')
        results_text_frame.pack(fill='both', expand=True, pady=10)
        
        self.results_text = tk.Text(results_text_frame, height=20, font=('Arial', 12), 
                                   bg='white', relief='flat', wrap=tk.WORD)
        scrollbar_results = ttk.Scrollbar(results_text_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar_results.set)
        
        self.results_text.pack(side='left', fill='both', expand=True)
        scrollbar_results.pack(side='right', fill='y')
        
        # Right column - Statistics
        right_col = tk.Frame(columns_frame, bg='white')
        right_col.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        tk.Label(right_col, text="📊 Thống kê tổng quan:", font=('Arial', 14, 'bold'),
                bg='white', fg='#2c3e50').pack(anchor='w')
        
        self.stats_text = tk.Text(right_col, height=20, font=('Arial', 12), 
                                 bg='white', relief='flat', wrap=tk.WORD)
        self.stats_text.pack(fill='both', expand=True, pady=10)
        
        # Tab 2: Vehicle Details
        vehicle_tab = tk.Frame(notebook, bg='white')
        notebook.add(vehicle_tab, text="🚙 Chi tiết phương tiện")
        
        self.vehicle_text = tk.Text(vehicle_tab, height=25, font=('Arial', 12), 
                                   bg='white', relief='flat', wrap=tk.WORD)
        self.vehicle_text.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Tab 3: People Analysis
        people_tab = tk.Frame(notebook, bg='white')
        notebook.add(people_tab, text="👥 Phân tích con người")
        
        self.people_text = tk.Text(people_tab, height=25, font=('Arial', 12), 
                                  bg='white', relief='flat', wrap=tk.WORD)
        self.people_text.pack(fill='both', expand=True, padx=20, pady=20)
    
    def load_best_model(self):
        """Tải model với độ chính xác cao nhất"""
        
        def load():
            try:
                self.status_label.config(text="📥 Đang tải YOLOv5x (Model chính xác nhất)...")
                # Sử dụng YOLOv5x để có độ chính xác cao nhất
                self.model = YOLO('yolov5x.pt')
                self.status_label.config(text="✅ YOLOv5x sẵn sàng! (Độ chính xác: 50.7% mAP)")
                self.process_btn.config(state='normal')
            except Exception as e:
                self.status_label.config(text=f"❌ Lỗi: {str(e)}")
                messagebox.showerror("Lỗi", f"Không thể tải model: {str(e)}")
        
        thread = threading.Thread(target=load)
        thread.daemon = True
        thread.start()
    
    def on_model_change(self, event):
        """Thay đổi model"""
        
        def change_model():
            try:
                model_name = self.model_var.get()
                self.status_label.config(text=f"📥 Đang tải {model_name}...")
                self.model = YOLO(model_name)
                
                # Thông tin về độ chính xác của từng model
                accuracy_info = {
                    "yolov5n.pt": "28.0% mAP (Nhanh nhất)",
                    "yolov5s.pt": "37.4% mAP (Cân bằng)",
                    "yolov5m.pt": "45.4% mAP (Tốt)",
                    "yolov5l.pt": "49.0% mAP (Rất tốt)",
                    "yolov5x.pt": "50.7% mAP (Chính xác nhất)"
                }
                
                self.status_label.config(text=f"✅ {model_name} sẵn sàng! ({accuracy_info.get(model_name, 'Không rõ')})")
                self.process_btn.config(state='normal')
                
            except Exception as e:
                self.status_label.config(text=f"❌ Lỗi: {str(e)}")
                messagebox.showerror("Lỗi", f"Không thể tải model {model_name}: {str(e)}")
        
        thread = threading.Thread(target=change_model)
        thread.daemon = True
        thread.start()
    
    def select_image(self):
        """Chọn ảnh"""
        
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh",
            filetypes=[
                ("Ảnh", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp"),
                ("Tất cả", "*.*")
            ]
        )
        
        if file_path:
            self.load_image(file_path)
    
    def select_video(self):
        """Chọn video"""
        
        file_path = filedialog.askopenfilename(
            title="Chọn video",
            filetypes=[
                ("Video", "*.mp4 *.avi *.mov *.mkv *.wmv"),
                ("Tất cả", "*.*")
            ]
        )
        
        if file_path:
            self.process_video(file_path)
    
    def load_image(self, file_path):
        """Tải và hiển thị ảnh"""
        
        try:
            self.input_path = file_path
            
            # Load ảnh
            image = Image.open(file_path)
            
            # Resize để hiển thị
            display_image = image.copy()
            panel_width, panel_height = 500, 300
            img_width, img_height = display_image.size
            
            # Tính tỷ lệ scale
            scale_w = panel_width / img_width
            scale_h = panel_height / img_height
            scale = min(scale_w, scale_h)
            
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            display_image = display_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(display_image)
            
            # Hiển thị
            self.input_image_label.config(image=photo, text="")
            self.input_image_label.image = photo
            
            # File info
            filename = os.path.basename(file_path)
            size = f"{image.size[0]}x{image.size[1]}"
            self.file_info_label.config(text=f"📄 {filename} ({size})")
            
            # Clear results
            self.result_image_label.config(image="", text="Chờ xử lý...")
            self.clear_all_results()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải ảnh: {str(e)}")
    
    def process_image(self):
        """Xử lý ảnh với cấu hình tối ưu"""
        
        if not self.input_path:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ảnh trước!")
            return
        
        if not self.model:
            messagebox.showwarning("Cảnh báo", "Model chưa sẵn sàng!")
            return
        
        # Disable button
        self.process_btn.config(state='disabled', text="⏳ Đang phân tích...")
        
        # Process in background
        thread = threading.Thread(target=self.process_thread)
        thread.daemon = True
        thread.start()
    
    def process_thread(self):
        """Xử lý trong thread riêng với cấu hình tối ưu"""
        
        try:
            # Get parameters
            confidence = self.conf_var.get() / 100.0
            iou = self.iou_var.get() / 100.0
            
            # Run detection with optimal settings
            results = self.model(self.input_path, conf=confidence, iou=iou, imgsz=640, augment=True)
            
            # Update UI
            self.root.after(0, self.update_traffic_results, results)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Lỗi", f"Lỗi xử lý: {str(e)}"))
            self.root.after(0, lambda: self.process_btn.config(state='normal', text="🚀 Phát hiện (Độ chính xác cao)"))
    
    def update_traffic_results(self, results):
        """Cập nhật kết quả chuyên dụng cho giao thông"""
        
        try:
            # Get result image
            result_image = results[0].plot()
            
            # Convert to PIL
            result_image = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)
            result_pil = Image.fromarray(result_image)
            
            # Resize for display
            panel_width, panel_height = 500, 300
            img_width, img_height = result_pil.size
            
            scale_w = panel_width / img_width
            scale_h = panel_height / img_height
            scale = min(scale_w, scale_h)
            
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            result_pil = result_pil.resize((new_width, new_height), Image.Resampling.LANCZOS)
            result_photo = ImageTk.PhotoImage(result_pil)
            
            # Display result
            self.result_image_label.config(image=result_photo, text="")
            self.result_image_label.image = result_photo
            
            # Clear all text areas
            self.clear_all_results()
            
            result = results[0]
            if result.boxes is not None:
                # Analyze results
                self.analyze_traffic_results(result)
            else:
                self.results_text.insert(tk.END, "❌ Không phát hiện đối tượng nào")
                self.stats_text.insert(tk.END, "❌ Không có dữ liệu thống kê")
            
            # Re-enable button
            self.process_btn.config(state='normal', text="🚀 Phát hiện (Độ chính xác cao)")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi hiển thị: {str(e)}")
            self.process_btn.config(state='normal', text="🚀 Phát hiện (Độ chính xác cao)")
    
    def analyze_traffic_results(self, result):
        """Phân tích kết quả chuyên dụng cho giao thông"""
        
        # Categorize detections
        people = []
        vehicles = []
        traffic_signs = []
        
        for i, box in enumerate(result.boxes):
            class_id = int(box.cls[0])
            class_name = self.model.names[class_id]
            confidence = float(box.conf[0]) * 100
            x1, y1, x2, y2 = box.xyxy[0]
            
            detection_info = {
                'id': i + 1,
                'class_name': class_name,
                'confidence': confidence,
                'bbox': (int(x1), int(y1), int(x2), int(y2)),
                'size': (int(x2-x1), int(y2-y1))
            }
            
            if class_id == 0:  # person
                people.append(detection_info)
            elif class_id in [1, 2, 3, 5, 6, 7, 8]:  # vehicles
                vehicles.append(detection_info)
            elif class_id in [9, 11, 12]:  # traffic signs
                traffic_signs.append(detection_info)
        
        # Update results text
        self.update_detection_results(people, vehicles, traffic_signs)
        self.update_statistics(people, vehicles, traffic_signs)
        self.update_vehicle_details(vehicles)
        self.update_people_analysis(people)
    
    def update_detection_results(self, people, vehicles, traffic_signs):
        """Cập nhật kết quả phát hiện"""
        
        total = len(people) + len(vehicles) + len(traffic_signs)
        
        self.results_text.insert(tk.END, f"🎯 TỔNG QUAN PHÁT HIỆN:\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")
        
        self.results_text.insert(tk.END, f"📊 Tổng số đối tượng: {total}\n")
        self.results_text.insert(tk.END, f"👥 Con người: {len(people)}\n")
        self.results_text.insert(tk.END, f"🚗 Phương tiện: {len(vehicles)}\n")
        self.results_text.insert(tk.END, f"🚦 Biển báo: {len(traffic_signs)}\n\n")
        
        # Detailed list
        all_detections = people + vehicles + traffic_signs
        all_detections.sort(key=lambda x: x['confidence'], reverse=True)
        
        self.results_text.insert(tk.END, "📋 DANH SÁCH CHI TIẾT:\n")
        self.results_text.insert(tk.END, "-" * 40 + "\n")
        
        for detection in all_detections:
            confidence = detection['confidence']
            if confidence >= 80:
                status = "🟢 Rất cao"
            elif confidence >= 60:
                status = "🟡 Cao"
            elif confidence >= 40:
                status = "🟠 Trung bình"
            else:
                status = "🔴 Thấp"
            
            self.results_text.insert(tk.END, 
                                   f"\n{detection['id']:2d}. {detection['class_name'].upper()}\n"
                                   f"    Độ tin cậy: {confidence:5.1f}% {status}\n"
                                   f"    Vị trí: ({detection['bbox'][0]}, {detection['bbox'][1]}) → "
                                   f"({detection['bbox'][2]}, {detection['bbox'][3]})\n"
                                   f"    Kích thước: {detection['size'][0]} x {detection['size'][1]} pixels\n")
    
    def update_statistics(self, people, vehicles, traffic_signs):
        """Cập nhật thống kê"""
        
        self.stats_text.insert(tk.END, "📈 THỐNG KÊ CHI TIẾT:\n")
        self.stats_text.insert(tk.END, "=" * 40 + "\n\n")
        
        # Overall stats
        total = len(people) + len(vehicles) + len(traffic_signs)
        if total > 0:
            all_confidences = [d['confidence'] for d in people + vehicles + traffic_signs]
            avg_conf = sum(all_confidences) / len(all_confidences)
            max_conf = max(all_confidences)
            min_conf = min(all_confidences)
            
            self.stats_text.insert(tk.END, f"📊 Độ tin cậy trung bình: {avg_conf:.1f}%\n")
            self.stats_text.insert(tk.END, f"📊 Độ tin cậy cao nhất: {max_conf:.1f}%\n")
            self.stats_text.insert(tk.END, f"📊 Độ tin cậy thấp nhất: {min_conf:.1f}%\n\n")
        
        # People statistics
        if people:
            people_confidences = [p['confidence'] for p in people]
            self.stats_text.insert(tk.END, f"👥 THỐNG KÊ CON NGƯỜI:\n")
            self.stats_text.insert(tk.END, f"   • Số lượng: {len(people)}\n")
            self.stats_text.insert(tk.END, f"   • Độ tin cậy TB: {sum(people_confidences)/len(people_confidences):.1f}%\n")
            self.stats_text.insert(tk.END, f"   • Phân bố: {self.get_confidence_distribution(people_confidences)}\n\n")
        
        # Vehicle statistics
        if vehicles:
            vehicle_types = {}
            for v in vehicles:
                vtype = v['class_name']
                if vtype not in vehicle_types:
                    vehicle_types[vtype] = []
                vehicle_types[vtype].append(v['confidence'])
            
            self.stats_text.insert(tk.END, f"🚗 THỐNG KÊ PHƯƠNG TIỆN:\n")
            self.stats_text.insert(tk.END, f"   • Tổng số: {len(vehicles)}\n")
            self.stats_text.insert(tk.END, f"   • Loại phương tiện:\n")
            
            for vtype, confidences in vehicle_types.items():
                avg_conf = sum(confidences) / len(confidences)
                self.stats_text.insert(tk.END, f"     - {vtype}: {len(confidences)} chiếc ({avg_conf:.1f}%)\n")
        
        # Traffic signs statistics
        if traffic_signs:
            self.stats_text.insert(tk.END, f"\n🚦 THỐNG KÊ BIỂN BÁO:\n")
            self.stats_text.insert(tk.END, f"   • Số lượng: {len(traffic_signs)}\n")
            for sign in traffic_signs:
                self.stats_text.insert(tk.END, f"     - {sign['class_name']}: {sign['confidence']:.1f}%\n")
    
    def update_vehicle_details(self, vehicles):
        """Cập nhật chi tiết phương tiện"""
        
        self.vehicle_text.insert(tk.END, "🚙 PHÂN TÍCH CHI TIẾT PHƯƠNG TIỆN:\n")
        self.vehicle_text.insert(tk.END, "=" * 60 + "\n\n")
        
        if not vehicles:
            self.vehicle_text.insert(tk.END, "❌ Không phát hiện phương tiện nào\n")
            return
        
        # Group by vehicle type
        vehicle_groups = {}
        for v in vehicles:
            vtype = v['class_name']
            if vtype not in vehicle_groups:
                vehicle_groups[vtype] = []
            vehicle_groups[vtype].append(v)
        
        for vtype, vehicle_list in vehicle_groups.items():
            self.vehicle_text.insert(tk.END, f"🚗 {vtype.upper()} ({len(vehicle_list)} chiếc):\n")
            self.vehicle_text.insert(tk.END, "-" * 40 + "\n")
            
            for i, vehicle in enumerate(vehicle_list, 1):
                confidence = vehicle['confidence']
                bbox = vehicle['bbox']
                size = vehicle['size']
                
                # Estimate size category
                area = size[0] * size[1]
                if area > 50000:
                    size_category = "Lớn"
                elif area > 20000:
                    size_category = "Trung bình"
                else:
                    size_category = "Nhỏ"
                
                # Estimate position
                x_center = (bbox[0] + bbox[2]) // 2
                if x_center < 213:  # Assuming 640px width
                    position = "Trái"
                elif x_center > 427:
                    position = "Phải"
                else:
                    position = "Giữa"
                
                self.vehicle_text.insert(tk.END, 
                                       f"   {i}. Độ tin cậy: {confidence:.1f}%\n"
                                       f"      Kích thước: {size[0]}x{size[1]}px ({size_category})\n"
                                       f"      Vị trí: {position} màn hình\n"
                                       f"      Tọa độ: ({bbox[0]}, {bbox[1]}) → ({bbox[2]}, {bbox[3]})\n\n")
    
    def update_people_analysis(self, people):
        """Cập nhật phân tích con người"""
        
        self.people_text.insert(tk.END, "👥 PHÂN TÍCH CHI TIẾT CON NGƯỜI:\n")
        self.people_text.insert(tk.END, "=" * 60 + "\n\n")
        
        if not people:
            self.people_text.insert(tk.END, "❌ Không phát hiện con người nào\n")
            return
        
        self.people_text.insert(tk.END, f"📊 Tổng số người: {len(people)}\n\n")
        
        # Analyze people positions and sizes
        for i, person in enumerate(people, 1):
            confidence = person['confidence']
            bbox = person['bbox']
            size = person['size']
            
            # Estimate person size
            height = size[1]
            if height > 200:
                size_category = "Người lớn (gần)"
            elif height > 100:
                size_category = "Người lớn (trung bình)"
            elif height > 50:
                size_category = "Người lớn (xa) / Trẻ em"
            else:
                size_category = "Rất xa / Không rõ"
            
            # Estimate position
            x_center = (bbox[0] + bbox[2]) // 2
            y_center = (bbox[1] + bbox[3]) // 2
            
            if x_center < 213:
                h_position = "Trái"
            elif x_center > 427:
                h_position = "Phải"
            else:
                h_position = "Giữa"
            
            if y_center < 160:
                v_position = "Trên"
            elif y_center > 320:
                v_position = "Dưới"
            else:
                v_position = "Giữa"
            
            # Safety analysis
            if confidence > 80:
                detection_quality = "Rất rõ"
            elif confidence > 60:
                detection_quality = "Rõ"
            elif confidence > 40:
                detection_quality = "Khá rõ"
            else:
                detection_quality = "Mờ"
            
            self.people_text.insert(tk.END, 
                                  f"👤 Người thứ {i}:\n"
                                  f"   • Độ tin cậy: {confidence:.1f}% ({detection_quality})\n"
                                  f"   • Phân loại: {size_category}\n"
                                  f"   • Vị trí: {h_position}-{v_position} màn hình\n"
                                  f"   • Kích thước: {size[0]}x{size[1]}px\n"
                                  f"   • Tọa độ: ({bbox[0]}, {bbox[1]}) → ({bbox[2]}, {bbox[3]})\n\n")
        
        # Safety recommendations
        self.people_text.insert(tk.END, "⚠️ KHUYẾN NGHỊ AN TOÀN:\n")
        self.people_text.insert(tk.END, "-" * 30 + "\n")
        
        high_conf_people = [p for p in people if p['confidence'] > 70]
        if len(high_conf_people) > 3:
            self.people_text.insert(tk.END, "• Khu vực đông người - Cần chú ý khi di chuyển\n")
        
        large_people = [p for p in people if p['size'][1] > 150]
        if large_people:
            self.people_text.insert(tk.END, "• Có người ở gần - Giảm tốc độ và cẩn thận\n")
        
        if len(people) > 0:
            self.people_text.insert(tk.END, "• Luôn tuân thủ luật giao thông và ưu tiên người đi bộ\n")
    
    def get_confidence_distribution(self, confidences):
        """Phân bố độ tin cậy"""
        
        high = len([c for c in confidences if c >= 80])
        medium = len([c for c in confidences if 60 <= c < 80])
        low = len([c for c in confidences if c < 60])
        
        return f"Cao: {high}, TB: {medium}, Thấp: {low}"
    
    def clear_all_results(self):
        """Xóa tất cả kết quả"""
        
        self.results_text.delete(1.0, tk.END)
        self.stats_text.delete(1.0, tk.END)
        self.vehicle_text.delete(1.0, tk.END)
        self.people_text.delete(1.0, tk.END)
    
    def process_video(self, video_path):
        """Xử lý video với phát hiện đối tượng"""
        
        if not self.model:
            messagebox.showwarning("Cảnh báo", "Model chưa sẵn sàng!")
            return
        
        try:
            # Kiểm tra file video
            if not os.path.exists(video_path):
                messagebox.showerror("Lỗi", "File video không tồn tại!")
                return
            
            # Tạo cửa sổ xử lý video
            self.create_video_processing_window(video_path)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xử lý video: {str(e)}")
    
    def create_video_processing_window(self, video_path):
        """Tạo cửa sổ xử lý video với UI nâng cao"""
        
        self.video_path = video_path  # Lưu path để dùng lại
        self.video_window = tk.Toplevel(self.root)
        self.video_window.title("🎬 Xử lý Video - YOLOv5 (Giao diện nâng cao)")
        self.video_window.geometry("1400x900")
        self.video_window.configure(bg='#f0f0f0')
        
        # Header với gradient effect
        header_frame = tk.Frame(self.video_window, bg='#2c3e50', height=60)
        header_frame.pack(fill='x', padx=10, pady=5)
        header_frame.pack_propagate(False)
        
        title_frame = tk.Frame(header_frame, bg='#2c3e50')
        title_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        title_label = tk.Label(title_frame, text=f"🎬 {os.path.basename(video_path)}", 
                              font=('Arial', 16, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(side='left')
        
        # Thông tin video ngay trên header
        self.video_header_info = tk.Label(title_frame, text="Chuẩn bị...", 
                                         font=('Arial', 10), fg='#ecf0f1', bg='#2c3e50')
        self.video_header_info.pack(side='right', padx=20)
        
        # Main content với layout cải thiện
        main_frame = tk.Frame(self.video_window, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Video display area với border đẹp hơn
        video_container = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=3)
        video_container.pack(fill='both', expand=True, pady=(0, 10))
        
        video_frame = tk.LabelFrame(video_container, text="📺 Video Preview (Real-time)", 
                                   font=('Arial', 13, 'bold'), bg='white', fg='#2c3e50', 
                                   relief='flat', bd=0)
        video_frame.pack(fill='both', expand=True, padx=3, pady=3)
        
        self.video_label = tk.Label(video_frame, text="Đang tải video...", 
                                   font=('Arial', 14), bg='#ecf0f1', fg='#7f8c8d')
        self.video_label.pack(expand=True, padx=10, pady=10)
        
        # Stats panel bên cạnh video (tùy chọn - có thể ẩn)
        stats_panel = tk.Frame(video_container, bg='#34495e', width=200)
        stats_panel.pack(side='right', fill='y', padx=(0, 3), pady=3)
        stats_panel.pack_propagate(False)
        
        tk.Label(stats_panel, text="📊 Thống kê Real-time", font=('Arial', 11, 'bold'),
                fg='white', bg='#34495e').pack(pady=10)
        
        self.realtime_fps_label = tk.Label(stats_panel, text="FPS: --", font=('Arial', 10),
                                           fg='#ecf0f1', bg='#34495e')
        self.realtime_fps_label.pack(pady=5)
        
        self.realtime_detections_label = tk.Label(stats_panel, text="Phát hiện: 0", font=('Arial', 10),
                                                  fg='#ecf0f1', bg='#34495e')
        self.realtime_detections_label.pack(pady=5)
        
        self.realtime_time_label = tk.Label(stats_panel, text="Thời gian: 00:00", font=('Arial', 10),
                                           fg='#ecf0f1', bg='#34495e')
        self.realtime_time_label.pack(pady=5)
        
        # Controls với thanh seekbar nâng cao
        controls_frame = tk.Frame(main_frame, bg='#34495e', height=120)
        controls_frame.pack(fill='x', pady=(0, 10))
        controls_frame.pack_propagate(False)
        
        # Thanh seekbar và progress
        seekbar_frame = tk.Frame(controls_frame, bg='#34495e')
        seekbar_frame.pack(fill='x', padx=20, pady=10)
        
        # Time labels
        time_frame = tk.Frame(seekbar_frame, bg='#34495e')
        time_frame.pack(fill='x', pady=(0, 5))
        
        self.current_time_label = tk.Label(time_frame, text="00:00", font=('Arial', 9),
                                          fg='white', bg='#34495e')
        self.current_time_label.pack(side='left')
        
        self.total_time_label = tk.Label(time_frame, text="/ 00:00", font=('Arial', 9),
                                        fg='white', bg='#34495e')
        self.total_time_label.pack(side='right')
        
        # Progress bar với style nâng cao
        progress_frame = tk.Frame(seekbar_frame, bg='#34495e')
        progress_frame.pack(fill='x')
        
        self.video_progress = ttk.Progressbar(progress_frame, mode='determinate', 
                                             length=800, style='TProgressbar')
        self.video_progress.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        # Frame skip control
        skip_frame = tk.Frame(progress_frame, bg='#34495e')
        skip_frame.pack(side='right')
        
        tk.Label(skip_frame, text="Frame skip:", font=('Arial', 9),
                fg='white', bg='#34495e').pack(side='left', padx=(0, 5))
        
        self.frame_skip_var = tk.IntVar(value=5)
        skip_spin = tk.Spinbox(skip_frame, from_=1, to=30, width=5,
                              textvariable=self.frame_skip_var, font=('Arial', 9),
                              bg='white', fg='#2c3e50')
        skip_spin.pack(side='left')
        
        # Control buttons với layout đẹp hơn
        btn_frame = tk.Frame(controls_frame, bg='#34495e')
        btn_frame.pack(fill='x', padx=20, pady=10)
        
        self.play_btn = tk.Button(btn_frame, text="▶️ Bắt đầu", font=('Arial', 11, 'bold'),
                                 bg='#27ae60', fg='white', 
                                 command=lambda: self.start_video_processing(video_path),
                                 relief='flat', padx=20, pady=8, cursor='hand2',
                                 activebackground='#229954', activeforeground='white')
        self.play_btn.pack(side='left', padx=5)
        
        self.pause_btn = tk.Button(btn_frame, text="⏸️ Tạm dừng", font=('Arial', 11, 'bold'),
                                  bg='#f39c12', fg='white', command=self.pause_video_processing,
                                  relief='flat', padx=20, pady=8, state='disabled',
                                  cursor='hand2', activebackground='#e67e22', activeforeground='white')
        self.pause_btn.pack(side='left', padx=5)
        
        self.stop_btn = tk.Button(btn_frame, text="⏹️ Dừng", font=('Arial', 11, 'bold'),
                                 bg='#e74c3c', fg='white', command=self.stop_video_processing,
                                 relief='flat', padx=20, pady=8, state='disabled',
                                 cursor='hand2', activebackground='#c0392b', activeforeground='white')
        self.stop_btn.pack(side='left', padx=5)
        
        # Info label với thông tin chi tiết
        self.video_info_label = tk.Label(btn_frame, text="Chuẩn bị xử lý video...", 
                                        font=('Arial', 10), fg='white', bg='#34495e')
        self.video_info_label.pack(side='right', padx=20)
        
        # Bottom tabs: group Results and Export actions to avoid hidden content
        bottom_tabs = ttk.Notebook(main_frame)
        bottom_tabs.pack(fill='both', expand=True)

        # Tab A: Results
        results_tab = tk.Frame(bottom_tabs, bg='white')
        bottom_tabs.add(results_tab, text="📊 Kết quả Video")

        # Create notebook for detailed video results inside results_tab
        video_notebook = ttk.Notebook(results_tab)
        video_notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Sub-tab 1: Frame by frame results
        frames_tab = tk.Frame(video_notebook, bg='white')
        video_notebook.add(frames_tab, text="🎞️ Từng frame")

        self.video_results_text = tk.Text(frames_tab, height=15, font=('Arial', 11),
                                          bg='white', relief='flat', wrap=tk.WORD)
        video_scrollbar = ttk.Scrollbar(frames_tab, orient="vertical", command=self.video_results_text.yview)
        self.video_results_text.configure(yscrollcommand=video_scrollbar.set)

        self.video_results_text.pack(side='left', fill='both', expand=True, padx=8, pady=8)
        video_scrollbar.pack(side='right', fill='y', pady=8)

        # Sub-tab 2: Summary statistics
        summary_tab = tk.Frame(video_notebook, bg='white')
        video_notebook.add(summary_tab, text="📈 Tổng hợp")

        self.video_summary_text = tk.Text(summary_tab, height=15, font=('Arial', 11),
                                          bg='white', relief='flat', wrap=tk.WORD)
        self.video_summary_text.pack(fill='both', expand=True, padx=8, pady=8)

        # Tab B: Export/Actions
        actions_tab = tk.Frame(bottom_tabs, bg='#e8f4fd')
        bottom_tabs.add(actions_tab, text="🔧 Xuất kết quả")
        
        # Initialize video processing variables
        self.video_processing = False
        self.video_paused = False
        self.current_frame = 0
        self.total_frames = 0
        self.video_fps = 0
        self.video_duration = 0
        self.processing_fps = 0
        self.last_frame_time = 0
        self.frame_times = []
        self.video_stats = {
            'total_detections': 0,
            'people_count': 0,
            'vehicle_count': 0,
            'frames_processed': 0
        }
        
        # Load video info ngay khi mở cửa sổ
        self.load_video_info(video_path)
        
        # Tạo thư mục kết quả ngay khi mở cửa sổ video
        self.ensure_result_directories()

        # Actions content (moved into the dedicated tab to avoid being hidden)
        action_frame = tk.LabelFrame(actions_tab, text="📦 CÁC CHỨC NĂNG XUẤT KẾT QUẢ", font=('Arial', 12, 'bold'),
                                    bg='#e8f4fd', fg='#2c3e50', relief='raised', bd=2)
        action_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Tạo 2 hàng nút để dễ nhìn
        action_row1 = tk.Frame(action_frame, bg='#e8f4fd')
        action_row1.pack(fill='x', padx=20, pady=10)
        
        action_row2 = tk.Frame(action_frame, bg='#e8f4fd')
        action_row2.pack(fill='x', padx=20, pady=(0, 15))
        
        # Hàng 1: Báo cáo
        tk.Label(action_row1, text="📊 BÁO CÁO:", font=('Arial', 11, 'bold'), 
                bg='#e8f4fd', fg='#2c3e50').pack(side='left', padx=(0, 15))
        
        self.instant_report_btn = tk.Button(action_row1, text="📋 Tạo báo cáo ngay", 
                                           font=('Arial', 11, 'bold'), bg='#9b59b6', fg='white',
                                           command=self.create_instant_report, relief='raised', 
                                           padx=20, pady=8, bd=2)
        self.instant_report_btn.pack(side='left', padx=5)
        
        self.save_report_btn = tk.Button(action_row1, text="📊 Lưu báo cáo chi tiết", 
                                        font=('Arial', 11, 'bold'), bg='#27ae60', fg='white',
                                        command=self.save_video_results, relief='raised', 
                                        padx=20, pady=8, bd=2)
        self.save_report_btn.pack(side='left', padx=5)
        
        # Hàng 2: Video và thư mục
        tk.Label(action_row2, text="🎬 VIDEO:", font=('Arial', 11, 'bold'), 
                bg='#e8f4fd', fg='#2c3e50').pack(side='left', padx=(0, 15))
        
        self.export_video_btn = tk.Button(action_row2, text="🎬 XUẤT VIDEO ĐÃ XỬ LÝ", 
                                         font=('Arial', 12, 'bold'), bg='#e74c3c', fg='white',
                                         command=lambda: self.export_processed_video(video_path), 
                                         relief='raised', padx=25, pady=10, bd=3,
                                         cursor='hand2')
        self.export_video_btn.pack(side='left', padx=5)
        
        self.open_results_btn = tk.Button(action_row2, text="📁 Mở thư mục kết quả", 
                                         font=('Arial', 11, 'bold'), bg='#f39c12', fg='white',
                                         command=self.open_results_folder, relief='raised', 
                                         padx=20, pady=8, bd=2)
        self.open_results_btn.pack(side='left', padx=10)
        
        # Thêm chú thích
        note_label = tk.Label(action_frame, text="💡 Lưu ý: Nút 'XUẤT VIDEO ĐÃ XỬ LÝ' tạo file MP4 với khoanh vùng màu sắc", 
                             font=('Arial', 10, 'italic'), bg='#e8f4fd', fg='#7f8c8d')
        note_label.pack(pady=(0, 10))
    
    def load_video_info(self, video_path):
        """Tải thông tin video và hiển thị ngay"""
        try:
            cap = cv2.VideoCapture(video_path)
            if cap.isOpened():
                self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                self.video_fps = cap.get(cv2.CAP_PROP_FPS)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                
                if self.video_fps > 0:
                    self.video_duration = self.total_frames / self.video_fps
                else:
                    self.video_duration = 0
                
                # Update UI
                duration_str = f"{int(self.video_duration // 60):02d}:{int(self.video_duration % 60):02d}"
                self.video_header_info.config(
                    text=f"{width}x{height} | {self.video_fps:.1f} FPS | {duration_str} | {self.total_frames} frames"
                )
                
                self.total_time_label.config(text=f"/ {duration_str}")
                
                # Hiển thị frame đầu tiên
                ret, frame = cap.read()
                if ret:
                    self.display_video_frame_preview(frame)
                
                cap.release()
        except Exception as e:
            print(f"Lỗi tải thông tin video: {e}")
    
    def display_video_frame_preview(self, frame):
        """Hiển thị frame preview (không có detection)"""
        try:
            # Resize for display
            height, width = frame.shape[:2]
            max_width, max_height = 800, 500
            
            scale = min(max_width/width, max_height/height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            
            resized_frame = cv2.resize(frame, (new_width, new_height))
            resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            
            # Convert to PhotoImage
            frame_image = Image.fromarray(resized_frame)
            frame_photo = ImageTk.PhotoImage(frame_image)
            
            # Update display
            self.video_label.config(image=frame_photo, text="")
            self.video_label.image = frame_photo  # Keep reference
        except Exception as e:
            print(f"Lỗi hiển thị preview: {e}")
    
    def ensure_result_directories(self):
        """Đảm bảo các thư mục kết quả tồn tại"""
        
        directories = ["video_results", "video_reports"]
        
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"✅ Đã tạo thư mục: {directory}/")
        
        # Tạo file README trong mỗi thư mục để giải thích
        self.create_directory_readme()
    
    def create_directory_readme(self):
        """Tạo file README trong các thư mục kết quả"""
        
        try:
            # README cho video_results
            video_results_readme = """# 📁 Video Results - Kết quả Video

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
"""
            
            with open("video_results/README.md", "w", encoding="utf-8") as f:
                f.write(video_results_readme)
            
            # README cho video_reports
            video_reports_readme = """# 📊 Video Reports - Báo cáo Video

Thư mục này chứa các báo cáo phân tích video từ YOLOv5.

## 📋 Loại báo cáo:
- `video_analysis_report_YYYYMMDD_HHMMSS.txt` - Báo cáo tạo ngay lập tức
- `video_detailed_report_YYYYMMDD_HHMMSS.txt` - Báo cáo chi tiết sau xử lý

## 📊 Nội dung báo cáo:
- 📹 Thông tin video: Resolution, FPS, thời lượng
- ⚙️ Cấu hình model: Model sử dụng, confidence, IoU
- 📊 Thống kê phát hiện: Số người, phương tiện, frame có đối tượng
- 🎯 Phân tích mật độ: Mật độ trung bình, đánh giá giao thông
- 💡 Khuyến nghị: Dựa trên phân tích tự động
- 🎞️ Kết quả chi tiết từng frame

## 🔧 Cách tạo báo cáo:
1. Mở video trong ứng dụng
2. Click "📋 Tạo báo cáo ngay" (bất cứ lúc nào)
3. Hoặc click "📊 Lưu báo cáo chi tiết" (sau khi xử lý)

Được tạo bởi YOLOv5 Traffic Detection GUI
"""
            
            with open("video_reports/README.md", "w", encoding="utf-8") as f:
                f.write(video_reports_readme)
                
        except Exception as e:
            print(f"Lỗi tạo README: {e}")
    
    def start_video_processing(self, video_path):
        """Bắt đầu xử lý video"""
        
        if self.video_processing:
            return
        
        self.video_processing = True
        self.video_paused = False
        
        # Update buttons
        self.play_btn.config(state='disabled')
        self.pause_btn.config(state='normal')
        self.stop_btn.config(state='normal')
        
        # Clear previous results
        self.video_results_text.delete(1.0, tk.END)
        self.video_summary_text.delete(1.0, tk.END)
        
        # Reset stats
        self.video_stats = {
            'total_detections': 0,
            'people_count': 0,
            'vehicle_count': 0,
            'frames_processed': 0
        }
        
        # Start processing in background thread
        thread = threading.Thread(target=self.process_video_thread, args=(video_path,))
        thread.daemon = True
        thread.start()
    
    def process_video_thread(self, video_path):
        """Xử lý video trong thread riêng với cải tiến"""
        import time
        
        try:
            # Open video
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                self.video_window.after(0, lambda: messagebox.showerror("Lỗi", "Không thể mở video!"))
                return
            
            # Get video properties (đã có từ load_video_info, nhưng lấy lại để chắc chắn)
            self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Update progress bar maximum
            self.video_window.after(0, lambda: self.video_progress.config(maximum=self.total_frames))
            
            # Get processing parameters
            confidence = self.conf_var.get() / 100.0
            iou = self.iou_var.get() / 100.0
            frame_skip = self.frame_skip_var.get()
            
            # Initialize FPS tracking
            self.frame_times = []
            self.last_frame_time = time.time()
            
            frame_count = 0
            last_display_frame = 0
            
            self.video_window.after(0, lambda: self.video_info_label.config(
                text=f"Đang xử lý: {width}x{height} @ {fps:.1f}fps"))
            
            while self.video_processing:
                if self.video_paused:
                    time.sleep(0.1)  # Wait 100ms
                    continue
                
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                self.current_frame = frame_count
                
                # Process every nth frame
                if frame_count % frame_skip == 0:
                    # Track FPS
                    current_time = time.time()
                    if self.last_frame_time > 0:
                        frame_time = current_time - self.last_frame_time
                        self.frame_times.append(frame_time)
                        if len(self.frame_times) > 30:
                            self.frame_times.pop(0)
                        self.processing_fps = len(self.frame_times) / sum(self.frame_times) if self.frame_times else 0
                    self.last_frame_time = current_time
                    
                    # Run detection
                    results = self.model(frame, conf=confidence, iou=iou, verbose=False)
                    
                    # Process results
                    self.process_video_frame_results(results, frame_count, frame.copy())
                    
                    # Update real-time stats
                    if results[0].boxes is not None:
                        num_detections = len(results[0].boxes)
                    else:
                        num_detections = 0
                    
                    self.video_window.after(0, lambda fps_val=self.processing_fps, det=num_detections: 
                                          self.update_realtime_stats(fps_val, det, frame_count))
                
                # Display frame more frequently (every 5 frames instead of 30)
                if frame_count - last_display_frame >= 5:
                    # Show frame with detection if available
                    if frame_count % frame_skip == 0:
                        try:
                            results = self.model(frame, conf=confidence, iou=iou, verbose=False)
                            self.display_video_frame(frame, results[0])
                        except:
                            self.display_video_frame_preview(frame)
                    else:
                        self.display_video_frame_preview(frame)
                    last_display_frame = frame_count
                
                # Update progress
                progress_percent = (frame_count / self.total_frames) * 100
                current_time_pos = (frame_count / fps) if fps > 0 else 0
                self.video_window.after(0, lambda p=progress_percent, f=frame_count, t=current_time_pos: 
                                      self.update_video_progress(p, f, t))
                
                # Small delay để không quá tải
                if frame_count % 10 == 0:
                    time.sleep(0.01)
            
            cap.release()
            
            # Update final summary
            self.video_window.after(0, self.update_video_summary)
            
            # Update buttons
            self.video_window.after(0, self.video_processing_finished)
            
        except Exception as e:
            self.video_window.after(0, lambda: messagebox.showerror("Lỗi", f"Lỗi xử lý video: {str(e)}"))
            self.video_window.after(0, self.video_processing_finished)
    
    def update_realtime_stats(self, fps, detections, frame_num):
        """Cập nhật thống kê real-time"""
        try:
            self.realtime_fps_label.config(text=f"FPS xử lý: {fps:.1f}")
            self.realtime_detections_label.config(text=f"Phát hiện: {detections}")
            
            # Update time
            if self.video_fps > 0:
                current_time_pos = frame_num / self.video_fps
                time_str = f"{int(current_time_pos // 60):02d}:{int(current_time_pos % 60):02d}"
                self.realtime_time_label.config(text=f"Thời gian: {time_str}")
        except:
            pass
    
    def process_video_frame_results(self, results, frame_number, frame):
        """Xử lý kết quả từng frame"""
        
        try:
            result = results[0]
            
            if result.boxes is not None and len(result.boxes) > 0:
                # Count detections
                people_in_frame = 0
                vehicles_in_frame = 0
                
                detections_info = []
                
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    class_name = self.model.names[class_id]
                    confidence = float(box.conf[0]) * 100
                    
                    if class_id == 0:  # person
                        people_in_frame += 1
                    elif class_id in [1, 2, 3, 5, 6, 7, 8]:  # vehicles
                        vehicles_in_frame += 1
                    
                    detections_info.append(f"{class_name}: {confidence:.1f}%")
                
                # Update stats
                self.video_stats['total_detections'] += len(result.boxes)
                self.video_stats['people_count'] += people_in_frame
                self.video_stats['vehicle_count'] += vehicles_in_frame
                self.video_stats['frames_processed'] += 1
                
                # Update results display
                frame_info = (f"Frame {frame_number}: {len(result.boxes)} đối tượng "
                            f"({people_in_frame} người, {vehicles_in_frame} phương tiện)\n"
                            f"   Chi tiết: {', '.join(detections_info)}\n\n")
                
                self.video_window.after(0, lambda info=frame_info: self.video_results_text.insert(tk.END, info))
                self.video_window.after(0, lambda: self.video_results_text.see(tk.END))
                
                # Display current frame (hiển thị thường xuyên hơn - mỗi 5 frame)
                # Display được xử lý trong process_video_thread
                pass
        
        except Exception as e:
            print(f"Error processing frame {frame_number}: {e}")
    
    def display_video_frame(self, frame, result):
        """Hiển thị frame hiện tại với detection"""
        
        try:
            # Draw detections on frame
            annotated_frame = result.plot()
            
            # Convert to RGB
            annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            
            # Resize for display
            height, width = annotated_frame.shape[:2]
            max_width, max_height = 600, 400
            
            scale = min(max_width/width, max_height/height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            
            resized_frame = cv2.resize(annotated_frame, (new_width, new_height))
            
            # Convert to PhotoImage
            frame_image = Image.fromarray(resized_frame)
            frame_photo = ImageTk.PhotoImage(frame_image)
            
            # Update display
            def update_display():
                self.video_label.config(image=frame_photo, text="")
                self.video_label.image = frame_photo  # Keep reference
            
            self.video_window.after(0, update_display)
            
        except Exception as e:
            print(f"Error displaying frame: {e}")
    
    def update_video_progress(self, progress_percent, frame_number, current_time_pos=0):
        """Cập nhật thanh tiến trình với thời gian"""
        
        self.video_progress['value'] = frame_number
        
        # Update time labels
        if self.video_fps > 0 and current_time_pos > 0:
            time_str = f"{int(current_time_pos // 60):02d}:{int(current_time_pos % 60):02d}"
            self.current_time_label.config(text=time_str)
        
        # Update info label
        self.video_info_label.config(
            text=f"Frame {frame_number}/{self.total_frames} ({progress_percent:.1f}%) | "
                 f"FPS: {self.processing_fps:.1f}" if self.processing_fps > 0 else 
                 f"Frame {frame_number}/{self.total_frames} ({progress_percent:.1f}%)"
        )
    
    def update_video_summary(self):
        """Cập nhật thống kê tổng hợp"""
        
        stats = self.video_stats
        
        summary_text = f"""📊 THỐNG KÊ TỔNG HỢP VIDEO:
{"="*50}

📈 Tổng quan:
• Tổng số frame xử lý: {stats['frames_processed']}
• Tổng số đối tượng phát hiện: {stats['total_detections']}
• Trung bình mỗi frame: {stats['total_detections']/max(stats['frames_processed'], 1):.1f} đối tượng

👥 Con người:
• Tổng số người phát hiện: {stats['people_count']}
• Trung bình mỗi frame: {stats['people_count']/max(stats['frames_processed'], 1):.1f} người

🚗 Phương tiện:
• Tổng số phương tiện: {stats['vehicle_count']}
• Trung bình mỗi frame: {stats['vehicle_count']/max(stats['frames_processed'], 1):.1f} phương tiện

🎯 Phân tích:
• Mật độ giao thông: {"Cao" if stats['vehicle_count']/max(stats['frames_processed'], 1) > 5 else "Trung bình" if stats['vehicle_count']/max(stats['frames_processed'], 1) > 2 else "Thấp"}
• Mật độ người: {"Cao" if stats['people_count']/max(stats['frames_processed'], 1) > 3 else "Trung bình" if stats['people_count']/max(stats['frames_processed'], 1) > 1 else "Thấp"}

⚠️ Khuyến nghị:
"""
        
        # Add recommendations based on analysis
        if stats['people_count']/max(stats['frames_processed'], 1) > 3:
            summary_text += "• Khu vực đông người - Cần chú ý an toàn\n"
        
        if stats['vehicle_count']/max(stats['frames_processed'], 1) > 5:
            summary_text += "• Giao thông đông đúc - Cần điều tiết\n"
        
        if stats['total_detections']/max(stats['frames_processed'], 1) > 10:
            summary_text += "• Khu vực hoạt động cao - Tăng cường giám sát\n"
        
        self.video_summary_text.delete(1.0, tk.END)
        self.video_summary_text.insert(tk.END, summary_text)
    
    def pause_video_processing(self):
        """Tạm dừng xử lý video"""
        
        self.video_paused = not self.video_paused
        
        if self.video_paused:
            self.pause_btn.config(text="▶️ Tiếp tục")
        else:
            self.pause_btn.config(text="⏸️ Tạm dừng")
    
    def stop_video_processing(self):
        """Dừng xử lý video"""
        
        self.video_processing = False
        self.video_paused = False
        self.video_processing_finished()
    
    def video_processing_finished(self):
        """Kết thúc xử lý video"""
        
        self.video_processing = False
        self.video_paused = False
        
        # Update buttons
        self.play_btn.config(state='normal', text="🔄 Xử lý lại")
        self.pause_btn.config(state='disabled', text="⏸️ Tạm dừng")
        self.stop_btn.config(state='disabled')
        
        # Thông báo hoàn thành
        messagebox.showinfo("Hoàn thành", 
                           "✅ Xử lý video hoàn tất!\n\n"
                           "🔧 Sử dụng các nút bên dưới để:\n"
                           "• 📋 Tạo báo cáo ngay\n"
                           "• 📊 Lưu báo cáo chi tiết\n"
                           "• 🎬 Xuất video đã xử lý\n"
                           "• 📁 Mở thư mục kết quả")
    
    def save_video_results(self):
        """Lưu kết quả phân tích video"""
        
        try:
            save_path = filedialog.asksaveasfilename(
                title="Lưu kết quả phân tích video",
                defaultextension=".txt",
                filetypes=[
                    ("Text files", "*.txt"),
                    ("CSV files", "*.csv"),
                    ("Tất cả", "*.*")
                ]
            )
            
            if save_path:
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write("🎬 YOLOv5 - Báo cáo phân tích video\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(f"Model: {self.model_var.get()}\n")
                    f.write(f"Độ tin cậy: {self.conf_var.get()}%\n")
                    f.write(f"IoU: {self.iou_var.get()}%\n\n")
                    
                    # Export frame results
                    f.write("KẾT QUẢ TỪNG FRAME:\n")
                    f.write("-" * 40 + "\n")
                    f.write(self.video_results_text.get(1.0, tk.END))
                    f.write("\n\nTHỐNG KÊ TỔNG HỢP:\n")
                    f.write("-" * 40 + "\n")
                    f.write(self.video_summary_text.get(1.0, tk.END))
                
                messagebox.showinfo("Thành công", f"Đã lưu kết quả video: {save_path}")
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu kết quả: {str(e)}")
    
    def create_instant_report(self):
        """Tạo báo cáo ngay lập tức từ dữ liệu hiện tại"""
        
        try:
            # Tạo thư mục reports nếu chưa có
            reports_dir = "video_reports"
            if not os.path.exists(reports_dir):
                os.makedirs(reports_dir)
            
            # Tạo tên file báo cáo
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = f"video_analysis_report_{timestamp}.txt"
            report_path = os.path.join(reports_dir, report_filename)
            
            # Lấy dữ liệu từ các text widget
            frame_results = self.video_results_text.get(1.0, tk.END).strip()
            summary_results = self.video_summary_text.get(1.0, tk.END).strip()
            
            # Tạo báo cáo
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("🎬 BÁO CÁO PHÂN TÍCH VIDEO - YOLOv5\n")
                f.write("=" * 60 + "\n\n")
                
                f.write(f"📅 Thời gian tạo báo cáo: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"⚙️ Model sử dụng: {self.model_var.get()}\n")
                f.write(f"🎯 Độ tin cậy: {self.conf_var.get()}%\n")
                f.write(f"📊 IoU threshold: {self.iou_var.get()}%\n\n")
                
                f.write("📊 THỐNG KÊ TỔNG HỢP:\n")
                f.write("-" * 40 + "\n")
                if summary_results:
                    f.write(summary_results)
                else:
                    f.write("Chưa có dữ liệu thống kê (video chưa được xử lý hoàn toàn)\n")
                f.write("\n\n")
                
                f.write("🎞️ KẾT QUẢ CHI TIẾT TỪNG FRAME:\n")
                f.write("-" * 40 + "\n")
                if frame_results:
                    f.write(frame_results)
                else:
                    f.write("Chưa có dữ liệu chi tiết frame\n")
                
                f.write(f"\n\n📝 Ghi chú: Báo cáo được tạo trong quá trình xử lý video\n")
                f.write(f"📁 Vị trí lưu: {report_path}\n")
            
            # Hiển thị thông báo thành công
            result_msg = f"✅ Đã tạo báo cáo thành công!\n\n📁 File: {report_filename}\n📂 Thư mục: {reports_dir}\n\n🔍 Báo cáo bao gồm:\n• Thống kê tổng hợp\n• Kết quả từng frame\n• Cấu hình model"
            
            response = messagebox.askquestion("Báo cáo đã tạo", 
                                            f"{result_msg}\n\n📂 Bạn có muốn mở thư mục chứa báo cáo không?")
            
            if response == 'yes':
                os.startfile(reports_dir)
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo báo cáo: {str(e)}")
    
    def open_results_folder(self):
        """Mở thư mục chứa kết quả"""
        
        try:
            # Tạo các thư mục nếu chưa có
            folders_to_check = ["video_results", "video_reports"]
            existing_folders = []
            
            for folder in folders_to_check:
                if not os.path.exists(folder):
                    os.makedirs(folder)
                existing_folders.append(folder)
            
            # Mở thư mục đầu tiên (video_results)
            main_folder = "video_results"
            os.startfile(main_folder)
            
            # Thông báo
            messagebox.showinfo("Thư mục kết quả", 
                               f"📂 Đã mở thư mục: {main_folder}\n\n"
                               f"📁 Các thư mục có sẵn:\n"
                               f"• video_results/ - Video đã xử lý\n"
                               f"• video_reports/ - Báo cáo phân tích\n\n"
                               f"💡 Tip: Các file sẽ được tự động lưu vào đây sau khi xử lý")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở thư mục: {str(e)}")
    
    def export_processed_video(self, input_video_path):
        """Xuất video đã xử lý với detection boxes nâng cao"""
        
        try:
            # Tạo thư mục kết quả nếu chưa có
            results_dir = "video_results"
            if not os.path.exists(results_dir):
                os.makedirs(results_dir)
            
            # Tạo tên file với timestamp
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = os.path.splitext(os.path.basename(input_video_path))[0]
            
            # Chọn nơi lưu video
            default_name = f"{base_name}_processed_{timestamp}.mp4"
            output_path = filedialog.asksaveasfilename(
                title="Xuất video đã xử lý",
                initialdir=results_dir,
                initialfile=default_name,
                defaultextension=".mp4",
                filetypes=[
                    ("MP4 Video", "*.mp4"),
                    ("AVI Video", "*.avi"),
                    ("Tất cả", "*.*")
                ]
            )
            
            if not output_path:
                return
            
            # Tạo dialog tiến trình nâng cao
            progress_window = tk.Toplevel(self.video_window)
            progress_window.title("🎬 Đang xuất video nâng cao...")
            progress_window.geometry("500x200")
            progress_window.configure(bg='#f0f0f0')
            progress_window.transient(self.video_window)
            progress_window.grab_set()
            
            # Center the window
            progress_window.geometry("+%d+%d" % (
                self.video_window.winfo_rootx() + 350,
                self.video_window.winfo_rooty() + 150
            ))
            
            tk.Label(progress_window, text="🎬 Đang xuất video với khoanh vùng nâng cao...", 
                    font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(pady=15)
            
            export_progress = ttk.Progressbar(progress_window, mode='determinate')
            export_progress.pack(fill='x', padx=20, pady=10)
            
            export_info_label = tk.Label(progress_window, text="Chuẩn bị...", 
                                        font=('Arial', 10), bg='#f0f0f0')
            export_info_label.pack(pady=5)
            
            # Thêm thông tin chi tiết
            detail_label = tk.Label(progress_window, text="", 
                                   font=('Arial', 9), bg='#f0f0f0', fg='#666')
            detail_label.pack(pady=5)
            
            # Xuất video trong thread riêng
            def export_thread():
                try:
                    # Mở video input
                    cap = cv2.VideoCapture(input_video_path)
                    
                    if not cap.isOpened():
                        progress_window.after(0, lambda: messagebox.showerror("Lỗi", "Không thể mở video!"))
                        progress_window.after(0, progress_window.destroy)
                        return
                    
                    # Lấy thông tin video
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    
                    # Cấu hình video writer với chất lượng cao hơn
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
                    
                    # Cập nhật progress bar
                    progress_window.after(0, lambda: export_progress.config(maximum=total_frames))
                    
                    # Lấy tham số
                    confidence = self.conf_var.get() / 100.0
                    iou = self.iou_var.get() / 100.0
                    
                    frame_count = 0
                    total_detections = 0
                    
                    # Thống kê cho báo cáo
                    video_stats = {
                        'total_people': 0,
                        'total_vehicles': 0,
                        'frames_with_detections': 0
                    }
                    
                    while True:
                        ret, frame = cap.read()
                        if not ret:
                            break
                        
                        frame_count += 1
                        
                        # Chạy detection
                        results = self.model(frame, conf=confidence, iou=iou, verbose=False)
                        
                        # Tùy chỉnh annotation nâng cao
                        annotated_frame = self.create_enhanced_annotation(frame, results[0])
                        
                        # Thống kê
                        if results[0].boxes is not None and len(results[0].boxes) > 0:
                            video_stats['frames_with_detections'] += 1
                            total_detections += len(results[0].boxes)
                            
                            for box in results[0].boxes:
                                class_id = int(box.cls[0])
                                if class_id == 0:  # person
                                    video_stats['total_people'] += 1
                                elif class_id in [1, 2, 3, 5, 6, 7, 8]:  # vehicles
                                    video_stats['total_vehicles'] += 1
                        
                        # Ghi frame
                        out.write(annotated_frame)
                        
                        # Cập nhật progress
                        if frame_count % 5 == 0:  # Cập nhật mỗi 5 frame
                            progress_percent = (frame_count / total_frames) * 100
                            progress_window.after(0, lambda p=progress_percent, f=frame_count, d=total_detections: (
                                export_progress.config(value=f),
                                export_info_label.config(text=f"Frame {f}/{total_frames} ({p:.1f}%)"),
                                detail_label.config(text=f"Đã phát hiện {d} đối tượng")
                            ))
                    
                    # Đóng video
                    cap.release()
                    out.release()
                    
                    # Tạo báo cáo video
                    report_path = output_path.replace('.mp4', '_report.txt')
                    self.create_video_report(report_path, input_video_path, output_path, video_stats, total_frames, fps)
                    
                    # Thông báo hoàn thành với thông tin chi tiết
                    progress_window.after(0, lambda: (
                        progress_window.destroy(),
                        self.show_export_success(output_path, report_path, video_stats, total_detections)
                    ))
                    
                except Exception as e:
                    progress_window.after(0, lambda: (
                        progress_window.destroy(),
                        messagebox.showerror("Lỗi", f"Lỗi xuất video: {str(e)}")
                    ))
            
            # Bắt đầu xuất
            export_thread_obj = threading.Thread(target=export_thread)
            export_thread_obj.daemon = True
            export_thread_obj.start()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất video: {str(e)}")
    
    def create_enhanced_annotation(self, frame, result):
        """Tạo annotation nâng cao với khoanh vùng rõ ràng"""
        
        # Copy frame
        annotated_frame = frame.copy()
        
        if result.boxes is None or len(result.boxes) == 0:
            return annotated_frame
        
        # Định nghĩa màu sắc cho từng loại
        colors = {
            'person': (0, 255, 0),      # Xanh lá - Con người
            'car': (255, 0, 0),         # Đỏ - Xe hơi
            'truck': (255, 165, 0),     # Cam - Xe tải
            'bus': (255, 255, 0),       # Vàng - Xe buýt
            'motorcycle': (255, 0, 255), # Tím - Xe máy
            'bicycle': (0, 255, 255),   # Cyan - Xe đạp
            'default': (255, 255, 255)  # Trắng - Khác
        }
        
        for i, box in enumerate(result.boxes):
            # Lấy thông tin
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
            class_id = int(box.cls[0])
            class_name = self.model.names[class_id]
            confidence = float(box.conf[0]) * 100
            
            # Chọn màu
            color = colors.get(class_name, colors['default'])
            
            # Vẽ khung chính với độ dày tùy theo confidence
            thickness = 3 if confidence > 80 else 2 if confidence > 60 else 1
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, thickness)
            
            # Vẽ khung nền cho text
            label = f"{class_name} {confidence:.1f}%"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.6
            font_thickness = 2
            
            # Tính kích thước text
            (text_width, text_height), baseline = cv2.getTextSize(label, font, font_scale, font_thickness)
            
            # Vẽ nền cho text
            cv2.rectangle(annotated_frame, 
                         (x1, y1 - text_height - 10), 
                         (x1 + text_width + 10, y1), 
                         color, -1)
            
            # Vẽ text
            cv2.putText(annotated_frame, label, 
                       (x1 + 5, y1 - 5), 
                       font, font_scale, (0, 0, 0), font_thickness)
            
            # Thêm ID số thứ tự
            cv2.putText(annotated_frame, f"#{i+1}", 
                       (x1, y2 + 20), 
                       font, 0.5, color, 2)
            
            # Vẽ điểm trung tâm
            center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.circle(annotated_frame, (center_x, center_y), 3, color, -1)
        
        # Thêm thông tin tổng quan lên frame
        info_text = f"Detected: {len(result.boxes)} objects"
        cv2.putText(annotated_frame, info_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Thêm timestamp (giả lập)
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        cv2.putText(annotated_frame, timestamp, (10, annotated_frame.shape[0] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return annotated_frame
    
    def create_video_report(self, report_path, input_path, output_path, stats, total_frames, fps):
        """Tạo báo cáo chi tiết cho video"""
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("🎬 BÁO CÁO PHÂN TÍCH VIDEO - YOLOv5\n")
                f.write("=" * 60 + "\n\n")
                
                # Thông tin video
                f.write("📹 THÔNG TIN VIDEO:\n")
                f.write("-" * 30 + "\n")
                f.write(f"• File gốc: {os.path.basename(input_path)}\n")
                f.write(f"• File đã xử lý: {os.path.basename(output_path)}\n")
                f.write(f"• Tổng số frame: {total_frames}\n")
                f.write(f"• FPS: {fps:.1f}\n")
                f.write(f"• Thời lượng: {total_frames/fps:.1f} giây\n\n")
                
                # Cấu hình model
                f.write("⚙️ CẤU HÌNH MODEL:\n")
                f.write("-" * 30 + "\n")
                f.write(f"• Model: {self.model_var.get()}\n")
                f.write(f"• Độ tin cậy: {self.conf_var.get()}%\n")
                f.write(f"• IoU threshold: {self.iou_var.get()}%\n\n")
                
                # Thống kê phát hiện
                f.write("📊 THỐNG KÊ PHÁT HIỆN:\n")
                f.write("-" * 30 + "\n")
                f.write(f"• Tổng số người: {stats['total_people']}\n")
                f.write(f"• Tổng số phương tiện: {stats['total_vehicles']}\n")
                f.write(f"• Frame có phát hiện: {stats['frames_with_detections']}/{total_frames}\n")
                f.write(f"• Tỷ lệ frame có đối tượng: {stats['frames_with_detections']/total_frames*100:.1f}%\n\n")
                
                # Phân tích mật độ
                avg_people = stats['total_people'] / max(stats['frames_with_detections'], 1)
                avg_vehicles = stats['total_vehicles'] / max(stats['frames_with_detections'], 1)
                
                f.write("🎯 PHÂN TÍCH MẬT ĐỘ:\n")
                f.write("-" * 30 + "\n")
                f.write(f"• Mật độ người TB/frame: {avg_people:.2f}\n")
                f.write(f"• Mật độ phương tiện TB/frame: {avg_vehicles:.2f}\n")
                
                # Đánh giá
                if avg_vehicles > 5:
                    traffic_level = "Cao - Giao thông đông đúc"
                elif avg_vehicles > 2:
                    traffic_level = "Trung bình - Giao thông bình thường"
                else:
                    traffic_level = "Thấp - Giao thông thưa thớt"
                
                f.write(f"• Mức độ giao thông: {traffic_level}\n\n")
                
                # Khuyến nghị
                f.write("💡 KHUYẾN NGHỊ:\n")
                f.write("-" * 30 + "\n")
                if avg_people > 3:
                    f.write("• Khu vực đông người - Cần chú ý an toàn\n")
                if avg_vehicles > 5:
                    f.write("• Giao thông đông đúc - Cần điều tiết\n")
                if stats['frames_with_detections']/total_frames > 0.8:
                    f.write("• Khu vực hoạt động cao - Tăng cường giám sát\n")
                
                f.write(f"\n📅 Thời gian tạo báo cáo: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                
        except Exception as e:
            print(f"Lỗi tạo báo cáo: {e}")
    
    def show_export_success(self, video_path, report_path, stats, total_detections):
        """Hiển thị thông báo thành công với thông tin chi tiết"""
        
        # Tạo cửa sổ thông báo tùy chỉnh
        success_window = tk.Toplevel(self.video_window)
        success_window.title("✅ Xuất video thành công!")
        success_window.geometry("500x400")
        success_window.configure(bg='#f0f0f0')
        success_window.transient(self.video_window)
        success_window.grab_set()
        
        # Center window
        success_window.geometry("+%d+%d" % (
            self.video_window.winfo_rootx() + 350,
            self.video_window.winfo_rooty() + 100
        ))
        
        # Header
        header_frame = tk.Frame(success_window, bg='#27ae60', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="✅ Xuất video thành công!", 
                font=('Arial', 16, 'bold'), fg='white', bg='#27ae60').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(success_window, bg='#f0f0f0')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Thông tin file
        info_text = f"""📁 FILES ĐÃ TẠO:
• Video: {os.path.basename(video_path)}
• Báo cáo: {os.path.basename(report_path)}

📊 THỐNG KÊ:
• Tổng phát hiện: {total_detections} đối tượng
• Người: {stats['total_people']}
• Phương tiện: {stats['total_vehicles']}
• Frame có đối tượng: {stats['frames_with_detections']}

🎯 Video đã được xử lý với khoanh vùng nâng cao:
• Màu sắc phân loại theo đối tượng
• Độ tin cậy hiển thị rõ ràng
• ID đánh số từng đối tượng
• Thông tin timestamp và tổng quan"""
        
        info_label = tk.Label(content_frame, text=info_text, 
                             font=('Arial', 11), bg='#f0f0f0', 
                             justify='left', anchor='w')
        info_label.pack(fill='both', expand=True, pady=10)
        
        # Buttons
        btn_frame = tk.Frame(content_frame, bg='#f0f0f0')
        btn_frame.pack(fill='x', pady=10)
        
        def open_folder():
            os.startfile(os.path.dirname(video_path))
        
        def open_video():
            os.startfile(video_path)
        
        tk.Button(btn_frame, text="📁 Mở thư mục", command=open_folder,
                 font=('Arial', 10, 'bold'), bg='#3498db', fg='white',
                 relief='flat', padx=15, pady=5).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="▶️ Xem video", command=open_video,
                 font=('Arial', 10, 'bold'), bg='#e74c3c', fg='white',
                 relief='flat', padx=15, pady=5).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="✅ Đóng", command=success_window.destroy,
                 font=('Arial', 10, 'bold'), bg='#95a5a6', fg='white',
                 relief='flat', padx=15, pady=5).pack(side='right', padx=5)
    
    def save_result(self):
        """Lưu kết quả ảnh"""
        
        if not hasattr(self, 'input_path') or not self.input_path:
            messagebox.showwarning("Cảnh báo", "Chưa có kết quả để lưu!")
            return
        
        try:
            save_path = filedialog.asksaveasfilename(
                title="Lưu ảnh kết quả",
                defaultextension=".jpg",
                filetypes=[
                    ("JPEG", "*.jpg"),
                    ("PNG", "*.png"),
                    ("Tất cả", "*.*")
                ]
            )
            
            if save_path:
                # Run detection and save
                confidence = self.conf_var.get() / 100.0
                iou = self.iou_var.get() / 100.0
                results = self.model(self.input_path, conf=confidence, iou=iou)
                results[0].save(save_path)
                messagebox.showinfo("Thành công", f"Đã lưu ảnh: {save_path}")
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu ảnh: {str(e)}")
    
    def export_data(self):
        """Xuất dữ liệu phân tích"""
        
        if not hasattr(self, 'input_path') or not self.input_path:
            messagebox.showwarning("Cảnh báo", "Chưa có dữ liệu để xuất!")
            return
        
        try:
            save_path = filedialog.asksaveasfilename(
                title="Xuất dữ liệu phân tích",
                defaultextension=".txt",
                filetypes=[
                    ("Text files", "*.txt"),
                    ("CSV files", "*.csv"),
                    ("Tất cả", "*.*")
                ]
            )
            
            if save_path:
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write("🚗 YOLOv5 - Báo cáo phân tích giao thông\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(f"File: {os.path.basename(self.input_path)}\n")
                    f.write(f"Model: {self.model_var.get()}\n")
                    f.write(f"Độ tin cậy: {self.conf_var.get()}%\n")
                    f.write(f"IoU: {self.iou_var.get()}%\n\n")
                    
                    # Export all results
                    f.write("KẾT QUẢ PHÁT HIỆN:\n")
                    f.write(self.results_text.get(1.0, tk.END))
                    f.write("\nTHỐNG KÊ:\n")
                    f.write(self.stats_text.get(1.0, tk.END))
                
                messagebox.showinfo("Thành công", f"Đã xuất dữ liệu: {save_path}")
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất dữ liệu: {str(e)}")

def main():
    root = tk.Tk()
    app = TrafficPeopleDetectionGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
