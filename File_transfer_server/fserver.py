import socket ,mysql.connector 
import threading
import os

def cursor_sql(command,file_details):
    mydb = mysql.connector.connect(host = "localhost",user = "root",password = "November21!",database = "file_share")
    my_cursor = mydb.cursor()
    
    if command =="upload":
        #insert_sql(file_details)
        print "upload"
        sqlstuff = "INSERT INTO test (filename , size ,  downloads) VALUES (%s,%s,%s)" 
        my_cursor.execute(sqlstuff ,(file_details))
        mydb.commit()
    if command =="remove":
        print "remove"
        my_sql = "DELETE FROM test WHERE filename = %s"
        my_cursor.execute(my_sql,(file_details,))
        mydb.commit()
    if command == "modify" :
        print file_details
        
        sql_com = "SELECT downloads = downloads + 1  FROM test WHERE filename = %s"
        my_cursor.execute(sql_com,(file_details,))
        mydb.commit()

def get_files(sock):
    list = os.listdir(os.curdir)
    list.remove("fserver.py")
    sock.send(str(list))
    # change this to pull the table from the SQL server 

    
def del_file(sock,name):
    if os.path.isfile(name):
        sock.send("EXISTS")
        print "test"
        userResponse = sock.recv(1024)
        
        if userResponse == "Y":
            os.remove(name)
            cursor_sql("remove",name)
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
                    cursor_sql("modify",filename)
    else:
        sock.send("ERR ")
        
        
        
def send_file(sock,filename):# file transfered from the client to the server.
    
    if os.path.isfile(filename): #and len(filename)<??
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
        cursor_sql("upload",[filename,filesize,0])
        


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
    sock.close()



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

""" bug report :
1 script crashes if the client attempts to send file that does not exist in the fclient folder 
2 cannot modify file send from client to server while script is running (f.close on server?)
3 send file from client must be !=0
4 the position column does not update after removing a file SQL """