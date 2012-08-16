import gntp.notifier
splunk = gntp.notifier.GrowlNotifier(
    applicationName = "Splunk Alerts",
    notifications = ["General","Failed Logins","IPS Alerts", "ACS Lockouts", "Port Security", "High Temp"],
    defaultNotifications = ["General"],
    hostname = "127.0.0.1",
    password = "splunkalertpassword"
)

message = gntp.notifier.GrowlNotifier(
    applicationName = "Chat",
    notifications = ["General"],
    defaultNotifications = ["General"],
    hostname = "127.0.0.1",
    password = "chatpassword"
)

backup = gntp.notifier.GrowlNotifier(
    applicationName = "Backup",
    notifications = ["General","Splunk","SolarWinds"],
    defaultNotifications = ["General"],
    hostname = "127.0.0.1",
    password = "backupPassword"
)

#Do this once and you should never have to do again
splunk.register()

#Do this once and you should never have to do again
message.register()

#Do this once and you should never have to do again
backup.register()