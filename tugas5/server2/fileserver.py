import os

import Pyro4


class FileServer(object):
    def __init__(self):
        self.observer_name = ['fileserver-1','fileserver-3']
        self.observer = []
        for name in self.observer_name:
            self.observer.append(self.get_fileserver_object(name))

    def create_return_message(self,kode='000',message='kosong',data=None):
        return dict(kode=kode,message=message,data=data)

    def list(self):
        print("list ops")
        try:
            daftarfile = []
            for x in os.listdir():
                if x[0:4]=='FFF-':
                    daftarfile.append(x[4:])
            return self.create_return_message('200',daftarfile)
        except:
            return self.create_return_message('500','Error')

    def create(self, name='filename000'):
        nama='FFF-{}' . format(name)
        print("create ops {}" . format(nama))
        try:
            if os.path.exists(name):
                return self.create_return_message('102', 'OK','File Exists')
            f = open(nama,'wb',buffering=0)
            f.close()

            for observer in self.observer:
                observer.create(name)

            return self.create_return_message('100','OK')
        except:
            return self.create_return_message('500','Error')
    def read(self,name='filename000'):
        nama='FFF-{}' . format(name)
        print("read ops {}" . format(nama))
        try:
            f = open(nama,'r+b')
            contents = f.read().decode()
            f.close()
            return self.create_return_message('101','OK',contents)
        except:
            return self.create_return_message('500','Error')
    def update(self,name='filename000',content=''):
        nama='FFF-{}' . format(name)
        print("update ops {}" . format(nama))

        if (str(type(content))=="<class 'dict'>"):
            content = content['data']
        try:
            f = open(nama,'w+b')
            f.write(content.encode())
            f.close()
            for observer in self.observer:
                observer.update(name,content)
            return self.create_return_message('101','OK')
        except Exception as e:
            return self.create_return_message('500','Error',str(e))

    def delete(self,name='filename000'):
        nama='FFF-{}' . format(name)
        print("delete ops {}" . format(nama))

        try:
            os.remove(nama)
            for observer in self.observer:
                observer.delete(name)
            return self.create_return_message('101','OK')
        except:
            return self.create_return_message('500','Error')

    def get_fileserver_object(self, namainstance):
        uri = "PYRONAME:{}@localhost:7777" . format(namainstance)
        fserver = Pyro4.Proxy(uri)
        return fserver


if __name__ == '__main__':
    k = FileServer()
    # print(k.create('f1'))
    # print(k.update('f1',content='wedusku'))
    # print(k.read('f1'))
#    print(k.create('f2'))
#    print(k.update('f2',content='wedusmu'))
#    print(k.read('f2'))
    print(k.list())
    #print(k.delete('f1'))

