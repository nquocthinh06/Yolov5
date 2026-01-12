# 🚀 YOLOv5 Traffic Detection - Web Interface Guide

## 📊 Dashboard Overview

Professional web-based dashboard for managing the complete YOLOv5 traffic sign detection system. Built with Streamlit for an interactive and user-friendly experience.

## ✨ Features

### 1️⃣ **Detect & Surveillance** 🎯

Real-time traffic sign detection with visualization

**Capabilities:**

- 📤 Upload image or video files
- 📹 Webcam real-time detection
- ⚙️ Adjustable confidence threshold (0.0-1.0)
- ⚙️ Adjustable IoU threshold for NMS (0.0-1.0)
- 📊 Live detection statistics
- 💾 Save detection results
- 📋 Results table with details (class, confidence, coordinates)

**How to Use:**

1. Select "📤 Upload File" or "📹 Use Webcam"
2. Upload your image/video
3. Adjust confidence and IoU thresholds
4. Click "🚀 Run Surveillance"
5. View results in the preview and statistics

### 2️⃣ **Train Model** 🎓

Complete model training interface with logging and monitoring

**Configuration Options:**

- 📁 Dataset YAML file upload
- ⚖️ Initial weights (optional)
- 🔢 Training parameters:
  - Epochs (10-500)
  - Batch size (1-256)
  - Image size (320-1280)
- 🎯 Advanced settings:
  - Optimizer selection (SGD, Adam, AdamW)
  - Learning rate configuration
  - Momentum settings
  - Weight decay

**Monitoring:**

- 📈 Real-time epoch progress
- 📊 Loss tracking
- 🎯 mAP50 and mAP50-95 metrics
- 📝 Live training logs
- 📉 Interactive training progress charts

**How to Use:**

1. Upload dataset YAML file (e.g., `data/traffic_signs_vietnam.yaml`)
2. Configure training parameters
3. Set advanced hyperparameters (optional)
4. Click "▶️ Start Training"
5. Monitor progress in logs and metrics
6. Click "⏹️ Stop Training" to halt

### 3️⃣ **Validate AID** ✅

Algorithm performance comparison and validation

**Features:**

- ⚙️ Configure Performance Index (PI) weights
- 🔍 Compare different AID algorithms
- 📊 Performance metrics:
  - Detection Rate (DR %)
  - False Alarm Rate (FAR %)
  - Mean Time To Detect (MTTD)
  - Performance Index (PI)
- 📈 Validation accuracy metrics:
  - Precision, Recall, F1-Score
  - Overall Accuracy

**Algorithms Compared:**

- AID1-AID7 with detailed performance comparison
- Automatic highlighting of best performer
- Customizable weight parameters

**How to Use:**

1. Adjust DR, FAR, and MTTD weights
2. Review algorithm comparison table
3. Check validation metrics
4. Identify best performing algorithm

### 4️⃣ **Export Model** 📦

Multi-format model export for deployment

**Export Formats:**

- ✅ ONNX (.onnx) - Cross-platform compatibility
- TorchScript (.torchscript) - PyTorch native
- TensorRT (.engine) - GPU-optimized inference
- CoreML (.mlmodel) - iOS/macOS deployment
- TensorFlow Lite (.tflite) - Mobile deployment

**Configuration:**

- Device selection (CPU/GPU)
- Half precision option (FP16)
- Inference optimization
- Format comparison table with:
  - File size
  - Inference speed (FPS)
  - Platform compatibility

**How to Use:**

1. Upload model weights (.pt file)
2. Select target device
3. Choose export formats
4. Click "📦 Export Model"
5. Download exported models

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Install Streamlit and dependencies:**

```bash
pip install streamlit plotly pillow pandas torch torchvision
```

2. **Run the application:**

```bash
streamlit run app_web.py
```

3. **Access in browser:**

```
http://localhost:8501
```

---

## 🎨 UI Design Details

### Color Scheme

- **Primary Background:** #121212 (Dark)
- **Secondary Background:** #1e1e1e (Darker)
- **Card Background:** #2d2d2d
- **Primary Blue:** #3b82f6
- **Primary Blue Dark:** #2563eb
- **Text Primary:** #ffffff (White)
- **Text Secondary:** #9ca3af (Gray)
- **Border:** #3e3e3e

### Design Features

- 📱 Responsive layout with two-column design
- 🎯 Sidebar navigation for module selection
- 📊 Metric cards with delta indicators
- 📈 Interactive Plotly charts
- 🎨 Dark theme with blue accents
- ⚡ Smooth animations and transitions
- 🌊 Gradient backgrounds

### Layout Structure

```
┌─────────────────────────────────────────┐
│         YOLOv5 Traffic Detection        │
├─────────────┬─────────────────────────────┤
│             │                             │
│  SIDEBAR    │     MAIN CONTENT            │
│             │                             │
│ • Navigation│  • Module specific UI       │
│ • Model Info│  • Input controls           │
│ • Status    │  • Results/Metrics          │
│ • Tabs      │  • Visualizations           │
│             │  • Action buttons           │
│             │                             │
└─────────────┴─────────────────────────────┘
```

---

## 📊 Key Sections Explained

### Dashboard Components

**1. Input & Controls (Left Column)**

- File upload widgets
- Parameter sliders
- Configuration inputs
- Action buttons

**2. Preview & Results (Right Column)**

- Image/video preview area
- Live statistics display
- Results visualization
- Metric cards

**3. Sidebar**

- Navigation between modules
- Model information metrics
- System status
- Quick access shortcuts

---

## 💡 Usage Tips

### Detection Best Practices

- Use **confidence 0.5** for balanced precision/recall
- Lower confidence (0.3-0.4) for improved recall
- Higher confidence (0.6-0.7) for improved precision
- IoU of **0.45** is standard for NMS

### Training Tips

- Start with **100 epochs** for quick tests
- Use **batch 16** for typical GPU (8GB VRAM)
- Reduce batch if running out of memory
- Monitor loss and mAP50 curves
- Stop if metrics plateau

### Validation Tips

- Always validate after training
- Check if precision/recall are balanced
- Compare with baseline models
- Use confusion matrix for error analysis

### Export Tips

- Export to **ONNX** for cross-platform use
- Export to **TensorRT** for GPU deployment
- Export to **TFLite** for mobile apps
- Test exported model before deployment

---

## 🔧 Troubleshooting

### Port Already in Use

```bash
streamlit run app_web.py --server.port 8502
```

### Slow Performance

- Reduce image size in training
- Use smaller batch size
- Enable GPU if available
- Reduce model size (use yolov5n instead of yolov5x)

### Out of Memory

- Reduce batch size
- Use lower resolution images
- Use smaller model variant
- Enable FP16 precision

### File Upload Issues

- Check file format (JPG, PNG, MP4, AVI)
- Verify file size < 200MB
- Ensure file is valid/not corrupted

---

## 📝 Configuration Files

### Required Files

```
data/traffic_signs_vietnam.yaml     # Dataset config
datasets/traffic_signs_vietnam/     # Training data
models/*.yaml                       # Model architectures
yolov5s.pt                         # Pre-trained weights
```

### Generated Files

```
results/models/best.pt             # Best trained model
results/predictions/               # Detection results
runs/train/exp*/                   # Training logs
```

---

## 🌐 API Integration (Future)

The web interface can be extended with:

- REST API endpoints
- WebSocket for real-time updates
- Database integration
- User authentication
- Advanced analytics

---

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [YOLOv5 Docs](https://docs.ultralytics.com/yolov5/)
- [Plotly Charting](https://plotly.com/python/)
- [Project Documentation](docs/COMPLETE_PROJECT_DOCUMENTATION.md)

---

## 🎯 Future Enhancements

- ✨ Real-time video streaming
- 📊 Advanced analytics dashboard
- 🗄️ Database integration
- 👥 Multi-user support
- 🔐 Authentication system
- 📱 Mobile responsive design
- 🚀 Cloud deployment

---

## 📞 Support

For issues or questions:

1. Check troubleshooting section
2. Review COMPLETE_PROJECT_DOCUMENTATION.md
3. Check GitHub issues
4. Contact development team

---

**Version:** 1.0.0  
**Last Updated:** 2025-01-11  
**Status:** ✅ Production Ready

🚀 **Happy Detecting!**
