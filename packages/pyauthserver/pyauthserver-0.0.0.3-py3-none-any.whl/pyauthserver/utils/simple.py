import uuid
import random
import hashlib
def gen_session_id():
    return uuid.uuid4().hex
def gen_hash(s):
    return hashlib.sha256(s.encode()).hexdigest()[:20]
def rename_func(name):
    def decorator(func):
        func.__name__=name
        return func
    return decorator
def gen_captcha(n=6):
    s=[]
    for i in range(n):
        s+=str(random.randint(0,9))
    return s
def sendPhoneCaptcha(phone):
    captcha=gen_captcha(6)
    return captcha
def hash_password(password):
    salt = 'd5453bab60014ead9cc4d9c10147e66e'
    hashed_password = hashlib.sha512(password + salt).hexdigest()
    return hashed_password
def validate_password(password,password_hash):
    return hash_password(password)==password_hash