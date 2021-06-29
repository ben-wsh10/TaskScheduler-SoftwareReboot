import subprocess
import logging

import FrontEnd.UserInterface as UI

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

taskType, taskPeriod, taskName, taskPath, taskTime = "", "", "", "", ""


def startLogging():
    formatter = logging.Formatter('%(levelname)s : %(asctime)s : %(message)s')
    fileHandler = logging.FileHandler('LogFile.log')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)


def createTask():
    try:
        cmdLine = 'SCHTASKS /{taskType} /SC {taskPeriod} /TN {taskName} /TR {taskPath} /ST {taskTime}'\
                .format(taskType=taskType, taskPeriod="", taskName="", taskPath="", taskTime="")
        # subprocess.call(['start', 'cmd', '/k', cmdLine], shell=True)
        # __logger.info("Successfully written scheduled task")
    except Exception as e:
        print(e)
        logger.exception("Unable to create scheduled task")

