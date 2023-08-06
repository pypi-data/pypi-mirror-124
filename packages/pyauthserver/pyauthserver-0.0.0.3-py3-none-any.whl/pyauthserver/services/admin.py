from sanic import Blueprint
from sanic.request import Request
from pyauthserver.utils.login import login_required
from pyauthserver import resplib
import os
from pyauthserver import config as cfg
from pyauthserver.session import session

admin_bp=Blueprint('admin')


@admin_bp.route('/isAdmin',methods=['GET'])
@login_required(False,roles=['admin'])
async  def do_is_admin(request:Request):
    return resplib.success(data={'isAdmin':True})

@admin_bp.route('/userInfo',methods=['GET'])
@login_required(False,roles=['admin'])
async  def do_user_info(request:Request):
    return resplib.success(data=request.ctx.user.to_dict())
