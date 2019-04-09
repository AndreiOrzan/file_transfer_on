import sys
import socket
import os



def main():

    host = "127.0.0.1"
    port = 5000 
    
    s = socket.socket()
    s.connect((host,port))
    
    
    print "connected"
    try:
        filename = str(sys.argv[2])
    except:
        print "pass"
    if sys.argv[1] == "get_filelist":
        s.send("get_files")
        file_list = eval(s.recv(1024))
        
        for i in file_list:
            print i
            

    
    if sys.argv[1] == "get":
        
        s.send("get" + str(sys.argv[2]))

        data = s.recv(1024)
        
        if data[:6] =="EXISTS":
            filesize = long(data[6:])
            message = raw_input("File exists," +str(filesize)+\
                                    "Bytes, download? (Y/N)? -> ")
            if message == "Y":
                s.send("OK")
                f = open(filename+"(1)", "wb")
                data = s.recv(1024)
                totalRecv = len(data)
                f.write(data)
                
                while totalRecv < filesize:
                    data = s.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                    print "{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done"
                print "Download Complete!"
                f.close()
        else:
            print "file does not exist!"
            
        s.close()
                
        
        
    if sys.argv[1] == "del":
        s.send("del"+str(sys.argv[2]))
        response = str(s.recv(1024))
        if (response == "EXISTS"):
            data = raw_input("File exists , Delete (Y/N)? ->")
            if data == "Y":
                s.send("Y")
                
    if sys.argv[1] == "send":
        s.send("send"+str(sys.argv[2]))
        serverResponse = s.recv(1024)
        if serverResponse == "ERR":
            print "A file with the same name is allready saved on the server"
        else:
            s.send(str(os.path.getsize(filename)))
            with open(filename, "rb") as f: 
                bytesToSend = f.read(1024)
                s.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    s.send(bytesToSend)

        serverResponse = s.recv(1024)
        print serverResponse
        s.close()
        
        
        
    
    
    
    
    
main()
