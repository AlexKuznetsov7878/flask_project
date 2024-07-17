import os
import sqlite3

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['UPLOAD_FOLDER'] = "./static"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    image_filename = db.Column(db.String(120), unique=True, nullable=True)


@app.route('/')
def index():
    users = User.query.all()
    return render_template("homepage.html", users=users)

@app.route("/signup/", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        file = request.files.get('image_filename')

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_user = User(username=username, email=email, password=password, image_filename=filename)
            db.session.add(new_user)
            db.session.commit()

    return render_template("signup.html")

if __name__ == '__main__':
    app.run(debug=True)