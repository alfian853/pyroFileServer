import glob
import os
import sched
import threading
import time

import Pyro4

from client_api import HeartBeat


class HeartBeatSender(threading.Thread):

    def __init__(self, heart_beat : HeartBeat):
        threading.Thread.__init__(self)
        self.heart_beat = heart_beat

    def run(self):
        while True:
            try:
                self.heart_beat.set_alive()
                time.sleep(1.5)
            except:
                print('client is gone')
                return

class ServerApi(object):

    def __init__(self):
        self.stillAlive = True
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.scheduler.run()
        self.event = None

    def set_connected(self, client_uri: str):
        print('connected to client : '+client_uri)
        client: HeartBeat = Pyro4.Proxy(client_uri)
        client.set_alive()
        HeartBeatSender(client).start()

    def list(self):
        dir_list = glob.glob('/*')
        dir_list = map(
            lambda path: {'name': path.split('/')[-1], 'is_file': os.path.isfile(path)},
            dir_list
        )
        output = ''
        for dir in dir_list:
            dir_type = ''
            if dir['is_file']:
                dir_type = 'file'
            else:
                dir_type = 'folder'
            output+='-> ' + dir['name'] + '     [{}]'.format(dir_type)+'\n'
        return output

    def create(self, filename):
        fd = open(filename, 'w+')
        return filename + 'has been created'

    def delete(self, path):
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
            elif len(os.listdir(path)) == 0:
                os.rmdir(path)
        return 'path '+path+' has been deleted'

    def read(self, filename):
        fd = open(filename, 'r')
        output = ''
        for data in fd:
            output+=data
        fd.close()
        return output

    def append(self, filename, text):
        fd = open(filename, 'w')
        fd.write(text)
        return 'success write to '+filename+'\ncontent : \n'+text