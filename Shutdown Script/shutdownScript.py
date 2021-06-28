import subprocess

maintenanceReboot = 'shutdown /r /t 5 /c "ScheduledMaintenance"'
subprocess.call(['start', 'cmd', '/c', maintenanceReboot], shell=True)
