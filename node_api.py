import glob
import os
import threading
import time

import Pyro4


class HeartBeatConsumer(threading.Thread):

    def __init__(self, server_die_callback):
        threading.Thread.__init__(self)
        self.server_die_callback = server_die_callback
        self.last_ping = None

    def run(self):
        self.last_ping = time.time()
        while True:
            time.sleep(2)
            if (time.time() - self.last_ping) > 2:
                # print('server is gone')
                self.server_die_callback()
                break

    def beat(self):
        # print('receive heartbeat')
        self.last_ping = time.time()


class HeartBeatProducer(threading.Thread):

    def __init__(self, heart_beat_sender):
        threading.Thread.__init__(self)
        self.heart_beat_sender = heart_beat_sender
        self.client_still_alive = True

    def run(self):
        while self.client_still_alive:
            try:
                self.heart_beat_sender()
                time.sleep(1.2)
            except:
                pass


class NodeApi(object):
    # key : server uri, value : this hb_consumer
    nodes_hb = {}
    nodes = {}
    node_uri = None

    @staticmethod
    def print_connected_nodes():
        for i, uri in enumerate(NodeApi.nodes.keys()):
            print(str(i + 1) + '. ' + uri)

    @staticmethod
    def get_heart_beat_consumer(server_uri):
        return NodeApi.nodes_hb[server_uri]

    @staticmethod
    def _remove_node(node_uri):
        print('nodes '+node_uri+' is gone')
        del NodeApi.nodes[node_uri]
        del NodeApi.nodes_hb[node_uri]

    @staticmethod
    def send_heart_beat(client_uri):
        NodeApi.nodes_hb[client_uri].beat()

    @staticmethod
    def ask_connect(client_uri: str):
        client: NodeApi = Pyro4.Proxy(client_uri)

        send_heat_beat = lambda: client.send_heart_beat(NodeApi.node_uri)

        hb_producer = HeartBeatProducer(send_heat_beat)

        def die_callback():
            hb_producer.client_still_alive = False
            NodeApi._remove_node(client_uri)

        hb_consumer = HeartBeatConsumer(die_callback)
        NodeApi.nodes_hb[client_uri] = hb_consumer
        NodeApi.nodes[client_uri] = client_uri
        hb_producer.start()
        hb_consumer.start()

        # return hb_consumer

    @staticmethod
    def connect_to(server_uri: str):
        server: NodeApi = Pyro4.Proxy(server_uri)
        hb_producer = None

        def die_callback():
            hb_producer.client_still_alive = False
            NodeApi._remove_node(server_uri)

        hb_consumer = HeartBeatConsumer(die_callback)
        NodeApi.nodes_hb[server_uri] = hb_consumer
        NodeApi.nodes[server_uri] = server

        server.ask_connect(NodeApi.node_uri)

        send_heart_beat = lambda : server.send_heart_beat(NodeApi.node_uri)
        hb_producer = HeartBeatProducer(send_heart_beat)

        hb_producer.start()
        hb_consumer.start()

        # del NodeApi.nodes_hb[server_uri]

    @staticmethod
    def list():
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
            output += '-> ' + dir['name'] + '     [{}]'.format(dir_type) + '\n'
        return output

    @staticmethod
    def create(filename):
        fd = open(filename, 'w+')
        return filename + 'has been created'

    @staticmethod
    def delete(path):
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
            elif len(os.listdir(path)) == 0:
                os.rmdir(path)
        return 'path ' + path + ' has been deleted'

    @staticmethod
    def read(filename):
        fd = open(filename, 'r')
        output = ''
        for data in fd:
            output += data
        fd.close()
        return output

    @staticmethod
    def append(filename, text):
        fd = open(filename, 'w')
        fd.write(text)
        return 'success write to ' + filename + '\ncontent : \n' + text
