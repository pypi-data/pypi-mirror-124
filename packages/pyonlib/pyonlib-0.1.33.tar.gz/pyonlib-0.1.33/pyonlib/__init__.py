class open_pyon(object):
    def __init__(self,path,mode='w',encoding="utf-8"):
        self.file=open(path,mode,encoding=encoding)
        self.path=path
    def write(self,value):
        value=str(value)
        self.file.write(value)
        self.file.flush()
    def flush(self):
        self.file.flush()
    def read(self,num=None):
        return self.file.read(num)
    def readline(self,val=None):
        return self.file.readline(val)
    def writeitem(self,itemkey,itemvalue):
        self.checkkeytype(itemkey)
        if type(itemvalue)==str:
            result=self.getstrcode(itemkey)+":\""+itemvalue+"\","
        else:
            result=self.getstrcode(itemkey)+':'+itemvalue+','
        self.file.write(result)
    def todic(self):
        r=open(self.path,"r+")
        if not r.read().endswith('}'):
            content=r.read()+"\n}"
        else:
            content=r.read()
        content=content.replace("\n\n",'')
        content=content.replace("{,",'{')#最大容错性
        try:
            result=eval(content)
        except Exception as e:
            raise (open_pyon.errors.PyonConvertError("不能将本对象转换为dict对象，因为"+str(e)))
        else:
            return result
        pass
    def getstrcode(self,obj):
        if type(obj)==str:
            result="\""+obj+"\""
            #如果是字符串，包含双引号。
        else:
            result=str(obj)
        return result
    from pyonlib import errors
    def checkkeytype(self,itemkey):
        if type(itemkey)==list:
            err=open_pyon.errors.KeyTypeError("不能将列表作为字典的建。")
            raise (err)
        else:pass
    def close(self):
        self.file.close()
    pass
def newpyon(path):
    file=open_pyon(path,"w+",encoding="utf-8")
    file.write('{\n')
    return file
def checkpyon(file):
    if not file.read():
        file.write("{\n")
        file.flush()
        return False
    else:
        return True
    pass