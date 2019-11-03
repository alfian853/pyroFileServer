import Pyro4

namainstance = "fileserver-2"

def get_fileserver_object():
    uri = "PYRONAME:{}@localhost:7777" . format(namainstance)
    fserver = Pyro4.Proxy(uri)
    return fserver

if __name__=='__main__':
    f = get_fileserver_object()


    while True:
        commands = input().split(' ', 1)
        command = commands[0]
        print(commands)
        if command == 'ls':
            print(f.list())

        elif command == 'create':
            print(f.create(commands[1]))

        elif command == 'delete':
            print(f.delete(commands[1]))

        elif command == 'update':
            commands = commands[1].split(' ')
            print(f.update(commands[0], commands[1]))

        elif command == 'read':
            print(f.read(commands[1]))
