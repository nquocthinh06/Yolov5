# YOLOv5 Traffic Sign Detection 🚦

Vietnamese traffic sign detection system using YOLOv5 object detection framework.

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-1.9%2B-red.svg)](https://pytorch.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![GitHub stars](https://img.shields.io/github/stars/nquocthinh06/Yolov5.svg?style=social&label=Star)](https://github.com/nquocthinh06/Yolov5)

## 📋 Mục lục

- [Tính năng](#tính-năng)
- [Cài đặt](#cài-đặt)
- [Cách sử dụng](#cách-sử-dụng)
- [Training](#training)
- [Kết quả](#kết-quả)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [Tài liệu tham khảo](#tài-liệu-tham-khảo)

## ✨ Tính năng

- ✅ Real-time Vietnamese traffic sign detection
- ✅ Support multiple model sizes (nano, small, medium, large, xlarge)
- ✅ GPU acceleration with CUDA
- ✅ Batch processing & video inference
- ✅ Model export (ONNX, TensorRT, CoreML)
- ✅ Easy-to-use API
- ✅ Docker support

## 🔧 Cài đặt

### Yêu cầu hệ thống

- **Python:** 3.8 hoặc cao hơn
- **OS:** Windows, Linux, macOS
- **GPU:** NVIDIA CUDA 11.0+ (tùy chọn, để tăng tốc độ)
- **RAM:** Tối thiểu 4GB (8GB+ khuyến nghị)

### Setup nhanh

#### 1. Clone repository

```bash
git clone https://github.com/nquocthinh06/Yolov5.git
cd Yolov5
```

#### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

#### 3. Download pre-trained weights (tùy chọn)

```bash
wget https://github.com/ultralytics/yolov5/releases/download/v6.2/yolov5s.pt
```

## 🚀 Cách sử dụng

### Inference trên ảnh

```bash
python detect.py \
  --source path/to/image.jpg \
  --weights yolov5s.pt \
  --conf 0.5 \
  --iou 0.45
```

### Inference trên video

```bash
python detect.py \
  --source path/to/video.mp4 \
  --weights yolov5s.pt \
  --conf 0.5 \
  --device 0
```

### Inference từ webcam

```bash
python detect.py \
  --source 0 \
  --weights yolov5s.pt \
  --conf 0.5
```

### GUI Demo

```bash
python scripts/gui_inference.py
```

## 🎯 Training

### Chuẩn bị dữ liệu

Dataset phải có cấu trúc:

```
datasets/traffic_signs_vietnam/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
└── labels/
    ├── train/
    ├── val/
    └── test/
```

### Training custom model

```bash
python train_custom.py \
  --data data/traffic_signs_vietnam.yaml \
  --epochs 100 \
  --img 640 \
  --batch 16 \
  --weights yolov5s.pt \
  --device 0
```

### Training options

```
--epochs       : Số epoch training (default: 100)
--img          : Kích thước ảnh input (default: 640)
--batch        : Batch size (default: 16)
--weights      : Pre-trained weights file
--device       : GPU device index, 0 cho GPU đầu tiên
--save-dir     : Thư mục lưu kết quả (default: results/)
```

## 📊 Validation

```bash
python val.py \
  --data data/traffic_signs_vietnam.yaml \
  --weights results/models/best.pt \
  --img 640
```

## 📦 Export Model

### Export sang ONNX

```bash
python export.py \
  --weights results/models/best.pt \
  --include onnx
```

### Export sang TensorRT (GPU)

```bash
python export.py \
  --weights results/models/best.pt \
  --include engine
--device 0
```

Hỗ trợ các format:

- TorchScript (.pt)
- ONNX (.onnx)
- TensorRT (.engine)
- CoreML (.mlmodel)
- TensorFlow SavedModel (.pb)

## 📁 Cấu trúc thư mục

```
yolov5-traffic-detection/
├── data/                       # Dataset configs
│   ├── traffic_signs_vietnam/
│   ├── hyps/                   # Hyperparameters
│   └── *.yaml
├── datasets/                   # Training datasets
│   └── traffic_signs_vietnam/
├── docs/                       # Documentation
├── models/                     # Model architectures
│   ├── hub/
│   ├── segment/
│   └── *.yaml
├── results/                    # Output results
│   ├── models/                 # Trained models
│   └── predictions/            # Detection results
├── scripts/                    # Utility scripts
│   ├── gui_inference.py        # GUI Demo
│   ├── create_demo_video.py
│   └── ...
├── utils/                      # Utilities
├── detect.py                   # Detection script
├── train_custom.py             # Training script
├── val.py                      # Validation script
├── export.py                   # Export model
├── requirements.txt            # Dependencies
├── README.md                   # This file
└── LICENSE                     # License
```

## 📈 Kết quả

Mô hình đạt được:

- **Accuracy:** ~95% trên test set
- **Speed:** Real-time inference (30+ FPS on GPU)
- **Model size:** 14MB (YOLOv5s)

Chi tiết kết quả xem trong `results/metrics/`

## 🐳 Docker Support

### Build Docker image

```bash
docker build -t yolov5-traffic .
```

### Run with Docker

```bash
docker run --gpus all -it yolov5-traffic python detect.py --source 0
```

## 📚 Tài liệu tham khảo

- [YOLOv5 Official Docs](https://docs.ultralytics.com/yolov5/)
- [Ultralytics GitHub](https://github.com/ultralytics/yolov5)
- [YOLOv5 Paper](https://arxiv.org/abs/2004.10934)

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

Project này được cấp phép dưới GPL v3 License - xem file [LICENSE](LICENSE) để chi tiết.

## 👤 Tác giả

- **Nguyen Quo Thinh** - [@nquocthinh06](https://github.com/nquocthinh06)

## ⚠️ Disclaimer

Mô hình này được phát triển cho mục đích nghiên cứu và giáo dục. Hiệu suất trong các tình huống thực tế có thể khác nhau.

## 🙏 Cảm ơn

- [Ultralytics](https://www.ultralytics.com/) - cho YOLOv5 framework
- [PyTorch](https://pytorch.org/) - cho deep learning framework

---

**Mời bạn ⭐ star repository nếu nó hữu ích cho bạn!**

## 📞 Liên hệ

- Email: nquocthinh06@gmail.com
- GitHub: [@nquocthinh06](https://github.com/nquocthinh06)

Last updated: 2025-01-11
