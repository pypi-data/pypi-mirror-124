import os

pkg_root=os.path.dirname(__file__)

#### database
class mysql:
    username='eiooie'
    db_name='eiooie'
    host='t.eiooie.com'
    password='eiooie.123456'



deploy=False
# deploy=True
#

if not deploy:
    devMode = True
    redirect_http_to_https = False
else:
    devMode = False
    redirect_http_to_https=True
raise_error=True
# raise_error=False
# redirect_http_to_https=False

login_max_age=60*60*24*30
download_link_expire_time=3*24*60*60
# 三小时
edit_file_expire_time=3*60*60


# session服务器
if deploy:
    use_fake_session=False
else:
    use_fake_session=True
redis_host='redis-session-server'
redis_port=6379

