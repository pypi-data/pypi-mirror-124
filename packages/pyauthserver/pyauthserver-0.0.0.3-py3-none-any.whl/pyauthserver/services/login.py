from sanic import Sanic,Blueprint,response,request
from sanic.request import Request
from sanic_cors import CORS
import uuid
from pyauthserver import resplib
from pyauthserver import config as cfg
from pyauthserver.session import session,captcha_cache
from pyauthserver.utils import sendPhoneCaptcha
from pyauthserver.utils.login import login_required
from pyauthserver.models.user import User
from pyauthserver.utils.db import get_db_helper
from pyauthserver.utils import hash_password,gen_session_id




login_bp=Blueprint('login')
user_helper=get_db_helper(User)

@login_bp.route('/api/currentUser',methods=['GET'])
@login_required(resplib.error('尚未登陆'),update_expire_time=True)
async def do_get_current_user(request):
    user=request.ctx.user
    print(user.to_dict())
    return resplib.success(data=user.to_dict())
@login_bp.route('/api/isUsernameUsed',methods=['GET'])
async def do_signup(request:Request,username):
    return resplib.data(username=username,isUsed=user_helper.exists(username=username))

@login_bp.route('/api/register',methods=['POST'])
async def do_signup(request:Request):
    email=request.json['email']
    username=request.json['username']
    password=request.json['password']
    mobile=request.json['mobile']
    print('Register user :',email,username,password,mobile)
    if user_helper.exists(email=email):
        return resplib.RegisterResultFailure('该邮箱已被注册')
    elif user_helper.exists(username=username):
        return resplib.RegisterResultFailure('该用户名已被注册')
    elif user_helper.exists(mobile=mobile):
        return resplib.RegisterResultFailure('该手机号已被注册')
    else:
        user_helper.create_one(password=password,username=username,email=email,mobile=mobile)
        return resplib.RegisterResultSuccess('注册成功')
@login_bp.route('/api/login/outLogin',methods=['POST'])
@login_required(False)
async def do_logout(request:Request):
    # if not cfg.devMode:
    session_id=request.ctx.session_id
    assert session_id
    print('Try Logout :', session_id, request.ctx.user.to_json())
    session.delete(session_id)
    resp=resplib.success('已退出登录')
    resp.cookies['session_id'] = ''
    resp.cookies['session_id']['max-age'] = 0
    return resp

@login_bp.route('/api/isLogin',methods=['get'])
async def do_auth(request:Request):
    if 'session_id' in request.cookies.keys():
        session_id=request.cookies['session_id']
        if session.get(session_id):
            return response.json(resplib.Success(isLogin=True))
    return response.json(resplib.Failure(isLogin=False))
# 获取验证码
@login_bp.route('/api/login/captcha',methods=['POST'])
async def do_captcha(request:Request):
    if not 'mobile' in request.args:
        return response.json(resplib.Failure(message='缺少手机号码字段'))
    mobile=request.args['mobile']
    captcha=sendPhoneCaptcha(mobile)
    captcha_cache.set(mobile,captcha)
    return response.json(resplib.Success(message='发送成功'))
# 处理登录表单
@login_bp.route('/api/login/account',methods=['POST'])
async def do_login(request:Request):
    data=request.json
    type=data.get('type')
    assert type  in ['username-password','email-password','mobile-password','mobile-code']
    def check_if_login(success_msg='登陆成功',err_msg='登录失败',**kwargs):
        user = user_helper.find_one(**kwargs)
        if user:
            resp = resplib.LoginResultSuccess(type=type,message=success_msg)
            session_id = gen_session_id()
            session.set(session_id, user.to_json(), cfg.login_max_age)
            resp.cookies['session_id'] = session_id
            resp.cookies['session_id']['max-age'] = cfg.login_max_age
            return resp
        else:
            return resplib.LoginResultFailure(type=type,message=err_msg)
    if type == 'mobile-code':
        captcha=data['captcha']
        mobile=data['mobile']
        cap=captcha_cache.get(mobile,None)
        if not cap:
            return resplib.LoginResultFailure(type=type,message='未提供验证码')
        if not cap==captcha:
            return resplib.LoginResultFailure(type=type,message='验证码错误')
        else:
            return check_if_login(mobile=mobile)
    else:
        identifier_name={
            'email-password':'email',
            'username-password':'password',
            'mobile-password':'mobile'
        }[type]
        identifier=data[identifier_name]
        password=data['password']
        if not user_helper.exists(**{identifier_name:identifier}):
            return resplib.LoginResultFailure(type=type,message='用户不存在')
        else:
            return check_if_login(**{identifier_name:identifier},password_hash=hash_password(password),err_msg='密码错误')


