from flask import Flask, render_template, request, redirect, url_for,send_from_directory, jsonify
from flask_saved import Storage
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
import pprint
import uuid
import os
import urllib
import requests
from requests.models import Response

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jajajjajjja'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/sogou'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.config['STORAGE_LOCAL_BASE_PATH'] = '../upload/pic'

# app.config['STORAGE_PROVIDER_DEFAULT'] = 'oss'
# app.config['STORAGE_OSS_ACCESS_KEY'] = ''
# app.config['STORAGE_OSS_SECRET_KEY'] = ''
# app.config['STORAGE_OSS_ENDPOINT'] = ''
# app.config['STORAGE_OSS_BUCKET'] = ''
# app.config['STORAGE_OSS_BASE_PATH'] = ''
# app.config['STORAGE_OSS_DOMIAN'] = ''
# app.config['STORAGE_OSS_CNAME'] = True

tool_bar = DebugToolbarExtension(app)
app.debug = True
storage = Storage(app)
db = SQLAlchemy(app)

class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Boolean, index=True, nullable=False, default=True, comment='状态')
    url = db.Column(db.String(255), comment='图片链接', index=True, nullable=False)
    name = db.Column(db.String(255))
    path = db.Column(db.String(255))
    
    @property
    def dest(self):
        return os.path.join(self.path, self.name)
    


@app.before_first_request
def bfr():
    db.create_all()

@app.route('/', methods=['get', 'post'])
def index():
    print(request.headers['Host'])
    if request.method == 'POST':
        upload = request.files.get('upload')
        src = request.form.get('src')
        if upload:
            f = request.files['upload']
        elif src:
            f = requests.get(src)
            if f.status_code != 200:
                return '', f.status_code
            # content_type = f.headers['Content-Type']
            # index = content_type.index('/')
            # if content_type[index+1:] not in storage.extensions:
            #     return '', 401
        else:
            return '', 400
        
        # print('========', f.__dict__)
        print(f.headers)
        result = storage.save(f)
        print(result)
        pic = Picture()
        pic.url = result.url
        pic.path = result.flag
        db.session.add(pic)
        db.session.commit()
    return render_template('index.html')


@app.route('/lists')
def show():
    res = Picture.query.all()
    return render_template('lists.html', result = res)

@app.route('/delete')
def delete():
    pid = request.args.get('picture')
    img = Picture.query.get(pid)
    storage.delete(img.name)
    db.session.delete(img)
    db.session.commit()
    return redirect(url_for('.show'))


@app.route('/img/<path:filename>')
def img(filename):
    return storage.read(filename)
    # return send_from_directory(storage.base_path, filename)