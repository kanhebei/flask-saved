flask-saved

flask-saved是一个flask的存储扩展

**使用方式**

pip install Flask-Saved

from flask_saved import Storage

storage = Storage(app) or storage = Storage.init_app(app)

storage.save(file)

**目前实现了local（本地） oss（阿里云）的存储方式**


**local 配置项**

STORAGE_LOCAL_BASE_PATH

说明：

本地存储基本的路径

比如 upload 目录

STORAGE_LOCAL_BASE_PATH = 'upload'

相对路径。。相对与当前应用的目录

STORAGE_LOCAL_BASE_PATH = '../upload'

相对路径。。相对与当前应用目录的上层目录

STORAGE_LOCAL_BASE_URL

说明：

本地存储基本url

STORAGE_LOCAL_BASE_URL = 'http://picture.domain.com'


**oss 配置项**

STORAGE_OSS_ACCESS_KEY

STORAGE_OSS_SECRET_KEY

STORAGE_OSS_ENDPOINT

STORAGE_OSS_BUCKET

STORAGE_OSS_CNAME

STORAGE_OSS_DOMIAN

STORAGE_OSS_BASE_PATH