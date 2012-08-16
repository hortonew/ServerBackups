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

title = "ACS Lockout"
note_type = "ACS Lockouts"
app_name = "Splunk Alerts"
notif = ["General","Failed Logins","IPS Alerts", "Port Security", "High Temp"]
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

	#regex to find hostname
	h = re.compile("UserName+.[a-zA-Z]*")

	r = h.findall(ourdata)

	#split up the returned regex to pull out only the username
	username = r[0]
	
	regexerror = "0"
except:
	regexerror = "1"

#run net send with our data
for ipaddr in iplist:
	des = username
	notify(ipaddr, app_name, notif, def_notif, passw, title, des, note_type)