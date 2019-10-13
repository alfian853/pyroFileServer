import traceback

from Pyro4 import Daemon

from client import Client
from server_api import *
import Pyro4


class Server(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon: Daemon = Pyro4.Daemon()
        x_GreetServer = Pyro4.expose(ServerApi)
        self.uri = self.daemon.register(x_GreetServer).asString()

    def run(self):
        self.daemon.requestLoop()


class ClientHandler:

    def __init__(self):
        self.server_api_dict = {}

    def register(self, uri, server_api: ServerApi):
        self.server_api_dict[uri] = server_api

    def unregister(self, uri):
        del self.server_api_dict[uri]

    def get_server_api(self, uri):
        if not self.server_api_dict.keys().__contains__(uri):
            return None
        return self.server_api_dict[uri]

    def print_info(self):
        for uri in self.server_api_dict.keys():
            print(uri)


if __name__ == '__main__':
    server = Server()
    server.start()
    print('start node uri: \n' + server.uri)
    client_handler = ClientHandler()
    active_server_api: ServerApi = None
    while True:
        commands = input().split(' ', 2)
        command = commands[0]

        if active_server_api is not None:
            if command == 'ls':
                print(active_server_api.list())

            elif command == 'create':
                print(active_server_api.create(commands[1]))

            elif command == 'rm':
                print(active_server_api.delete(commands[1]))

            elif command == 'append':
                print(active_server_api.append(commands[1], commands[2]))

            elif command == 'cat':
                print(active_server_api.read(commands[1]))
        else:
            print('no server used')

        if command == 'connect':
            try:
                uri = commands[1]+""
                die_callback = lambda: client_handler.unregister(uri)
                new_client_server = Client(commands[1], die_callback)
                client_handler.register(commands[1], new_client_server.server_api)
                active_server_api = client_handler.get_server_api(commands[1])
                print('connected to ' + commands[1])
            except:
                traceback.print_exc()
                print('failed connect to ' + commands[1])

        elif command == 'use':
            active_server_api = client_handler.get_server_api(commands[1])
            if active_server_api is not None:
                print('success')

        elif command == 'stat':
            client_handler.print_info()

        elif command == 'help':
            print('List of commands :')
            print('ls                         list of file/folder')
            print('create <filename>          create file')
            print('rm <filename/foldername>   remove file/folder')
            print('append <filename> <text>   append text to file content')
            print('cat <filename>             print file content')
