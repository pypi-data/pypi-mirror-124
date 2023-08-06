from pyauthserver import config as cfg
from pyauthserver.utils import gen_hash

def sign_text(text):
    return gen_hash('%s:%s:%s'%(cfg.access_key_id,cfg.access_key_secret,text))
def check_sign(signature,text):
    sig=gen_hash('%s:%s:%s'%(cfg.access_key_id,cfg.access_key_secret,text))
    return sig==signature