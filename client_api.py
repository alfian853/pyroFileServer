import sched
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
        print('receive heartbeat')
        HeartBeat.last_ping = time.time()

    @staticmethod
    def set_die():
        print('stop heartbeat')
        HeartBeat.is_alive = False


class HeartBeatChecker(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            time.sleep(2)
            print(time.time() - HeartBeat.last_ping)
            if (time.time() - HeartBeat.last_ping) > 2:
                HeartBeat.set_die()
                return


class FailureDetector(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.fd_daemon = Pyro4.Daemon()
        heart_beat = Pyro4.expose(HeartBeat)
        self.client_uri = self.fd_daemon.register(heart_beat)

    def run(self):
        HeartBeatChecker().start()
        self.fd_daemon.requestLoop()

    def get_client_uri(self):
        return self.client_uri

    def is_alive(self):
        return HeartBeat.is_alive

