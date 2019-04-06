import socket
import threading
import os

def get_files(sock):
    list = os.listdir(os.curdir)
    list.remove("fserver.py")
    sock.send(str(list))
    
def del_file(sock,name):
    if os.path.isfile(name):
        sock.send("EXISTS")
        print "test"
        userResponse = sock.recv(1024)
        
        if userResponse == "Y":
            os.remove(name)
    #find file and send exists 

def Retrfile(filename,sock):#sending file from the server to the client

    if os.path.isfile(filename):
        sock.send("EXISTS " + str(os.path.getsize(filename)))
        userResponse = sock.recv(1024)
        if userResponse[:2] == "OK" :
            with open(filename, "rb") as f: 
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
    else:
        sock.send("ERR ")
        
    sock.close()
    
def send_file(sock,filename):# file transfered from the client to the server.

    if os.path.isfile(filename):
        sock.send("ERR")
        print "message send: ERR"#
    else:
        sock.send("ok")
        data = sock.recv(1024)
        print data
        filesize = long(data)
        f = open(filename, "wb")
        data = sock.recv(1024)
        totalRecv = len(data)
        f.write(data)
            
        while totalRecv < filesize:
            data = sock.recv(1024)
            totalRecv += len(data)
            f.write(data)
            print "{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done"
        sock.send("File send succesfully!")
        f.close()

        
    sock.close()
    
def handle(name,sock):
    code = sock.recv(1024)
    print code
    if code == "get_files":
        get_files(sock)
    if code[:3] =="get":
        filename = code[3:]
        Retrfile(filename,sock)
    if code[:3] == "del":
        name = code[3:]
        del_file(sock,name)
    if code[:4] == "send":
        name = code[4:]
        send_file(sock,name)
        



def main():
    host ="127.0.0.1"
    port = 5000
    
    s = socket.socket()
    s.bind((host,port))
    
    s.listen(5)
    
    print "server operational"
    while True:
        c,addr = s.accept()
        print "client connected ip :<" +str(addr) + ">"
        t = threading.Thread(target=handle, args=("Name",c))
        t.start()
        
    s.close()    
    
main()