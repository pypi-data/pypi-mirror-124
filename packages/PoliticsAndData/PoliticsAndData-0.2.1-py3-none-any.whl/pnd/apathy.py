from pnd.specific import *
from pnd import Boredom
import threading


class Apathy:
    def __init__(self, types: tuple[Boredom] = (Alliances, Cities, Nations)):
        self.threads = []

        for T in types:
            thing = T()
            self.threads.append(threading.Thread(target=thing.run, daemon=True, name=T.__name__))

    def run(self):
        for thread in self.threads:
            thread.run()
        for thread in self.threads:
            thread.join()

        # combination placeholder
