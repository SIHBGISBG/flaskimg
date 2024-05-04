from flask import Flask, request, Response, render_template
from werkzeug.utils import secure_filename

from db import db_init, db
from models import Img

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
db_init(app)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        pic = request.files['pic']
        if not pic:
            return "No pic", 400
        filename = secure_filename(pic.filename)
        print(filename)
        mimetype = pic.mimetype
        print(mimetype)
        if not filename or not mimetype:
            return "Wrong data", 400
        
        img = Img(img=pic.read(), name=filename, mimetype=mimetype)
        db.session.add(img)
        db.session.commit()
        return "Img uploaded", 200
    else:
        return render_template('index.html')

@app.route('/<int:id>')
def get_img(id):
    img = Img.query.filter_by(id=id).first()
    if not img:
        return 'Img not found', 404
    return Response(img.img, mimetype=img.mimetype)
    
if __name__ == "__main__":
    app.run()