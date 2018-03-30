from threading import Thread
from queue import Queue, Empty

class NonBlockingSocketReceive:

    def __init__(self, socket):
        '''
        stream: the stream to read from.
                Usually a process' stdout or stderr.
        '''
        self._s = socket
        self._q = Queue()
        self._active = True

        def _populateQueue(socket, queue):
            '''
            Collect lines from 'stream' and put them in 'quque'.
            '''
            while self._active:
                line = socket.recv(64)
                if line:
                    queue.put(line)
                else:
                    raise UnexpectedEndOfStream

        self._t = Thread(target=_populateQueue, args=(self._s, self._q))
        self._t.daemon = True
        self._t.start() #start collecting lines from the stream

    def readline(self, timeout = None):
        try:
            return self._q.get(block = timeout is not None, timeout = timeout)
        except Empty:
            return None

    def close(self):
        try:
            self._active = False
        except SystemExit:
            pass

class UnexpectedEndOfStream(Exception): pass