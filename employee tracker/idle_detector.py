from pynput import keyboard, mouse
import time

class IdleDetector:
    def __init__(self):
        self.last_activity_time = time.time()
        self.listener_started = False
        
    def start_listeners(self):
        self.keyboard_listener = keyboard.Listener(on_press=self.on_activity)
        self.keyboard_listener.start()
        
        self.mouse_listener = mouse.Listener(on_move=self.on_activity, 
                                            on_click=self.on_activity,
                                            on_scroll=self.on_activity)
        self.mouse_listener.start()
        self.listener_started = True
    
    def on_activity(self, *args, **kwargs):
        self.last_activity_time = time.time()
    
    def get_idle_time(self):
        return time.time() - self.last_activity_time
    
    def stop_listeners(self):
        if self.listener_started:
            self.keyboard_listener.stop()
            self.mouse_listener.stop()
            self.listener_started = False