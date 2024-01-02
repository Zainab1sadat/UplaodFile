from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///files.db'  # SQLite database
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)
app.app_context().push()

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), unique=True, nullable=False)

@app.route('/upload')
def index():
    files = File.query.all()
    return render_template('index.html', files=files)

@app.route('/uploadfile', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = app.config['UPLOAD_FOLDER'] + '/' + uploaded_file.filename
        uploaded_file.save(file_path)
        new_file = File(filename=uploaded_file.filename)
        db.session.add(new_file)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
