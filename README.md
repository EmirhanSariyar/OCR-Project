## OCR Project - Image to Text Desktop Application
This project is a Python desktop application that allows users to select an image from their computer and extract the text within the image.
It uses OCR (Optical Character Recognition) technology to read the text and presents it to the user in an editable format.

---
 
## Features 
- Image selection interface
- Convert text in selected image to editable text using OCR
- Tools like Copy, Save As, Clear Text, Font Size Adjustment, and Theme Switching
- Whitespace and indentation sensitivity (suitable for code blocks)
- Support for Dark and Light themes

---

## Requirements
- Python 3.10 or higher.
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (must be installed seperately on the computer)  
- Required Python Packages:
```bash
pip install -r requirements.txt
```

---

## How to Build the Application

To convert the Python script into a standalone executable file (.exe) for Windows, you can use PyInstaller.

Make sure PyInstaller is installed in your Python environment:
pip install pyinstaller

Run the following command in your project directory to create a single executable without a console window:
pyinstaller --noconfirm --onefile --windowed ocr.py

After the process completes, find the executable file inside the dist folder. You can distribute this .exe to run the app on Windows machines without requiring Python.
