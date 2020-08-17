from . import BaseStorage
from .._compat import urljoin
from flask import current_app
from werkzeug.utils import cached_property
import oss2
import os
import uuid
  

class OssStorage(BaseStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._access_key = current_app.config.get('STORAGE_OSS_ACCESS_KEY')
        self._secret_key = current_app.config.get('STORAGE_OSS_SECRET_KEY')
        self._endpoint = current_app.config.get('STORAGE_OSS_ENDPOINT')
        self._bucket = current_app.config.get('STORAGE_OSS_BUCKET')
        self._cname = current_app.config.get('STORAGE_OSS_CNAME')
        self._domain = current_app.config.get('STORAGE_OSS_DOMIAN')
        self.base_path = current_app.config.get('STORAGE_OSS_BASE_PATH')
 
    @cached_property
    def auth(self):
        return oss2.Auth(self._access_key, self._secret_key)

    @cached_property
    def bucket(self):
        return oss2.Bucket(self.auth, self._endpoint, self._bucket)
    
    @cached_property
    def host(self):
        return '{schema}://{bucket}.{endpoint}'.format(
            schema='https', 
            bucket=self._bucket,
            endpoint=self._endpoint
        )
    
    def save(self, storage, filename=None):
        filename = filename if filename else uuid.uuid4().hex
        full_path = os.path.join(self.base_path, filename).replace('\\','/')
        headers = None
        content_type = storage.headers.get('Content-Type')
        if content_type:
            headers = {'Content-Type': content_type}
        result = self.bucket.put_object(full_path, storage, headers=headers)
        if result.status == 200:
            return self.Result(
                url=self._generate_url(full_path),
                flag=full_path
            )
        else:
            return False
    
    def delete(self, flag):
        if self.bucket.object_exists(flag):
            self.bucket.delete_object(flag)
        return True

    
    def _generate_url(self, path):
        if self._domain:
            return urljoin(self._domain, path)
        else:
            return urljoin(self.host, path)
    
   