import socket                   # Import socket module

s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
port = 60000                    # Reserve a port for your service.

s.connect((host, port))

filename='data.txt'
f = open(filename,'rb')
l = f.read(1024)
while (l):
   s.send(l)
   l = f.read(1024)
f.close()

print('Done sending')
s.close()
print('connection closed')