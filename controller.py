from model import InputForm
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
from compute import compute
import sys
import colorbynumbers.colorbynumbers as cbn
import os


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

WTF_CSRF_SECRET_KEY = 'a random string'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

try:
    template_name = sys.argv[1]
except IndexError:
    template_name = 'view_plain'

if template_name == 'view_flask_bootstrap':
    from flask_bootstrap import Bootstrap
    Bootstrap(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/mnz', methods=['GET', 'POST'])
def index():
    # img_path = None
    # if request.method == 'POST':
    #     file = request.files['file']
    #     if file and allowed_file(file.filename):
    #         filename = secure_filename(file.filename)
    #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #         img_path = redirect(url_for('uploaded_file',
    #                                 filename=filename))
    
    form = InputForm(csrf_enabled=False)  

    print form.errors

    segment_img = None
    model_img = None
    filename = None

    if request.method == "POST":    
        if form.validate_on_submit():
            n_segments = int(form.S.data)
            compactness = form.C.data
            sigma = form.s.data
            n_colors = int(form.NC.data)

            print "getting file name" 
            filename = os.path.join("uploads",
                                    secure_filename(form.P.data.filename))

            print "saving image", filename
            form.P.data.save(filename)
            # img = cbn.load_image("static/tiger.jpg")
            print "loading image"
            img = cbn.load_image(filename)
            print "processing image"
            segment_img, model_img = cbn.image_to_color_in(img,
                                           n_segments=n_segments,
                                           compactness=compactness,
                                           sigma=sigma,
                                           n_colors=n_colors) 
        else:
            print "nothing"

    return render_template(template_name + '.html',
                           form=form, 
                           img=filename,
                           result_1=segment_img,
                           result_2=model_img)

if __name__ == '__main__':
    app.run(debug=True)
