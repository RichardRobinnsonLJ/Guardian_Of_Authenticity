from img_header import img_with_feature
from vid_header import video_with_feature 
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import shutil

app = Flask(__name__)

# Specify the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check if the file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for rendering the image input page
@app.route('/image_input')
def image_input():
    return render_template('img_page.html')  

# Route for rendering the video input page
@app.route('/video_input')
def video_input():
    return render_template('video_page.html')

# Route for handling image upload and displaying the result
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        destination_path = os.path.join('static', 'uploads', filename)
        shutil.copy(file_path, destination_path)
        result = img_with_feature(file_path)
        os.remove(file_path)

        return render_template('result.html', filename=filename, result=result)

    return redirect(request.url)

# Route for handling video upload and displaying the result
@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(video_path)
        destination_path = os.path.join('static', 'uploads', filename)
        shutil.copy(video_path, destination_path)
        result = video_with_feature(video_path)  # Perform video detection
        os.remove(video_path)
        return render_template('video_result.html', filename=filename, result=result)

    return redirect(request.url)


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)