import socket  
import pdb
 
host='127.0.0.1'  
host='10.129.232.39'
host='10.134.113.75'
port=50000 
BUFFER=4096  
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
sock.connect((host,port))  
sock.send('hello, tcpServer!')  
recv=sock.recv(BUFFER)  
print('[tcpServer said]: %s' % recv)  
pdb.set_trace()
sock.close() 

print "hello ok"
