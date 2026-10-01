import tkinter as tk

class WarningPopup:
    def __init__(self):
        self.root = None
        self.popup_shown = False
        self.ok_pressed = False
        self.timeout_callback = None
        self.on_ok_callback = None
        self.timer_id = None
        self.is_closing = False
        self.timeout_seconds = 8
        self.time_left = 8
    
    def show_warning(self, on_timeout=None, on_ok=None):
        """Show warning popup with callbacks"""
        if self.popup_shown:
            return
        
        self.popup_shown = True
        self.ok_pressed = False
        self.timeout_callback = on_timeout
        self.on_ok_callback = on_ok
        self.time_left = self.timeout_seconds
        self.is_closing = False
        
        # Root window
        self.root = tk.Tk()
        self.root.title("⚠️ WARNING")
        self.root.geometry("500x280")
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#FF4444')
        
        # Warning icon and message
        label = tk.Label(
            self.root,
            text="⚠️ PLZ DOING YOUR WORK!\n\nAap 10 seconds se kaam nahi kar rahe!\nPress OK to continue working.\n\n⏱️ 8 seconds timeout",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#FF4444",
            wraplength=450
        )
        label.pack(expand=True, fill='both', padx=20, pady=15)
        
        # Timer label
        self.timer_label = tk.Label(
            self.root,
            text="⏱️ 8 seconds remaining",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#FF4444"
        )
        self.timer_label.pack(pady=5)
        
        # OK button
        self.ok_button = tk.Button(
            self.root,
            text="✅ OK, I'm working",
            font=("Arial", 13, "bold"),
            command=self.on_ok_pressed,
            bg="white",
            fg="#FF4444",
            padx=25,
            pady=12,
            width=22
        )
        self.ok_button.pack(pady=15)
        
        # Info label
        info = tk.Label(
            self.root,
            text="⚠️ System will shutdown after timeout or OK press",
            font=("Arial", 10),
            fg="#FFDDDD",
            bg="#FF4444"
        )
        info.pack(pady=5)
        
        # Start timer
        self.update_timer()
        
        # Main loop
        self.root.mainloop()
    
    def update_timer(self):
        """Update timer every second"""
        if self.is_closing or not self.root or self.ok_pressed:
            return
        
        if self.time_left > 0:
            self.timer_label.config(text=f"⏱️ {self.time_left} seconds remaining")
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            # Timeout - No OK pressed
            self.timer_label.config(text="⏱️ 0 seconds - Taking photo...")
            print("⏰ Timer expired! No OK pressed...")
            if self.timeout_callback:
                self.timeout_callback()
            self.close_popup()
    
    def on_ok_pressed(self):
        """OK button pressed"""
        if self.is_closing:
            return
        
        self.ok_pressed = True
        print("✅ User pressed OK")
        
        # Call OK callback
        if self.on_ok_callback:
            self.on_ok_callback()
        
        self.close_popup()
    
    def close_popup(self):
        """Close popup"""
        if self.is_closing:
            return
        
        self.is_closing = True
        self.popup_shown = False
        
        try:
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None
            
            if self.root:
                self.root.quit()
                self.root.destroy()
                self.root = None
                
        except Exception as e:
            print(f"Popup close error: {e}")
            self.root = None