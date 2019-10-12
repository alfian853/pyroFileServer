import Pyro4

from client_api import FailureDetector
from server_api import ServerApi


def run_client():
    uri = "PYRONAME:greetserver@localhost:8888"
    server: ServerApi = Pyro4.Proxy(uri)
    failure_detector = FailureDetector()
    failure_detector.start()
    client_uri: str = failure_detector.get_client_uri().asString()
    server.set_connected(client_uri)

    if not failure_detector.is_alive():
        print('server is down')
        return

    while True:
        commands = input().split(' ', 2)
        command = commands[0]
        if not failure_detector.is_alive():
            print('server is down')
            break

        if command == 'ls':
            print(server.list())

        elif command == 'create':
            print(server.create(commands[1]))

        elif command == 'rm':
            print(server.delete(commands[1]))

        elif command == 'append':
            print(server.append(commands[1], commands[2]))

        elif command == 'cat':
            print(server.read(commands[1]))

        elif command == 'help':
            print('List of commands :')
            print('ls                         list of file/folder')
            print('create <filename>          create file')
            print('rm <filename/foldername>   remove file/folder')
            print('append <filename> <text>   append text to file content')
            print('cat <filename>             print file content')


if __name__ == '__main__':
    run_client()
