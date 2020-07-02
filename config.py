import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\x1f\r\xc0P\x84S\xc4\xa0\xc1\x86<\x07]V8n'

    
