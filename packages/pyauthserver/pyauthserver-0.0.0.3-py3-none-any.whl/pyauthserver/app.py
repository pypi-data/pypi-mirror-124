from sanic import Sanic,response
from sanic.request import Request
from sanic_cors import CORS
from pyauthserver.services.login import login_bp
from pyauthserver.config import mysql
def initdb():
    from pyauthserver.models.user import Base
    from pyauthserver.utils.db import gen_engine,gen_mysql_uri
    engine=gen_engine(uri=gen_mysql_uri(
        username=mysql.username,
        password=mysql.password,
        host=mysql.host,
        db_name=mysql.db_name,
    ))
    Base.metadata.create_all(engine,checkfirst=True)
def create_app():
    initdb()
    app=Sanic(__name__)
    CORS(app)
    app.blueprint(login_bp,url_prefix='/')
    return app
