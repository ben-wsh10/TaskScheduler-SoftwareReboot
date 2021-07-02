import csv
import os
import subprocess
import logging

from tempfile import NamedTemporaryFile
import shutil

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

taskType, taskPeriod, taskName, taskPath, taskTime = "", "", "", os.path.abspath(
    "shutdownScript.exe"), ""
periodCriteriaC, timeCriteriaC, nameCriteriaC = False, False, False
timerCriteriaU = False
nameCriteriaD = False
cmdLineC = ""
cmdLineU = ""
cmdLineD = ""

csvFileName = "data.csv"
csvField = ["taskName", "taskPeriod", "taskTime"]
taskNameList, taskPeriodList, taskTimeList = [], [], []

periodList = ["-", "Minute", "Hourly", "Daily", "Weekly", "Monthly"]

minuteList = ["Select a minute",
              "1 minute", "2 minutes", "3 minute", "4 minute", "5 minute",
              "10 minutes", "15 minutes", "20 minutes", "25 minutes", "30 minutes",
              "35 minutes", "40 minutes", "45 minutes", "50 minutes", "55 minutes"
              ]
hourlyList = ["Select an hour",
              "1 hour", "2 hour", "3 hour", "4 hour", "5 hour", "6 hour", "7 hour", "8 hour",
              "9 hour", "10 hour", "11 hour", "12 hour", "13 hour", "14 hour", "15 hour", "16 hour",
              "17 hour", "18 hour", "19 hour", "20 hour", "21 hour", "22 hour", "23 hour",
              ]
dailyList = ["-"]
weekList = ["Select a Day", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
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


def startLogging():
    formatter = logging.Formatter('%(levelname)s : %(asctime)s : %(message)s')
    fileHandler = logging.FileHandler('LogFile.log')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)


def newCSV():
    try:
        fileExists = os.path.isfile(csvFileName)
        with open(csvFileName, 'a', encoding='utf-8') as csvFile:
            csvWriter = csv.writer(csvFile)

            if not fileExists:
                csvWriter.writerow(csvField)
            else:
                pass

    except:
        logger.exception("Create CSV error.")


def createCSV(rTaskName, rTaskPeriod, rTaskTime):
    try:
        with open(csvFileName, 'a+', newline='', encoding='utf-8') as csvFile:
            row = [rTaskName, rTaskPeriod, rTaskTime]
            write = csv.writer(csvFile)
            write.writerow(row)
    except:
        logger.exception("Write CSV error.")


def updateCSV(rTaskName, rTaskTime):
    try:
        tempfile = NamedTemporaryFile('w+t', newline='', delete=False)
        with open(csvFileName, 'r', newline='') as csvFile, tempfile:
            reader = csv.reader(csvFile, delimiter=',')
            writer = csv.writer(tempfile, delimiter=',')
            for row in reader:
                if len(row) == 0:
                    writer.writerow(row)
                elif row[0] == "taskName" and row[1] == "taskPeriod" and row[2] == "taskTime":
                    writer.writerow(row)
                elif row[0] == rTaskName:
                    tmp = row
                    tmp[2] = rTaskTime
                    writer.writerow(row)
                else:
                    writer.writerow(row)
        shutil.move(tempfile.name, csvFileName)
    except:
        logger.exception("update CSV error.")


def deleteCSV(rTaskName):
    try:
        tempfile = NamedTemporaryFile('w+t', newline='', delete=False)
        with open(csvFileName, 'r', newline='') as csvFile, tempfile:
            reader = csv.reader(csvFile, delimiter=',')
            writer = csv.writer(tempfile, delimiter=',')
            for row in reader:
                if len(row) == 0:
                    writer.writerow(row)
                elif row[0] == "taskName" and row[1] == "taskPeriod" and row[2] == "taskTime":
                    writer.writerow(row)
                elif row[0] == rTaskName:
                    pass
                else:
                    writer.writerow(row)
        shutil.move(tempfile.name, csvFileName)
    except:
        logger.exception("update CSV error.")


def createCmdLine():
    global cmdLineC

    cmdLineC = r'SCHTASKS /{taskType} /SC {taskPeriod} /TN {taskName} /TR {taskPath} /ST {taskTime}' \
        .format(taskType=taskType, taskPeriod=taskPeriod, taskName=taskName, taskPath=taskPath, taskTime=taskTime)

    return cmdLineC


def updateCmdLine():
    global cmdLineU
    cmdLineU = r'SCHTASKS /{taskType} /TN {taskName} /ST {taskTime}' \
        .format(taskType=taskType, taskName=taskName, taskTime=taskTime)

    return cmdLineU


def deleteCmdLine():
    global cmdLineD
    cmdLineD = r'SCHTASKS /{taskType} /TN {taskName} /f' \
        .format(taskType=taskType, taskName=taskName)

    return cmdLineD


def createTask():
    global cmdLineC

    try:
        # subprocess.call(['start', 'cmd', '/k', cmdLineC], shell=True)
        # __logger.info("Successfully written scheduled task")
        subprocess.run(cmdLineC, shell=True)
    except Exception as e:
        print(e)
        logger.exception("Unable to create scheduled task")


def updateTask():
    global cmdLineU

    try:
        subprocess.call(['start', 'cmd', '/k', cmdLineU], shell=True)
        # __logger.info("Successfully written scheduled task")
    except Exception as e:
        print(e)
        logger.exception("Unable to update scheduled task")


def deleteTask():
    global cmdLineD

    try:
        subprocess.call(['start', 'cmd', '/k', cmdLineD], shell=True)

    except Exception as e:
        print(e)
        logger.exception("Unable to delete scheduled task")
