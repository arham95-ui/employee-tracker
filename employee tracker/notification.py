import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime

class EmailNotification:
    def __init__(self, sender_email, sender_password, admin_email):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.admin_email = admin_email
    
    def send_alert(self, employee_name, photo_path=None):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.admin_email
            msg['Subject'] = f"⚠️ EMPLOYEE ALERT: {employee_name} not working!"
            
            body = f"""
            <h2 style="color:red;">⚠️ Employee Inactivity Alert</h2>
            <p><strong>Employee:</strong> {employee_name}</p>
            <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Status:</strong> Employee not working for 15+ seconds</p>
            <p><strong>Action Taken:</strong> Photo captured</p>
            <p><em>This is an automated alert from Employee Tracking System</em></p>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            if photo_path and os.path.exists(photo_path):
                with open(photo_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename={os.path.basename(photo_path)}'
                    )
                    msg.attach(part)
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            
            print("✅ Email sent to admin successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Email send nahi ho paaya: {e}")
            return False