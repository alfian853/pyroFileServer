import Pyro4


def setupClient():
    uri = "PYRONAME:greetserver@localhost:8888"
    gserver = Pyro4.Proxy(uri)

    while True:
        commands = input().split(' ', 2)
        command = commands[0]
        if command == 'ls':
            gserver.list()

        elif command == 'create':
            gserver.create(commands[1])

        elif command == 'rm':
            gserver.delete(commands[1])

        elif command == 'append':
            gserver.append(commands[1], commands[2])

        elif command == 'cat':
            gserver.read(commands[1])


if __name__ == '__main__':
    setupClient()
