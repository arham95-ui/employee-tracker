import cv2
import os
import time
from datetime import datetime

class CameraModule:
    def __init__(self, save_path="captured_photos/"):
        self.save_path = save_path
        if not os.path.exists(save_path):
            os.makedirs(save_path)
    
    def capture_photo(self, employee_name="employee"):
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Camera open nahi ho rahi!")
                return None
            
            time.sleep(0.5)
            
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                print("Photo capture nahi ho paayi!")
                return None
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{employee_name}_{timestamp}.jpg"
            filepath = os.path.join(self.save_path, filename)
            
            cv2.imwrite(filepath, frame)
            print(f"Photo saved: {filepath}")
            
            return filepath
            
        except Exception as e:
            print(f"Camera error: {e}")
            return None