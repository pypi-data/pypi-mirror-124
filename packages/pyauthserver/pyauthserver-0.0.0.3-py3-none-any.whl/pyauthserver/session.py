from pyauthserver.utils.fake_session import FakeSession as Session
import os
import pyauthserver.config as cfg
import redis

if cfg.use_fake_session:
    _root = os.path.dirname(__file__)
    access_session = Session(_root + '/access.json')
    captcha_cache = Session(_root + '/captcha.json')
    session=Session(_root+'/session.json')
else:
    redis_connection_pool = redis.ConnectionPool(host=cfg.redis_host, port=cfg.redis_port, decode_responses=True)
    access_session = redis.Redis(host=cfg.redis_host, port=cfg.redis_port, decode_responses=True)
    captcha_cache=access_session
    session=access_session
