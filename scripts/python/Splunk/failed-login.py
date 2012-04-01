#!python
import sys
import os
import gzip
import csv
import re

#list of ip addresses that will be sent an alert
iplist = ['192.168.1.33', '192.168.1.7']

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

	#regex to find hostname
	h = re.compile("\[[a-zA-Z]{4}:\ [a-z]*\]")

	r = h.findall(ourdata)
	d = v.findall(ourdata)

	#split up the returned regex to pull out only the username
	username = r[0].split(" ")[1].split("]")[0]

	#store the ip address in a variable
	ip = d[0]
	
	regexerror = "0"
except:
	regexerror = "1"

#run net send with our data
for ipaddr in iplist:
	os.system("net send %s Splunk Alert: Failed Login: Username = %s, IP Address = %s, filepatherror=%s, regexerror=%s" % (ipaddr, username, ip, filepatherror, regexerror))
