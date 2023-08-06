
from pyauthserver.session import session
from sanic import response
from sanic.request import Request
from pyauthserver import resplib
from pyauthserver import config as cfg
from pyauthserver.models.user import User

def isLogin(request,update_expire_time=False):
    if 'session_id' in request.cookies.keys():
        session_id=request.cookies['session_id']
        user_info=session.get(session_id)
        if not user_info:
            return False
        else:
            user=User.from_json(user_info)
            if update_expire_time:
                session.set(session_id,user_info,cfg.login_max_age)
            return {
                'session_id':session_id,
                'user':user
            }
    return False

def login_required(defaultResponse=None,update_expire_time=False,roles=False):
    if roles:
        assert isinstance(roles,(list,tuple))
    def decorator(coroutine):
        async def wrapper(request: Request, **kwargs):

            if cfg.devMode:
                # print("cookies:",request.cookies)
                user =create_test_user()
                request.ctx.user=user
                request.ctx.session_id='wfrjuyf8'
                return await coroutine(request=request, **kwargs)
            res = isLogin(request,update_expire_time=update_expire_time)
            if res:
                user=res['user']
                user.check_role()
                request.ctx.session_id=res['session_id']
                request.ctx.user = user
                if roles and (user.role not in roles):
                    return resplib.error('您没有访问权限')
                return await coroutine(request=request, **kwargs)
            else:
                return defaultResponse or resplib.error(message='请先登录')
        return wrapper
    return decorator