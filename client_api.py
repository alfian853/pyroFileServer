import threading
import time

import Pyro4


class HeartBeat:
    failure_detector = None
    is_alive = True
    last_ping = time.time()
    event = None

    @staticmethod
    def set_alive():
        HeartBeat.last_ping = time.time()
        return "yes"

    @staticmethod
    def set_die():
        HeartBeat.is_alive = False


class HeartBeatChecker(threading.Thread):

    def __init__(self, server_die_callback):
        threading.Thread.__init__(self)
        self.server_die_callback = server_die_callback

    def run(self):
        while True:
            time.sleep(2)
            if (time.time() - HeartBeat.last_ping) > 2:
                HeartBeat.set_die()
                self.server_die_callback()
                return


class FailureDetector(threading.Thread):

    def __init__(self, server_die_callback):
        threading.Thread.__init__(self)
        self.server_die_callback = server_die_callback
        self.fd_daemon = Pyro4.Daemon()
        heart_beat = Pyro4.expose(HeartBeat)
        self.client_uri = self.fd_daemon.register(heart_beat)

    def run(self):
        HeartBeatChecker(self.server_die_callback).start()
        self.fd_daemon.requestLoop()

    def get_client_uri(self):
        return self.client_uri

    def is_alive(self):
        return HeartBeat.is_alive

