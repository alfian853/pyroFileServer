from server_api import *
import Pyro4


def start_without_ns():
    daemon = Pyro4.Daemon()
    x_GreetServer = Pyro4.expose(ServerApi)
    uri = daemon.register(x_GreetServer)
    print("my URI : ", uri)
    daemon.requestLoop()


def start_with_ns():
    # name server harus di start dulu dengan  pyro4-ns -n localhost -p 8888
    # untuk mengecek service apa yang ada di ns, gunakan pyro4-nsc -n localhost -p 8888 list
    daemon = Pyro4.Daemon(host="localhost")
    ns = Pyro4.locateNS("localhost", 8888)
    serverClass = Pyro4.expose(ServerApi)
    uri_greetserver = daemon.register(serverClass)
    print("URI greet server : ", uri_greetserver)
    ns.register("greetserver", uri_greetserver)
    daemon.requestLoop()


if __name__ == '__main__':
    start_with_ns()
