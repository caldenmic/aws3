from flask import Flask, render_template, request
import boto3
from werkzeug.utils import secure_filename
import key_config as keys
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db= SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/swiftcode'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class app_user(db.Model):
    __tablename__ = "app_user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    legal_terms_agreed = db.Column(db.Integer)
    password = db.Column(db.String)
    role = db.Column(db.String)
    resume_submitted = db.Column(db.Integer)
    candidate_information_id = db.Column(db.Integer)
    s3bucket = db.relationship('s3bucket', backref = 'app_user', cascade = 'all, delete-orphan', lazy = 'dynamic')

class S3Bucket(db.Model):
    __tablename__ = "s3bucket"
    id = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    link = db.Column(db.String)

s3 = boto3.client('s3',
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key= keys.ACCESS_SECRET_KEY,
                    aws_session_token=keys.AWS_SESSION_TOKEN
                )

BUCKET_NAME='swiftcode-dev'

@app.route('/')  
def home():
    return render_template("upload.html")

@app.route('/upload',methods=['post'])
def upload():
    if request.method == 'POST':
        resume = request.files['file']
        if resume:
                filename = secure_filename(resume.filename)
                resume.save(filename)
                s3.upload_file(
                    Bucket = BUCKET_NAME,
                    Filename = filename,
                    Key = filename
                )
                msg = "Upload Done ! "

    return render_template("upload.html",msg=msg)

if __name__ == "__main__":
    app.run(debug=True)