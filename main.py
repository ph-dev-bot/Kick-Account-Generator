import threading
from Utils.temps_mail import *
from Utils.generator import *


class GenerateThread(threading.Thread):
    def run(self):
        while True:
            Generate()


def launch_generate_threads(num_threads):
    threads = []
    for _ in range(num_threads):
        thread = GenerateThread()
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


num_threads = int(input("Entrez le nombre de threads: "))

launch_generate_threads(num_threads)
