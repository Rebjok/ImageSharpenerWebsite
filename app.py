from flask import Flask, render_template, url_for, redirect, send_from_directory
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
import requests

#Configuring app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hajlghkanie'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

#Creating Form Class
class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only Images are allowed'),
            FileRequired("File field should not be empty")
        ]
    )
    submit = SubmitField('Upload')

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

@app.route('/', methods=['GET', 'POST'])
def home():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)

        ##API fpr DeepLearnAPI for control comparison
        # r = requests.post(
        #     "https://api.deepai.org/api/torch-srgan",
        #     files={
        #         'image': open(file_url, 'rb'),
        #     },
        #     headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
        # )
        # print(r.json())
    else:
        file_url=None
    return render_template('index.html', form=form, file_url=file_url)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)

