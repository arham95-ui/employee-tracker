import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--windowed',
    '--name=EmployeeTracker',
    '--add-data=config.json;.',
    '--hidden-import=pynput',
    '--hidden-import=cv2',
    '--hidden-import=PIL',
])

print("✅ EXE created successfully!")
print("📁 Check 'dist' folder for EmployeeTracker.exe")