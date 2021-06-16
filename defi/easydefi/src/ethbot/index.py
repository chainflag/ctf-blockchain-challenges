import sys
import os
from conf.base import alarmsecs, workdir
import signal
import codecs
from src.main import main


class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)

sys.path.append(workdir)
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stdout = Unbuffered(sys.stdout)
signal.alarm(alarmsecs)
os.chdir(workdir)
main()