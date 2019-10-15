import traceback

from Pyro4 import Daemon

from node_api import *


class Server(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon: Daemon = Pyro4.Daemon()
        x_GreetServer = Pyro4.expose(NodeApi)
        self.uri = self.daemon.register(x_GreetServer).asString()

    def run(self):
        self.daemon.requestLoop()


if __name__ == '__main__':
    server = Server()
    NodeApi.node_uri = server.uri
    server.start()
    print('start node uri: \n' + server.uri)
    # client_handler = ServerApi()
    active_server_api: NodeApi = None
    while True:
        commands = input().split(' ', 2)
        command = commands[0]

        if active_server_api is not None:
            if command == 'ls':
                print(active_server_api.list())

            elif command == 'create':
                print(active_server_api.create(commands[1]))

            elif command == 'rm':
                print(active_server_api.delete())

            elif command == 'append':
                print(active_server_api.append(commands[2]))

            elif command == 'cat':
                print(active_server_api.read())
        else:
            print('no server used')

        if command == 'connect':
            try:
                uri = commands[1]
                NodeApi.connect_to(uri)
                # die_callback = lambda: client_handler.unregister(uri)
                # new_client_server = Client(commands[1], die_callback)
                # client_handler.register(commands[1], new_client_server.server_api)
                # active_server_api = client_handler.get_server_api(commands[1])
                print('connected to ' + commands[1])
            except:
                traceback.print_exc()
                print('failed connect to ' + commands[1])

        elif command == 'use':
            active_server_api = NodeApi.nodes[commands[1]]
            if active_server_api is not None:
                print('success')

        elif command == 'stat':
            NodeApi.print_connected_nodes()

        elif command == 'help':
            print('List of commands :')
            print('ls                         list of file/folder')
            print('create <filename>          create file')
            print('rm <filename/foldername>   remove file/folder')
            print('append <filename> <text>   append text to file content')
            print('cat <filename>             print file content')
            print('connect <server uri>       connect to other node')
            print('use <server uri>           use specific node for file server')
            print('stat <server uri>          show list of connected node')
