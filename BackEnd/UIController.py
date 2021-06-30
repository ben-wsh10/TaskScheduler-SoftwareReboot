import os
import subprocess
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from pathlib import Path

taskType, taskPeriod, taskName, taskPath, taskTime = "", "", "", os.path.abspath("shutdownScript.exe"), ""
radioCriteria, timeCriteria, nameCriteria = False, False, False
cmdLine = ""
dailyList = ["-"]
weekList = ["Select a Day", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
# weekListConversion = ["MON", "TUES", "WED", "THU", "FRI", "SAT", "SUN"]
monthList = ["Select a date",
             "1st Day of the Month", "2nd Day of the Month", "3rd Day of the Month",
             "4th Day of the Month", "5th Day of the Month", "6th Day of the Month",
             "7th Day of the Month", "8th Day of the Month", "9th Day of the Month",
             "10th Day of the Month", "11th Day of the Month", "12th Day of the Month",
             "13th Day of the Month", "14th Day of the Month", "15th Day of the Month",
             "16th Day of the Month", "17th Day of the Month", "18th Day of the Month",
             "19th Day of the Month", "20th Day of the Month", "21st Day of the Month",
             "22nd Day of the Month", "23rd Day of the Month", "24th Day of the Month",
             "25th Day of the Month", "26h Day of the Month", "27th Day of the Month",
             "28th Day of the Month", "29th Day of the Month", "30th Day of the Month",
             "31st Day of the Month",
             ]


# monthListConversion = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
#                        27, 28, 29, 30, 31]


def startLogging():
    formatter = logging.Formatter('%(levelname)s : %(asctime)s : %(message)s')
    fileHandler = logging.FileHandler('LogFile.log')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)


def updateCmdLine():
    global cmdLine

    cmdLine = r'SCHTASKS /{taskType} /SC {taskPeriod} /TN {taskName} /TR {taskPath} /ST {taskTime}' \
        .format(taskType=taskType, taskPeriod=taskPeriod, taskName=taskName, taskPath=taskPath, taskTime=taskTime)

    return cmdLine


def createTask():
    global cmdLine

    try:
        # cmdLine = 'SCHTASKS /CREATE /SC DAILY /TN test /TR "D:\\Coding\\Python\\TSSR\\ShutdownScript\\shutdownScript.exe" /ST 17:42'
        # cmdLine = 'SCHTASKS /CREATE /SC DAILY /TN test /TR "C:Users\\benwu\\Desktop\\FinalYearProject-master\\Main.py.exe" /ST 17:44'
        subprocess.call(['start', 'cmd', '/k', cmdLine], shell=True)
        # __logger.info("Successfully written scheduled task")
    except Exception as e:
        print(e)
        logger.exception("Unable to create scheduled task")

createTask()