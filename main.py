from flask import Flask, send_file, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] =  'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"],filename)
        file.save(file_path)

        if os.path.exists(file_path):
            import subprocess
            subprocess.run(['python3','dg_final_analysisplan.py',filename])

            output_filename = f"static/files/output-{filename}.zip"
            
            return send_file(output_filename, as_attachment=True)

    return render_template('index.html', form=form)

if __name__ == '__main__':
    
    app.run(debug=True, host="0.0.0.0")