import Pyro4

from client_api import FailureDetector
from server_api import ServerApi


class Client:
    def __init__(self, uri, server_die_callback : callable):
        self.die_callback = server_die_callback
        self.server_api: ServerApi = Pyro4.Proxy(uri)
        failure_detector = FailureDetector(self.set_die)
        failure_detector.start()
        client_uri: str = failure_detector.get_client_uri().asString()
        self.server_api.set_connected(client_uri)
        self.is_alive = True

    def set_die(self):
        self.is_alive = False
        self.die_callback()

