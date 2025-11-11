#!/usr/bin/env python3
"""Ứng dụng GUI YOLOv5 đơn giản - không cần drag & drop."""

import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk
from ultralytics import YOLO


class SimpleYOLOGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 YOLOv5 - Phát hiện đối tượng")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f0f0f0")

        # Khởi tạo model
        self.model = None
        self.input_path = None

        # Tạo giao diện
        self.create_widgets()

        # Load model
        self.load_model()

    def create_widgets(self):
        """Tạo các widget cho giao diện."""
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=50)
        header_frame.pack(fill="x", padx=10, pady=5)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame, text="🚀 YOLOv5 - Phát hiện đối tượng", font=("Arial", 14, "bold"), fg="white", bg="#2c3e50"
        )
        title_label.pack(expand=True)

        # Main content frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Left panel - Input
        left_frame = tk.LabelFrame(
            main_frame, text="📁 Ảnh gốc", font=("Arial", 10, "bold"), bg="white", fg="#2c3e50", relief="raised", bd=2
        )
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Right panel - Result
        right_frame = tk.LabelFrame(
            main_frame,
            text="🎯 Kết quả phát hiện",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#2c3e50",
            relief="raised",
            bd=2,
        )
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        # Left panel content
        self.create_left_panel(left_frame)

        # Right panel content
        self.create_right_panel(right_frame)

        # Bottom controls
        self.create_controls()

    def create_left_panel(self, parent):
        """Tạo panel bên trái."""
        # Select button
        select_btn = tk.Button(
            parent,
            text="📂 Chọn ảnh",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            command=self.select_image,
            relief="flat",
            padx=20,
            pady=10,
        )
        select_btn.pack(pady=10)

        # Image display
        self.input_image_label = tk.Label(
            parent, text="Chưa có ảnh", font=("Arial", 12), bg="#ecf0f1", fg="#7f8c8d", width=40, height=15
        )
        self.input_image_label.pack(pady=10, padx=10)

        # File info
        self.file_info_label = tk.Label(parent, text="", font=("Arial", 9), bg="white", fg="#7f8c8d")
        self.file_info_label.pack(pady=5)

    def create_right_panel(self, parent):
        """Tạo panel bên phải."""
        # Result image
        self.result_image_label = tk.Label(
            parent, text="Chờ xử lý...", font=("Arial", 12), bg="#ecf0f1", fg="#7f8c8d", width=40, height=15
        )
        self.result_image_label.pack(pady=10, padx=10)

        # Results text
        self.results_text = tk.Text(
            parent, height=8, width=40, font=("Arial", 10), bg="white", relief="flat", wrap=tk.WORD
        )
        self.results_text.pack(pady=10, padx=10, fill="both", expand=True)

        # Save button
        save_btn = tk.Button(
            parent,
            text="💾 Lưu kết quả",
            font=("Arial", 10),
            bg="#27ae60",
            fg="white",
            command=self.save_result,
            relief="flat",
            padx=15,
            pady=5,
        )
        save_btn.pack(pady=5)

    def create_controls(self):
        """Tạo controls ở dưới."""
        controls_frame = tk.Frame(self.root, bg="#34495e", height=60)
        controls_frame.pack(fill="x", padx=10, pady=5)
        controls_frame.pack_propagate(False)

        # Model status
        self.status_label = tk.Label(
            controls_frame, text="⏳ Đang tải model...", font=("Arial", 10), fg="white", bg="#34495e"
        )
        self.status_label.pack(side="left", padx=20, pady=15)

        # Confidence slider
        conf_frame = tk.Frame(controls_frame, bg="#34495e")
        conf_frame.pack(side="left", padx=20, pady=15)

        tk.Label(conf_frame, text="Độ tin cậy:", font=("Arial", 10), fg="white", bg="#34495e").pack(side="left")

        self.conf_var = tk.IntVar(value=50)
        self.conf_scale = tk.Scale(
            conf_frame,
            from_=10,
            to=90,
            orient="horizontal",
            variable=self.conf_var,
            length=150,
            bg="#34495e",
            fg="white",
            highlightthickness=0,
        )
        self.conf_scale.pack(side="left", padx=10)

        # Process button
        self.process_btn = tk.Button(
            controls_frame,
            text="🚀 Phát hiện",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            command=self.process_image,
            state="disabled",
            relief="flat",
            padx=20,
        )
        self.process_btn.pack(side="right", padx=20, pady=15)

    def load_model(self):
        """Tải model."""

        def load():
            try:
                self.status_label.config(text="📥 Đang tải YOLOv5s...")
                self.model = YOLO("yolov5s.pt")
                self.status_label.config(text="✅ Model sẵn sàng!")
                self.process_btn.config(state="normal")
            except Exception as e:
                self.status_label.config(text=f"❌ Lỗi: {e!s}")
                messagebox.showerror("Lỗi", f"Không thể tải model: {e!s}")

        thread = threading.Thread(target=load)
        thread.daemon = True
        thread.start()

    def select_image(self):
        """Chọn ảnh."""
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh", filetypes=[("Ảnh", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp"), ("Tất cả", "*.*")]
        )

        if file_path:
            self.load_image(file_path)

    def load_image(self, file_path):
        """Tải và hiển thị ảnh."""
        try:
            self.input_path = file_path

            # Load ảnh
            image = Image.open(file_path)

            # Resize để hiển thị
            display_image = image.copy()
            display_image.thumbnail((300, 300), Image.Resampling.LANCZOS)

            # Convert để hiển thị
            photo = ImageTk.PhotoImage(display_image)

            # Hiển thị
            self.input_image_label.config(image=photo, text="")
            self.input_image_label.image = photo

            # File info
            filename = os.path.basename(file_path)
            size = f"{image.size[0]}x{image.size[1]}"
            self.file_info_label.config(text=f"📄 {filename} ({size})")

            # Clear result
            self.result_image_label.config(image="", text="Chờ xử lý...")
            self.results_text.delete(1.0, tk.END)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải ảnh: {e!s}")

    def process_image(self):
        """Xử lý ảnh."""
        if not self.input_path:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ảnh trước!")
            return

        if not self.model:
            messagebox.showwarning("Cảnh báo", "Model chưa sẵn sàng!")
            return

        # Disable button
        self.process_btn.config(state="disabled", text="⏳ Đang xử lý...")

        # Process in background
        thread = threading.Thread(target=self.process_thread)
        thread.daemon = True
        thread.start()

    def process_thread(self):
        """Xử lý trong thread riêng."""
        try:
            # Get confidence
            confidence = self.conf_var.get() / 100.0

            # Run detection
            results = self.model(self.input_path, conf=confidence)

            # Update UI
            self.root.after(0, self.update_results, results)

        except Exception:
            self.root.after(0, lambda: messagebox.showerror("Lỗi", f"Lỗi xử lý: {e!s}"))
            self.root.after(0, lambda: self.process_btn.config(state="normal", text="🚀 Phát hiện"))

    def update_results(self, results):
        """Cập nhật kết quả."""
        try:
            # Get result image
            result_image = results[0].plot()

            # Convert to PIL
            import cv2
            from PIL import Image

            result_image = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)
            result_pil = Image.fromarray(result_image)

            # Resize for display
            result_pil.thumbnail((300, 300), Image.Resampling.LANCZOS)
            result_photo = ImageTk.PhotoImage(result_pil)

            # Display result
            self.result_image_label.config(image=result_photo, text="")
            self.result_image_label.image = result_photo

            # Update text
            self.results_text.delete(1.0, tk.END)

            result = results[0]
            if result.boxes is not None:
                self.results_text.insert(tk.END, f"📊 Phát hiện {len(result.boxes)} đối tượng:\n\n")

                for i, box in enumerate(result.boxes, 1):
                    class_id = int(box.cls[0])
                    class_name = self.model.names[class_id]
                    confidence = float(box.conf[0])
                    confidence_percent = confidence * 100

                    # Status icon
                    if confidence_percent >= 80:
                        status = "🟢 Rất cao"
                    elif confidence_percent >= 60:
                        status = "🟡 Cao"
                    elif confidence_percent >= 40:
                        status = "🟠 Trung bình"
                    else:
                        status = "🔴 Thấp"

                    self.results_text.insert(
                        tk.END, f"{i}. {class_name}\n   Độ tin cậy: {confidence_percent:.1f}% {status}\n\n"
                    )
            else:
                self.results_text.insert(tk.END, "❌ Không phát hiện đối tượng nào")

            # Re-enable button
            self.process_btn.config(state="normal", text="🚀 Phát hiện")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi hiển thị: {e!s}")
            self.process_btn.config(state="normal", text="🚀 Phát hiện")

    def save_result(self):
        """Lưu kết quả."""
        if not hasattr(self, "input_path") or not self.input_path:
            messagebox.showwarning("Cảnh báo", "Chưa có kết quả để lưu!")
            return

        try:
            # Get save path
            save_path = filedialog.asksaveasfilename(
                title="Lưu kết quả",
                defaultextension=".jpg",
                filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("Tất cả", "*.*")],
            )

            if save_path:
                # Run detection again and save
                results = self.model(self.input_path, conf=self.conf_var.get() / 100.0)
                results[0].save(save_path)
                messagebox.showinfo("Thành công", f"Đã lưu kết quả: {save_path}")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu: {e!s}")


def main():
    root = tk.Tk()
    SimpleYOLOGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
