from werkzeug.utils import import_string
from flask import current_app

_DRIVES = {
    'local':'flask_saved.providers.local.LocalStorage',
    'oss': 'flask_saved.providers.oss.OssStorage'
}


class Storage:
    def __init__(self, app=None):
        self.default_provider = None
        if app is not None:
            self.init_app(app)
      
    @staticmethod       
    def provider(self, name=None):
        _provider = name if name is not None else current_app.config['STORAGE_PROVIDER_DEFAULT']
        if _provider not in _DRIVES:
            raise RuntimeError('Storage Provider error')
        _provider_object = import_string(_DRIVES[_provider])
        return _provider_object()
    
    def __getattr__(self, key):
        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            current_provider = current_app.config['STORAGE_PROVIDER_DEFAULT']
            if current_provider not in _DRIVES:
                raise RuntimeError('Storage Provider error')
            _provider_object = import_string(_DRIVES[current_provider])
            return getattr(_provider_object(), key)

    def init_app(self, app):
        # STORAGE 默认使用的
        default_provider = app.config.setdefault('STORAGE_PROVIDER_DEFAULT', 'local')        
        if default_provider not in _DRIVES:
           raise RuntimeError('STORAGE_PROVIDER_DEFAULT set error')  
        
        # LOCAL 提供器配置项
        app.config.setdefault('STORAGE_LOCAL_BASE_PATH', 'upload')
        app.config.setdefault('STORAGE_LOCAL_BASE_URL', None)
              
        
        # OSS 提供器配置
        oss_key = app.config.setdefault('STORAGE_OSS_ACCESS_KEY', None)
        oss_secret = app.config.setdefault('STORAGE_OSS_SECRET_KEY', None)
        oss_endpoint = app.config.setdefault('STORAGE_OSS_ENDPOINT', None)
        oss_bucket = app.config.setdefault('STORAGE_OSS_BUCKET', None)
        app.config.setdefault('STORAGE_OSS_CNAME', None)
        app.config.setdefault('STORAGE_OSS_DOMIAN', None)
        app.config.setdefault('STORAGE_OSS_BASE_PATH', None)
        # 使用oss提供器 必须设置的配置项
        if default_provider == 'oss':
            if oss_key is None:
                raise RuntimeError('STORAGE_OSS_ACCESS_KEY must be set')
            if oss_secret is None:
                raise RuntimeError('STORAGE_OSS_SECRET_KEY must be set')
            if oss_endpoint is None:
                raise RuntimeError('STORAGE_OSS_ENDPOINT must be set')
            if oss_bucket is None:
                raise RuntimeError('STORAGE_OSS_BUCKET must be set')

        self.default_provider = default_provider
        app.extensions['storage'] = self