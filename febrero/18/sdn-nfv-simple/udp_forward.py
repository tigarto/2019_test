import socket

UDP_IP = "10.0.0.3"
UDP_PORT = 5005
 
UDP_IP2 = "10.0.0.2"
UDP_PORT2 = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.bind((UDP_IP, UDP_PORT))
sock2 = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "received message:", data
    sock2.sendto(data, (UDP_IP2, UDP_PORT2))  #duplicate the received packets and send the packets to H2
    sock2.sendto(data, (UDP_IP2, UDP_PORT2))


