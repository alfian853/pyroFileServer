import glob
import os


class ServerApi:

    def list(self):
        dir_list = glob.glob('/*')
        dir_list = map(
            lambda path: {'name': path.split('/')[-1], 'is_file': os.path.isfile(path)},
            dir_list
        )
        for dir in dir_list:
            dir_type = ''
            if dir['is_file']:
                dir_type = 'file'
            else:
                dir_type = 'folder'
            print('-> ' + dir['name'] + '     [{}]'.format(dir_type))

    def create(self, filename):
        fd = open(filename, 'w+')

    def delete(self, path):
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
            elif len(os.listdir(path)) == 0:
                os.rmdir(path)

    def read(self, filename):
        fd = open(filename, 'r')
        for data in fd:
            print(data)
        fd.close()

    def append(self, filename, text):
        fd = open(filename, 'w')
        fd.write(text)
