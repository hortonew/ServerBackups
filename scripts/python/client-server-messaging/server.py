import socket
import win32api

UDP_IP="192.168.1.100" #Change to your own IP
UDP_PORT=1337

sock = socket.socket( socket.AF_INET, # Internet
                      socket.SOCK_DGRAM ) # UDP
sock.bind( (UDP_IP,UDP_PORT) )

while True:
    data, addr = sock.recvfrom( 1024 ) # buffer size is 1024 bytes
    win32api.MessageBox(0, data, "Alert from the Client", 0x00001000) 
