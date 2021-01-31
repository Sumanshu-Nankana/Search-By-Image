from flask import Flask, render_template, request, flash, url_for, redirect
import os
from werkzeug.utils import secure_filename
from utils import *

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


app = Flask(__name__)
app.config['UPLOAD_PATH'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'my_secret_key'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def delete_images():
    for img in os.listdir(app.config['UPLOAD_PATH']):
        path = app.config['UPLOAD_PATH'] + img
        os.remove(path)

@app.route('/')
def search_by_image_home():
    filename = ''
    matched_images = []
    all_cosine_distance = []
    range_value = 0
    # Deleting the Images which already get uploaded in uploads
    delete_images()
    return render_template('search_by_image.html', 
                            filename=filename, 
                            count=int(range_value),
                            result=matched_images,
                            distance=all_cosine_distance[:int(range_value)])

@app.route('/upload_and_search', methods=['GET','POST'])
def upload_and_search():
    filename = ''
    matched_images = []
    all_cosine_distance = []
    range_value = 0
    # Deleting the Images which already get uploaded in uploads
    delete_images()
    if request.method == 'POST':
        # Return File Object
        file = request.files['filename']  
        range_value = request.form['rangeValue1']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            input_image_path = os.path.join(app.config['UPLOAD_PATH'], filename)
            input_image_features = get_input_image_features(input_image_path)
            all_cosine_distance = calculate_cosine_distance_with_all_DB_images(input_image_features, all_images_features)
            for i in all_cosine_distance[:int(range_value)]:
                path = os.path.join('/static/Images/', all_images_names[i[1]])
                matched_images.append(path)
            return render_template('search_by_image.html', 
                                    filename=filename, 
                                    count=int(range_value),
                                    result=matched_images,
                                    distance=all_cosine_distance[1:int(range_value)+1])
        else:
            extension = file.filename.split('.')[-1].upper()
            msg = extension + " - File Extension not allowed"
            flash(msg)
            return render_template('search_by_image.html', 
                                    filename=filename, 
                                    count=int(range_value),
                                    result=matched_images,
                                    distance=all_cosine_distance[:int(range_value)])
    else:
        return render_template('search_by_image.html', 
                                filename=filename, 
                                count=int(range_value),
                                result=matched_images,
                                distance=all_cosine_distance[:int(range_value)])
if __name__ == "__main__":
    app.run(debug=True, port=5001, threaded=False)