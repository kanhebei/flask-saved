from . import BaseStorage
import os
from .._compat import urljoin
from flask import current_app
from werkzeug.exceptions import BadRequest
from requests.models import Response
import uuid


class LocalStorage(BaseStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = current_app.config.get('STORAGE_LOCAL_BASE_URL')
        self.base_path = current_app.config.get('STORAGE_LOCAL_BASE_PATH')
        
    def _generate_url(self, path):
        return urljoin(self.base_url or 'http', path)

    def save(self, storage, filename=None):
        filename = filename if filename else uuid.uuid4().hex
        ### 获取保存的目标地址 
        full_path = os.path.join(self.base_path, filename).replace('\\','/')
        # 如果保存的目标路径已经存在则返回异常
        if os.path.exists(full_path):
            raise UploadFileExists('File Already Exists')
        # 获取目标地址的路径
        folder = os.path.dirname(full_path)
        if not os.path.exists(folder):
            # 路径不存在的时候新建路径
            os.makedirs(folder)
            
        if isinstance(storage, str):
            with open(full_path, 'wb') as _f:
                _f.write(storage)
        if isinstance(storage, Response):
            with open(full_path, 'wb') as _f:
                _f.write(storage.content)
        elif hasattr(storage, 'read'):
            storage.save(full_path)
        else:
            raise BadRequest()
        return self.Result(
            url=self._generate_url(full_path),
            flag=full_path
        )

    def delete(self, flag):
        if os.path.exists(flag):
           os.remove(flag)
        # raise FileExistsError('Not Find %s' %dest)