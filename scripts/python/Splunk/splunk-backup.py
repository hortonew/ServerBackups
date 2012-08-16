#!python
import shutil
import datetime
import os
import gntp.notifier

# List of IP Addresses to receive growl notification upon backup completion
iplist = ['ip.xx.xx.xx']

# Sends growl notification
def notify(ip, growl_app_name, growl_notif, growl_def_notif, growl_pass, growl_title, growl_des, growl_nt):
	gsend = gntp.notifier.GrowlNotifier(applicationName = growl_app_name, notifications = growl_notif, defaultNotifications = growl_def_notif, hostname = ip, password = growl_pass)
	try:
		gsend.register()
		gsend.notify(noteType = growl_nt, title = growl_title, description = growl_des, sticky = True, priority = 1)
	except:
		pass

# Settings for growl notification	
title = "Splunk Backup Complete"
des = "Splunk finished backing up to the share"
note_type = "Splunk"
app_name = "Backup"
notif = ["General","Splunk","SolarWinds"]
def_notif = ["General"]
passw = "backupPassword"

# Back up directories
def backup(s_path, d_path, db_list, is_tree):
    src_path = s_path + "\\"
    dst_path = d_path + "\\" + str(datetime.date.today())
    if not os.path.exists(dst_path):
            os.makedirs(dst_path)
    #f = open(dst_path + str(datetime.date.today()) + ".txt", "w")
    for db in db_list:
        path = src_path + db
        dstpath = dst_path + "\\" + db
        print "Backing up: " + path + " to: " + dstpath
        #f.write("Added: %s\n" % db)
        if is_tree:
            shutil.copytree(path, dstpath)
        else:
            shutil.copyfile(path, dstpath)
    #f.close()

databases = [
r"audit\db",
r"blockSignature\db",
r"_internaldb\db",
r"fishbucket\db",
r"historydb\db",
r"defaultdb\db",
]

scripts = [
r"acs-account-lockout.py",
r"aron_911.py",
r"failed-login.py",
r"ips-signature.py",
r"port-security.py",
r"high-temp.py",
]

backup(r"C:\Program Files\Splunk\bin\scripts", r"Z:\BackupsFolder\Splunk\Scripts", scripts, False)
backup(r"C:\Program Files\Splunk\var\lib\splunk", r"Z:\BackupsFolder\Splunk\Databases", databases, True)
for ip in iplist:
	notify(ip, app_name, notif, def_notif, passw, title, des, note_type)