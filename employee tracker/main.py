import time
import json
import sys
from idle_detector import IdleDetector
from popup_warning import WarningPopup
from camera_module import CameraModule
from notification import EmailNotification
from database import Database

class EmployeeTracker:
    def __init__(self, config_file="config.json"):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.idle_detector = IdleDetector()
        self.warning = WarningPopup()
        self.camera = CameraModule(self.config['photo_save_path'])
        self.notifier = EmailNotification(
            self.config['sender_email'],
            self.config['sender_password'],
            self.config['admin_email']
        )
        self.db = Database(self.config['log_db'])
        
        self.warning_time = self.config['idle_time_warning']  # 10 sec
        self.employee_name = "Employee"
        
        self.warning_shown = False
        self.is_running = True
        self.system_should_exit = False  # System band hone ke liye
        
        print("🚀 Employee Tracking System Started!")
        print(f"⚠️ Warning after: {self.warning_time}s")
        print(f"⏱️ 8 sec wait after warning for OK button")
        print("----------------------------------------")
        print("💡 Press Ctrl+C to stop")
        print("")
    
    def on_warning_timeout(self):
        """Called when 8 seconds timeout - Take photo and exit"""
        print("⏰ 8 seconds passed - Worker did NOT press OK!")
        print("📸 Capturing photo...")
        
        # Photo capture
        photo_path = self.camera.capture_photo(self.employee_name)
        
        if photo_path:
            print("📧 Sending email to admin...")
            self.notifier.send_alert(self.employee_name, photo_path)
            self.db.log_event(
                self.employee_name,
                "CAPTURE_TIMEOUT",
                photo_path,
                "No response to warning for 8 seconds"
            )
            print("✅ Photo captured and sent to admin!")
        else:
            print("❌ Photo capture failed!")
            self.notifier.send_alert(self.employee_name, None)
        
        # System band karo
        self.system_should_exit = True
        self.is_running = False
        print("🛑 System shutting down...")
    
    def on_ok_pressed(self):
        """Called when user presses OK - Just exit"""
        print("✅ Worker pressed OK - Working normally")
        self.db.log_event(
            self.employee_name,
            "WARNING_OK",
            status="User pressed OK"
        )
        
        # System band karo
        self.system_should_exit = True
        self.is_running = False
        print("🛑 System shutting down...")
    
    def run(self):
        self.idle_detector.start_listeners()
        
        try:
            while self.is_running:
                idle_time = self.idle_detector.get_idle_time()
                
                # 1. 10 seconds idle - Show warning
                if idle_time >= self.warning_time and not self.warning_shown:
                    print(f"⚠️ {idle_time:.1f}s - Showing warning...")
                    self.warning_shown = True
                    
                    # Warning show karein - callbacks pass karein
                    self.warning.show_warning(
                        on_timeout=self.on_warning_timeout,
                        on_ok=self.on_ok_pressed
                    )
                    
                    # Warning ke baad system exit ho jana chahiye
                    # (callback already sets is_running = False)
                    break
                
                time.sleep(0.3)
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping tracker...")
        finally:
            self.cleanup()
            # System exit
            print("👋 Goodbye!")
            sys.exit(0)
    
    def cleanup(self):
        self.idle_detector.stop_listeners()
        self.db.close()
        if self.warning.root:
            try:
                self.warning.close_popup()
            except:
                pass
        print("✅ Cleanup complete")

if __name__ == "__main__":
    tracker = EmployeeTracker()
    tracker.run()