import subprocess
import logging

# Logging information
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s : %(asctime)s : %(message)s')
fileHandler = logging.FileHandler('LogFile.log')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

try:
    test = 'SCHTASKS /CREATE /SC DAILY /TN task /TR "C:Users\\benwu\\Desktop\\FinalYearProject-master\\Main.exe" /ST 15:38'
    # maintenanceReboot = 'shutdown /r /t 5 /c "Scheduled Maintenance"'
    subprocess.call(['start', 'cmd', '/k', test], shell=True)
    logger.info("Successfully written scheduled task")
except Exception as e:
    print(e)
    logger.exception("Unable to create scheduled task")
