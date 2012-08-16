import sys
import gntp.notifier
import socket

try:
	my_ip = socket.gethostbyname(socket.gethostname())
except:
	my_ip = "127.0.0.1"

if my_ip == "ip.xx.xx.xx":
	title = "Message from Me"
else:
	title = "Message from Unknown"
	
if len(sys.argv) < 3:
	sys.exit('\nUsage: %s ip1,ip2,ip3 message. \n\nNote: There should be no spaces between the list of IP addresses.\n\nUse * instead of IP addresses to send to all devices.' % sys.argv[0])

if sys.argv[1] != "*":
	ips = sys.argv[1].split(',')
else:
	ips = ['ip.xx.xx.xx, ip2.xx.xx.xx, ip3.xx.xx.xx']
mesg = []
for i in range(2, len(sys.argv)):
	mesg.append(sys.argv[i])

msg_joined = ' '.join(mesg)

def sendMsg(ip, msg, msg_title):
	aronmessage = gntp.notifier.GrowlNotifier(
		applicationName = "Chat",
		notifications = ["General"],
		defaultNotifications = ["General"],
		hostname = ip,
		password = "chatpassword"
	)
	try:
		aronmessage.register()
		aronmessage.notify(
			noteType = "General",
			title = msg_title,
			description = msg,
			sticky = True,
			priority = 1,
		)
		print "Sent", ip, "a message."
	except:
		print "Tried sending", ip, "a message, but failed. "

for ip in ips:
	sendMsg(ip, msg_joined, title)
