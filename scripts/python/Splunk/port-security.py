#!python
import sys
import os
import gzip
import csv
import re

#list of ip addresses that will be sent an alert
iplist = ['192.168.1.33', '192.168.1.7', '192.168.1.5']

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
	pn = re.compile("((Gigabit|Fast)Ethernet[\d/]{3,6})");
	
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
	os.system("net send %s Splunk Alert: Port Security: IP Address = %s, MAC = %s, Port = %s, filepatherror=%s, regexerror=%s" % (ipaddr, ip, mac, port, filepatherror, regexerror))
