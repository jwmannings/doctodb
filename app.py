try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import os
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
from flask import Flask, render_template, request
from flask import jsonify
import xmltodict, json
from flask import send_file, current_app

UPLOAD_FOLDER = '/static/uploads/'
output_folder = './static/output'
allowed_files = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

def ocr_core(filename):
    text = pytesseract.image_to_pdf_or_hocr(Image.open(filename), extension='pdf')
    f = open('{dir}/{name}.pdf'.format(name=filename.filename.rsplit('.', 1)[0].lower(), dir=output_folder), 'w+b')
    f.write(bytearray(text))
    f.close()
    return

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_files


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):
            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))

            # call the OCR function on it
            extracted_text = ocr_core(file)
            #extracted_text = json.dumps(extracted_text)

            # extract the text and display it
            static_file = open('{dir}/{name}.pdf'.format(name=file.filename.rsplit('.', 1)[0].lower(), dir=output_folder), 'rb')
            print('hit return statement')
            return send_file(
                    static_file,
                    'application/pdf',
                    as_attachment=True,
                    attachment_filename='{name}.pdf'.format(name=file.filename.rsplit('.', 1)[0].lower())
                )
                #return send_file(static_file, attachment_filename='file.pdf')
            #return render_template('upload.html',
                                   #msg='Successfully processed',
                                   #extracted_text=jsonify(extracted_text),
                                   #img_src=UPLOAD_FOLDER + file.filename)
    elif request.method == 'GET':
        return render_template('upload.html')

@app.route('/show/static-pdf/')
def show_static_pdf():
    with open('/path/of/file.pdf', 'rb') as static_file:
        return send_file(static_file, attachment_filename='file.pdf')

@app.route('/upload_api', methods=['GET', 'POST'])
def upload_api():
    if request.method == 'POST':
        # call the OCR function on it
        extracted_text = ocr_core('images/example_1.PNG')
        extracted_text = xmltodict.parse(extracted_text)
        #extracted_text = json.dumps(extracted_text)

        # extract the text and display it
        return jsonify(extracted_text)

    elif request.method == 'GET':
        return '404'

if __name__ == '__main__':
    app.run()
