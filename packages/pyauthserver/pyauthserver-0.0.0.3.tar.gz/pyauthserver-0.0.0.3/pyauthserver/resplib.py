from sanic import response

def data(**kwargs):
    return response.json(kwargs,ensure_ascii=False)
def error(message='未知错误',code=-1,status='error',**kwargs):
    return response.json(dict(message=message,code=code,status=status,**kwargs),ensure_ascii=False)
def success(message='成功', success=True, data=None,**kwargs):
    if data is None:
        data = {}
    return response.json(dict(message=message,success=success,data=data,**kwargs),ensure_ascii=False)
def LoginResult(status,message='',type=None,currentAuthority='未指定',code=0,**kwargs):
    return response.json(dict(status=status,type=type,currentAuthority=currentAuthority,message=message,code=code,**kwargs),ensure_ascii=False)

def LoginResultSuccess(message='',type=None,currentAuthority='未指定',code=0):
    return LoginResult(status='ok',message=message,type=type,currentAuthority=currentAuthority,code=code,success=True)
def LoginResultFailure(message='',type=None,currentAuthority='未指定',code=0):
    return LoginResult(status='error',message=message,type=type,currentAuthority=currentAuthority,code=code,success=False)
def RegisterResult(status,message='',type=None,currentAuthority='未指定',code=0,**kwargs):
    return response.json(dict(status=status,type=type,currentAuthority=currentAuthority,message=message,code=code,**kwargs),ensure_ascii=False)

def RegisterResultSuccess(message='',type=None,currentAuthority='未指定',code=0):
    return response.json(dict(status='ok',type=type,currentAuthority=currentAuthority,message=message,code=code,success=True),ensure_ascii=False)
def RegisterResultFailure(message='',type=None,currentAuthority='未指定',code=0):
    return response.json(dict(status='error',type=type,currentAuthority=currentAuthority,message=message,code=code,success=False),ensure_ascii=False)

class _T(str):
    def __call__(self, s):
        if s.upper() == self or s == self:
            return True
        else:
            return False


CONST_TYPE = _T


class TMetaClass(type):
    def __new__(cls, name, bases, attrs):
        dic = attrs.copy()
        for k, v in attrs.items():
            if isinstance(v, _T):
                dic[k] = _T(k)
        return type.__new__(cls, name, bases, dic)


class T(metaclass=TMetaClass):
    NOT_FOUND = _T()
    NOT_EXISTS = _T()
    NO_VALUE = _T()
    NOT_IMPLEMENTED = _T()
    NOT_ALLOWED = _T()
    EMPTY = _T()
    NO_SUCH_VALUE = _T()
    NO_SUCH_ATTR = _T()
    NOT_GIVEN = _T()
    FOLDER = _T()
    FILE = _T()
    DIR = _T()
    LINK = _T()
    MOUNT = _T()
    IMAGE = _T()
    TEXT = _T()
    VIDEO = _T()
    AUDIO = _T()
    JSON = _T()
    TXT = _T()
    PY = _T()
    JPG = _T()
    PNG = _T()
    JPEG = _T()
    GIF = _T()
    PGM = _T()
    BMP = _T()
    JS = _T()
    MP4 = _T()
    AVI = _T()
    IMAGE_FILE_EXTS = [JPG, JPEG, PNG, GIF, PGM, BMP]
class PointDict(dict):
    __no_value__ = '<__no_value__>'

    def __getattr__(self, key, default=T.NOT_GIVEN):
        if key in self.keys():
            return self[key]
        elif default != T.NOT_GIVEN:
            return default
        raise KeyError('No such key named %s' % (key))

    def __setattr__(self, key, value):
        self[key] = value

    def __call__(self, key, value=__no_value__):
        if value is self.__no_value__:
            self[key] = PointDict()
        else:
            self[key] = value
        return self[key]

    def set_attribute(self, key, value):
        self.__dict__[key] = value

    def get_attribute(self, *args, **kwargs):
        return self.__dict__.get(*args, **kwargs)

    def seta(self, **kwargs):
        for k, v in kwargs.items():
            self.set_attribute('__%s__' % (k), v)

    def geta(self, key, *args, **kwargs):
        return self.get_attribute('__%s__' % (key), *args, **kwargs)

    @classmethod
    def from_dict(cls, dic):
        dic2 = cls()
        for k, v in dic.items():
            if not isinstance(v, dict):
                dic2[k] = v
            else:
                dic2[k] = cls.from_dict(v)
        return dic2

    def print(self):
        import json
        print(json.dumps(self, sort_keys=True, indent=4))

    def print1(self, depth=0, step=5, space_around_delimiter=1, fillchar=' ', cell_border='|', delimiter=':'):
        import re
        def len_zh(data):
            temp = re.findall('[^a-zA-Z0-9.]+', data)
            count = 0
            for i in temp:
                count += len(i)
            return (count)

        for k, v in self.items():
            for i in range(depth):
                print(fillchar * step, end='')
                print(cell_border, end='')
            print(k.rjust(step - len_zh(k), fillchar),
                  end=' ' * space_around_delimiter + delimiter + ' ' * space_around_delimiter)
            if not isinstance(v, PointDict):
                print(v)
            else:
                print('\n', end='')
                v.print1(depth=depth + 1, step=step, space_around_delimiter=space_around_delimiter,
                         cell_border=cell_border, fillchar=fillchar, delimiter=delimiter)

    def pprint1(self):
        self.print1(step=5, space_around_delimiter=0, fillchar='`', cell_border='|', delimiter=':')


def _make_metaclass(mapper):
    class Meta(type):
        def __new__(cls, name, bases, attrs):
            altered_attrs={}
            __shadow_dict__ = {}
            for base in bases:
                if hasattr(base, '__shadow_dict__'):
                    __shadow_dict__.update(getattr(base, '__shadow_dict__'))
            for k, v in attrs.items():
                k1,v1=mapper(k,v)
                if k1:
                    altered_attrs[k1]=v1
                    __shadow_dict__[k1] = v1
            attrs.update(altered_attrs)
            attrs['__shadow_dict__'] = __shadow_dict__
            return type.__new__(cls, name, bases, attrs)
    return Meta

class MetaclassFactory:
    ClassToDictMeta=lambda :_make_metaclass(mapper=lambda k,v:(None,None) if k.startswith('__') else (k,v))

    @staticmethod
    def ResponseFactoryMeta():
        def response_mapper(k, v):
            if k.startswith('__'): return None, None
            class SomeResponse(ResponseBase):
                status = k
                code = v[0]
                status_zh=v[1]
                message = v[1]
            SomeResponse.__name__=k
            v = SomeResponse
            # print(k, v)
            return k, v
        return _make_metaclass(mapper=response_mapper)


class BaseFactory:

    @staticmethod
    def ClassDict():
        class ClassDict(PointDict, metaclass=MetaclassFactory.ClassToDictMeta()):
            def __init__(self, *args, **kwargs):
                super().__init__(self.__class__.__shadow_dict__)
                self.update(*args, **kwargs)
        return ClassDict

    @staticmethod
    def PredefinedDict():
        class PredefinedDict(PointDict):
            __predefined_location__='__shadow_dict__'
            def __init__(self, *args, **kwargs):
                super().__init__(getattr(self.__class__,self.__predefined_location__))
                self.update(*args, **kwargs)
        return PredefinedDict
    @staticmethod
    def ResponseTypes():
        class ResponseTypes(BaseFactory.PredefinedDict(),metaclass=MetaclassFactory.ResponseFactoryMeta()):
            pass
        return ResponseTypes

class ResponseBase(BaseFactory.ClassDict()):
    status=None
    code=None
    message=None
    data=None
class Success(ResponseBase):
    success = True
class Failure(ResponseBase):
    success = False



class ResponseFactory(BaseFactory.ResponseTypes()):
    # 成功
    SUCCESS = 0, "成功"

    # / *参数错误：10001 - 19999 * /
    PARAM_IS_INVALID = 101, "参数无效"
    PARAM_IS_BLANK = 102, "参数为空"
    PARAM_TYPE_BIND_ERROR = 103, "参数类型错误"
    PARAM_NOT_COMPLETE = 104, "参数缺失"

    # / *用户错误：20001 - 29999 * /
    USER_NOT_LOGGED_IN = 201, "用户未登录"
    USER_LOGIN_ERROR = 202, "账号不存在或密码错误"
    USER_ACCOUNT_FORBIDDEN = 203, "账号已被禁用"
    USER_NOT_EXIST = 204, "用户不存在"
    USER_HAS_EXISTED = 205, "用户已存在"

    # / *业务错误：30001 - 39999 * /
    SPECIFIED_QUESTIONED_USER_NOT_EXIST = 301, "某业务出现问题"

    # / *系统错误：40001 - 49999 * /
    SYSTEM_INNER_ERROR = 401, "系统繁忙，请稍后重试"

    # / *数据错误：50001 - 599999 * /
    DATA_NOT_FOUND = 501, "数据未找到"
    DATA_IS_WRONG = 502, "数据有误"
    DATA_ALREADY_EXISTED = 503, "数据已存在"

    # / *接口错误：60001 - 69999 * /
    INTERFACE_INNER_INVOKE_ERROR = 601, "内部系统接口调用异常"
    INTERFACE_OUTTER_INVOKE_ERROR = 602, "外部系统接口调用异常"
    INTERFACE_FORBID_VISIT = 603, "该接口禁止访问"
    INTERFACE_ADDRESS_INVALID = 604, "接口地址无效"
    INTERFACE_REQUEST_TIMEOUT = 605, "接口请求超时"
    INTERFACE_EXCEED_LOAD = 606, "接口负载过高"

    # / *权限错误：70001 - 79999 * /
    PERMISSION_NO_ACCESS = 701, "无访问权限"



