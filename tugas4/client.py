import Pyro4

namainstance = "fileserver-1"

def get_fileserver_object():
    uri = "PYRONAME:{}@localhost:7777" . format(namainstance)
    fserver = Pyro4.Proxy(uri)
    return fserver

if __name__=='__main__':
    f = get_fileserver_object()


    while True:
        commands = input().split(' ', 2)
        command = commands[0]

        if command == 'ls':
            f.list()

        elif command == 'create':
            f.create(commands[1])

        elif command == 'rm':
            f.delete(commands[1])

        elif command == 'update':
            commands = commands[1].split(' ')
            f.update(commands[0], commands[1])

        elif command == 'read':
            f.read(commands[1])
