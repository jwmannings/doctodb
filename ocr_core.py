try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import os
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

input_folder = './input'
output_folder = './output'
allowed_files = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_files

def ocr_core(filename):
    print('FULENAME: ',filename)
    text = pytesseract.image_to_pdf_or_hocr(Image.open('{dir}/{name}'.format(name=filename,dir=input_folder)), extension='pdf')
    f = open('{dir}/{name}.pdf'.format(name=filename.rsplit('.', 1)[0].lower(), dir=output_folder), 'w+b')
    f.write(bytearray(text))
    f.close()
    return 1  # Then we will print the text in the image

for filename in os.listdir(input_folder):
    if filename and allowed_file(filename):
        out = ocr_core(filename)
        if out == 1:
            print('Processed: ',filename)
        else:
            print('Process issue with: ',filename)
    else:
        print('Could not process: ',filename)
