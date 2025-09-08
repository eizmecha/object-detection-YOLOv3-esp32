import cv2
import numpy as np
import urllib.request
import time
import paho.mqtt.client as mqtt
import json

# MQTT Configuration
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "camera/results"
MQTT_CLIENT_ID = "object-detector-pc"

# IP Webcam URL
url = 'http://192.168.8.157:8080/shot.jpg'

# YOLO Configuration
whT = 320
confThreshold = 0.5
nmsThreshold = 0.3
classesfile = 'coco.names'
classNames = []
with open(classesfile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

modelConfig = 'yolov3.cfg'
modelWeights = 'yolov3.weights'
net = cv2.dnn.readNetFromDarknet(modelConfig, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# MQTT Client setup with callback API version
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, MQTT_CLIENT_ID)
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
print(f"Connected to MQTT broker: {MQTT_BROKER}")

def findObjects(outputs, im):
    hT, wT, cT = im.shape
    bbox = []
    classIds = []
    confs = []
    detected_objects = []
    
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                w, h = int(det[2] * wT), int(det[3] * hT)
                x, y = int((det[0] * wT) - w/2), int((det[1] * hT) - h/2)
                bbox.append([x, y, w, h])
                classIds.append(classId)
                confs.append(float(confidence))
    
    indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)
    
    if len(indices) > 0:
        for i in indices.flatten():
            box = bbox[i]
            x, y, w, h = box[0], box[1], box[2], box[3]
            object_name = classNames[classIds[i]]
            confidence = confs[i]
            
            detected_objects.append({
                "name": object_name,
                "confidence": float(confidence),
                "bbox": [x, y, w, h]
            })
            
            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 255), 2)
            cv2.putText(im, f'{object_name.upper()} {int(confidence * 100)}%', 
                       (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
    
    return detected_objects

def send_detection_mqtt(detected_objects):
    if detected_objects:
        # Create message with all detected objects
        message = {
            "timestamp": time.time(),
            "detections": detected_objects,
            "count": len(detected_objects)
        }
        
        # Send via MQTT
        mqtt_client.publish(MQTT_TOPIC, json.dumps(message))
        print(f"Sent MQTT message: {len(detected_objects)} objects detected")
        
        # Also send simple text message for ESP32
        object_names = [obj["name"] for obj in detected_objects]
        simple_message = f"Detected: {', '.join(object_names)}"
        mqtt_client.publish("esp32/detections", simple_message)
        print(f"Simple message: {simple_message}")

print("Starting object detection with MQTT...")
print("Press 'q' to quit")

detection_interval = 2  # Send detection every 2 seconds
last_detection_time = 0

while True:
    try:
        # Get image from IP webcam
        img_resp = urllib.request.urlopen(url, timeout=3)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        im = cv2.imdecode(imgnp, -1)
        
        if im is None:
            print("Failed to decode image")
            time.sleep(1)
            continue
        
        # Process with YOLO
        blob = cv2.dnn.blobFromImage(im, 1/255, (whT, whT), [0, 0, 0], 1, crop=False)
        net.setInput(blob)
        
        layernames = net.getLayerNames()
        outputNames = [layernames[i - 1] for i in net.getUnconnectedOutLayers()]
        
        outputs = net.forward(outputNames)
        
        detected_objects = findObjects(outputs, im)
        
        # Send detection via MQTT at intervals
        current_time = time.time()
        if current_time - last_detection_time >= detection_interval and detected_objects:
            send_detection_mqtt(detected_objects)
            last_detection_time = current_time
        
        # Display status
        status_text = f"Objects: {len(detected_objects)}"
        cv2.putText(im, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow('Object Detection', im)
        
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
            
    except urllib.error.URLError as e:
        print(f"Connection error: {e}")
        time.sleep(2)
        
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)

mqtt_client.disconnect()
cv2.destroyAllWindows()