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
		gsend.notify(noteType = growl_nt, title = growl_title, description = growl_des, sticky = False, priority = 1)
	except:
		pass

title = "IPS Alert"
note_type = "IPS Alerts"
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

	#regex to find hostname
	d = re.compile("description=\"(.*?)\"")
	a = re.compile("attacker=\"(.*?)\"")
	t = re.compile("target=\"(.*?)\"")

	r1 = d.findall(ourdata)
	r2 = a.findall(ourdata)
	r3 = t.findall(ourdata)

	#split up the returned regex to pull out only the username
	description = r1[0]
	attacker = r2[0]
	
	targets = "[ "
	for tr in r3:
		targets += tr + " "
		
	targets += "]"
	
	
	regexerror = "0"
except:
	regexerror = "1"

#run net send with our data
for ipaddr in iplist:
	if attacker == "172.16.11.4":
		note = "Erik's probably doing testing."
	elif attacker == "172.16.11.3":
		note = "Kevin's probably doing testing."
	else:
		note = "Possible real threat."
		
	des = "Signature: %s\n\nAttacker: %s\nTargets: %s\n\n%s" % (description, attacker, targets, note)
	notify(ipaddr, app_name, notif, def_notif, passw, title, des, note_type)