# doctodb

# To setup
- Install tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
- pip3 install pytesseract
- pip3 install xmltodict

# To run
### to run application:
python3 app.py
Navigate too http://127.0.0.1:5000/upload
Use the upload button to upload the file

### to run standalone from files
place files that you want to process in the 'input' folder
python3 ocr_core.py
take the processed files from the 'output' folder
