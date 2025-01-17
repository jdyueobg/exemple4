from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# إعداد Cloudinary
cloudinary.config(
  cloud_name = 'dsendkvnz',
  api_key = '166825977529234',
  api_secret = 'jiD4JBX6rspLdGY62gzjK1YPX5U'
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_url = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Post {self.name}>'

@app.route('/')
@app.route('/index')
def home():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/posts/add', methods=['GET', 'POST'])
def post_add():
    if request.method == 'POST':
        if 'photo' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['photo']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            try:
                upload_result = cloudinary.uploader.upload(file)
                photo_url = upload_result['secure_url']
                new_post = Post(photo_url=photo_url, name=request.form['name'], body=request.form['body'])
                db.session.add(new_post)
                db.session.commit()
                return redirect(url_for('home'))
            except Exception as e:
                flash(f'An error occurred: {e}')
                return redirect(request.url)
    return render_template('post-add.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)