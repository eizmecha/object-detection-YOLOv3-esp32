# Object Detection with YOLOv3 and ESP32

A real-time object detection system that uses YOLOv3 for detecting objects through an IP webcam stream and communicates detection results to an ESP32 microcontroller via MQTT protocol.

## 📋 Project Overview

This project combines computer vision with IoT to create a distributed object detection system:
- **Python Application**: Runs on a computer, performs real-time object detection using YOLOv3 on IP webcam feed
- **ESP32 Microcontroller**: Receives detection results via MQTT and can trigger physical actions
- **MQTT Communication**: Enables seamless communication between the detection system and IoT devices

## ✨ Features

- Real-time object detection using YOLOv3
- IP webcam integration for remote camera feed
- MQTT-based communication system
- ESP32 integration for IoT capabilities
- Support for 80+ COCO dataset object classes
- Configurable detection thresholds
- Cross-platform compatibility

## 🔗 References

- **YOLOv3 Official**: [https://pjreddie.com/darknet/yolo/](https://pjreddie.com/darknet/yolo/)
- **COCO Dataset Names**: [https://github.com/pjreddie/darknet/blob/master/data/coco.names](https://github.com/pjreddie/darknet/blob/master/data/coco.names)

## 🛠️ Hardware Requirements

- ESP32 development board
- Android/iOS device with IP Webcam app installed
- Computer/laptop with webcam capability
- Stable WiFi network

## 📦 Software Requirements

### Python Application Dependencies:
```bash
opencv-python>=4.5.0
numpy>=1.21.0
paho-mqtt>=1.6.0
```

### ESP32 Requirements:
- MicroPython firmware
- umqtt.simple library

### Mobile Application:
- IP Webcam (Available on Android/iOS app stores)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/eizmecha/object-detection-YOLOv3-esp32.git
cd object-detection-YOLOv3-esp32
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Download YOLO Model Files
Download the following files and place them in the project root directory:

1. **yolov3.weights**: Download from [YOLO official website](https://pjreddie.com/darknet/yolo/)

### 4. Configure ESP32
- Upload the MicroPython code to your ESP32 using Thonny IDE
- Update WiFi credentials in the ESP32 code
- Ensure proper MQTT broker configuration

## 🎯 Usage Instructions

### Step 1: Start IP Webcam Service
1. Open IP Webcam app on your mobile device
2. Click "Start server"
3. Note the IP address and port shown (e.g., `192.168.8.157:8080`)
4. Update the URL in `main.py` with your phone's IP address

### Step 2: Run Python Detection Script
```bash
python main.py
```

### Step 3: Deploy ESP32 Code
- Upload and run the MicroPython code on your ESP32
- The ESP32 will automatically connect to WiFi and MQTT broker

### Step 4: Monitor Results
- Object detection results will display on your computer screen
- Detection data will be sent to ESP32 via MQTT
- ESP32 will output received detections to do actions

## 📡 MQTT Configuration

### Topics Used:
- `camera/results` - Detailed JSON detection data
- `esp32/detections` - Simple text messages for ESP32
- `esp32/status` - ESP32 status updates

### Broker:
- Default: `broker.hivemq.com`
- Port: `1883`

## 📁 Project Structure

```
object-detection-YOLOv3-esp32/
├── main.py                 # Main Python detection application
├── esp32_Micropython_Thonny.py         # ESP32 MicroPython code
├── requirements.txt       # Python dependencies list
├── .gitignore            # Git exclusion rules
├── README.md             # Project documentation      
├── yolov3.cfg            # YOLOv3 network configuration
└── coco.names            # COCO dataset class names
```

## 🎨 Detection Capabilities

The system can detect 80+ object classes including:
- 👥 People and animals (cats, dogs, birds, etc.)
- 🚗 Vehicles (cars, trucks, buses, motorcycles)
- 🏠 Everyday objects (chairs, tables, phones, laptops)
- 🍎 Food items (bananas, apples, bottles)
- 🏢 Infrastructure (traffic lights, stop signs, buildings)

## ⚙️ Customization

### Adjust Detection Sensitivity:
```python
confThreshold = 0.5  # Confidence threshold (0-1)
nmsThreshold = 0.3   # Non-maximum suppression threshold
```

### Add ESP32 Actions:
```python
def mqtt_callback(topic, msg):
    message = msg.decode()
    if "person" in message.lower():
        # Add custom actions like LED control, buzzer, etc.
        print("Person detected - activating security protocol!")
```

## 📊 Performance Notes

- **Frame Rate**: ~3-5 FPS on average hardware
- **Detection Accuracy**: High for most COCO classes
- **Latency**: <2 seconds end-to-end detection to ESP32
- **Network**: Requires stable WiFi connection

## 👨‍💻 Author

- **Eiz Mecha** 
- GitHub: [@eizmecha](https://github.com/eizmecha)
- Email: alazy555yemen@gmail.com

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ❓ Support

For questions or issues:
1. Check existing GitHub issues
2. Create a new issue with detailed description
3. Contact: alazy555yemen@gmail.com

