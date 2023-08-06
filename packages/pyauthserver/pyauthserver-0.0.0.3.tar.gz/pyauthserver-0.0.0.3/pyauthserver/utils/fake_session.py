import os

_root=os.path.dirname(__file__)
def json_load(f,encoding='utf-8',*args,**kwargs):
    import json
    with open(f,'r',encoding=encoding) as fp:
        return json.load(fp,*args,**kwargs)
def json_dump(obj,fp,encoding='utf-8',ensure_ascii=False,*args,**kwargs):
    import json
    with open(fp,'w',encoding=encoding) as f:
        json.dump(obj,f,ensure_ascii=ensure_ascii,*args,**kwargs)
class FileDict(dict):
    def __init__(self, path):
        self.seta(path=path)
        if os.path.exists(path):
            assert os.path.isfile(path)
            dic = json_load(path)
            assert isinstance(dic, dict)
        else:
            dic = {}
            json_dump(dic, path, indent=4)
        super().__init__(dic)

    def set_attribute(self, key, value):
        self.__dict__[key] = value

    def get_attribute(self, *args, **kwargs):
        return self.__dict__.get(*args, **kwargs)

    def seta(self, **kwargs):
        for k, v in kwargs.items():
            self.set_attribute('__%s__' % (k), v)

    def __setattr__(self, key, value):
        dict.__setattr__(self, key, value)
        self._save()

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        self._save()
    def pop(self, key):
        dict.pop(self,key)
        self._save()
    def update(self, *args, **kwargs):
        for k, v in kwargs.items():
            self[k] = v
        for arg in args:
            self.update(**arg)
    def geta(self, key, *args, **kwargs):
        return self.get_attribute('__%s__' % (key), *args, **kwargs)
    def _save(self):
        json_dump(self, self.geta('path'), indent=4)
class FakeSession(FileDict):
    def set(self,key,value,ex=None):
        self[key]=value
    def exists(self,key):
        return key in self.keys()
    def delete(self,key):
        self.pop(key)
    def get(self,key):
        return FileDict.get(self,key)

