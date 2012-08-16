#!python
import sys
import os
import gzip
import csv
import re
import gntp.notifier

#list of ip addresses that will be sent an alert
iplist = ['ip.xx.xx.xx']

def notify(growl_ip, growl_app_name, growl_notif, growl_def_notif, growl_pass, growl_title, growl_des, growl_nt):
	gsend = gntp.notifier.GrowlNotifier(applicationName = growl_app_name, notifications = growl_notif, defaultNotifications = growl_def_notif, hostname = growl_ip, password = growl_pass)
	try:
		gsend.register()
		gsend.notify(noteType = growl_nt, title = growl_title, description = growl_des, sticky = True, priority = 1)
	except:
		pass

title = "Port Security"
note_type = "Port Security"
app_name = "Splunk Alerts"
notif = ["General","Failed Logins","IPS Alerts", "ACS Lockouts", "Port Security", "High Temp"]
def_notif = ["General"]
passw = "splunkalertpassword"

try:
	mypath = r"C:\Program Files\Splunk\var\run\splunk\dispatch"
	mypath += "\\" #add backslash for file path
	
	#concatenate our path to the log folders + the correct folder for this log, + results.csv.gz 
	results = mypath + sys.argv[8].split('\\')[-3] + "\\results.csv.gz"

	filepatherror="0"
except:
	filepatherror="1"

try:
	#extracts the .gz file
	ogz = gzip.open(results)

	for row in csv.DictReader(ogz):
		ourdata = row['_raw']

	#regex to find ip address
	v = re.compile("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+");
	
	#regex to find mac address  (af00.ffff.ee12)
	m = re.compile("[a-f0-9]{4}\.[a-f0-9]{4}\.[a-f0-9]{4}");
	
	#regex to find port
	pn = re.compile("((Gigabit|Fast|TenGigabit)Ethernet[\d/]{3,6})");
	
	#find all matches for ip, mac, port
	d = v.findall(ourdata)
	mc = m.findall(ourdata)
	pt = pn.findall(ourdata)

	#store the first result of each in a variable
	ip = d[0]
	mac = mc[0]
	port = pt[0][0]
	
	regexerror = "0"
except:
	regexerror = "1"

#run net send with our data
for ipaddr in iplist:
	des = "IP: %s\nMAC: %s\nPort: %s" % (ip, mac, port)
	notify(ipaddr, app_name, notif, def_notif, passw, title, des, note_type)