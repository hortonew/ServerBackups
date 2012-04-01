import socket
import sys

try:
	sysmessage = str(sys.argv[1])
except:
	sysmessage = "Client Alert"

class Client(object):
	def __init__(self):
		global UDP_IP
		global UDP_PORT
		UDP_IP="192.168.1.200"
		UDP_PORT=1337
	
	def sendmsg(self, msg):
		global UDP_IP
		global UDP_PORT
		sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		sock.sendto( str(msg), (UDP_IP, UDP_PORT) )

message = Client()
#message.sendmsg("Login Failure: Someone can't type correctly.")
message.sendmsg(sysmessage)
