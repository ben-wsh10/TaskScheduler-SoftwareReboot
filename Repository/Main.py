import re
import sys

from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QApplication, QMainWindow

from UserInterface import Ui_MainWindow
import UIController as UIC


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        # Set up User Interface
        QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)

        UIC.startLogging()
        UIC.createCSV()
        UIC.taskType = "CREATE"
        self.realTimeUpdates()
        self.initialiseObject()

    # Initialise objects
    def initialiseObject(self):
        self.initialiseTabs()
        self.initialiseButtons()
        self.initialiseField()
        self.initialiseMenu()

    # Initialise tabs
    def initialiseTabs(self):
        self.tabWidget.currentChanged.connect(self.tabChanged)

    def initialiseButtons(self):
        # Push Buttons
        self.cudButton.setText("Create")
        self.cudButton.setEnabled(False)
        self.cudButton.clicked.connect(lambda: self.triggerCUDBtn())
        # QTimeEdit
        self.timePeriod.setTime(QTime(0, 0))
        self.timePeriod2.setTime(QTime(0, 0))
        self.timePeriod.timeChanged.connect(lambda: self.periodTimeChanged())
        self.timePeriod2.timeChanged.connect(lambda: self.periodTimeChanged())

    def initialiseField(self):
        # QLineEdit
        self.lineTaskName.textChanged.connect(lambda: self.taskNameChanged())
        self.labelTaskName.setText("-")
        self.labelPeriod.setText("-")

    def initialiseMenu(self):
        self.dropDownSchedule.addItems(UIC.periodList)
        # DropdownScheduler
        self.dropDownSchedule.currentTextChanged.connect(lambda: self.periodMenuChanged())
        # Combo box
        self.dropDownPeriod.currentTextChanged.connect(lambda: self.periodValue())
        self.dropDownTaskName.currentTextChanged.connect(lambda: self.populateUpdateData())

    def resetDefault(self):
        # reset dropdown menu
        UIC.taskPeriod = ""
        self.dropDownSchedule.setCurrentIndex(0)
        self.dropDownPeriod.clear()
        self.dropDownPeriod.addItem("-")
        # reset task name
        self.lineTaskName.setText("")
        UIC.taskName = ""
        # reset task time
        self.timePeriod.setTime(QTime(0, 0))
        self.timePeriod2.setTime(QTime(0, 0))
        UIC.taskTime = str("{:02}".format(self.timePeriod.time().hour())) + ":" + str(
            "{:02}".format(self.timePeriod.time().minute()))
        # reset labelcmdline
        self.realTimeUpdates()
        # Reset criteria
        UIC.periodCriteriaC, UIC.timeCriteriaC, UIC.nameCriteriaC = False, False, False
        # reset createButton
        self.cudButton.setEnabled(False)

    # Get task type
    def tabChanged(self):
        if self.tabWidget.currentIndex() == 0:
            UIC.taskType = "CREATE"
            self.cudButton.setText("Create")
            UIC.logger.info("CREATE Tab is selected.")
        elif self.tabWidget.currentIndex() == 1:
            UIC.taskType = "CHANGE"
            self.cudButton.setText("Update")
            self.readTask()
            UIC.logger.info("UPDATE Tab is selected.")
        elif self.tabWidget.currentIndex() == 2:
            UIC.taskType = "DELETE"
            self.cudButton.setText("Delete")
            UIC.logger.info("DELETE Tab is selected.")
        self.resetDefault()
        self.realTimeUpdates()


    # Get task period
    def periodMenuChanged(self):
        if self.dropDownSchedule.currentText() == "Minute":
            UIC.taskPeriod = "MINUTE"
            self.minuteComboBox()
            UIC.logger.info("MINUTE Period is selected.")
        elif self.dropDownSchedule.currentText() == "Hourly":
            UIC.taskPeriod = "HOURLY"
            self.hourlyComboBox()
            UIC.logger.info("HOURLY Period is selected.")
        elif self.dropDownSchedule.currentText() == "Daily":
            UIC.taskPeriod = "DAILY"
            self.dailyComboBox()
            UIC.logger.info("Daily Period is selected.")
        elif self.dropDownSchedule.currentText() == "Weekly":
            UIC.taskPeriod = "WEEKLY"
            self.weeklyComboBox()
            UIC.logger.info("Weekly Period is selected.")
        elif self.dropDownSchedule.currentText() == "Monthly":
            UIC.taskPeriod = "MONTHLY"
            self.monthlyComboBox()
            UIC.logger.info("Monthly Period is selected.")
        self.realTimeUpdates()


    def minuteComboBox(self):
        self.dropDownPeriod.clear()
        self.dropDownPeriod.addItems(UIC.minuteList)

    def hourlyComboBox(self):
        self.dropDownPeriod.clear()
        self.dropDownPeriod.addItems(UIC.hourlyList)

    # Get daily drop down menu
    def dailyComboBox(self):
        self.dropDownPeriod.clear()
        self.dropDownPeriod.addItems(UIC.dailyList)

    # Get weekly drop down menu
    def weeklyComboBox(self):
        self.dropDownPeriod.clear()
        self.dropDownPeriod.addItems(UIC.weekList)

    # Get weekly drop down menu
    def monthlyComboBox(self):
        self.dropDownPeriod.clear()
        self.dropDownPeriod.addItems(UIC.monthList)

    # Get task period's day/date
    def periodValue(self):
        if self.dropDownSchedule.currentText() == "Minute":
            if self.dropDownPeriod.currentIndex() != 0 and self.dropDownPeriod.currentIndex() != -1:
                UIC.taskPeriod = "MINUTE"
                UIC.taskPeriod = UIC.taskPeriod + " /MO " + str(
                    re.search(r'\d+', self.dropDownPeriod.currentText()).group())
            else:
                UIC.taskPeriod = "MINUTE"
        elif self.dropDownSchedule.currentText() == "Hourly":
            if self.dropDownPeriod.currentIndex() != 0 and self.dropDownPeriod.currentIndex() != -1:
                UIC.taskPeriod = "HOURLY"
                UIC.taskPeriod = UIC.taskPeriod + " /MO " + str(
                    re.search(r'\d+', self.dropDownPeriod.currentText()).group())
                print(UIC.taskPeriod)
            else:
                UIC.taskPeriod = "HOURLY"
        elif self.dropDownSchedule.currentText() == "Daily":
            # print(UIC.taskPeriod)
            pass
        elif self.dropDownSchedule.currentText() == "Weekly":
            if self.dropDownPeriod.currentIndex() != 0 and self.dropDownPeriod.currentIndex() != -1:
                UIC.taskPeriod = "WEEKLY"
                UIC.taskPeriod = UIC.taskPeriod + " /D " + self.dropDownPeriod.currentText()[:3]
                # print(UIC.taskPeriod)
                UIC.logger.info("Day is selected.")
            else:
                UIC.taskPeriod = "WEEKLY"
        elif self.dropDownSchedule.currentText() == "Monthly":
            if self.dropDownPeriod.currentIndex() != 0 and self.dropDownPeriod.currentIndex() != -1:
                UIC.taskPeriod = "MONTHLY"
                UIC.taskPeriod = UIC.taskPeriod + " /D " + str(
                    re.search(r'\d+', self.dropDownPeriod.currentText()).group())
                # print(UIC.taskPeriod)
                UIC.logger.info("Date is selected.")
            else:
                UIC.taskPeriod = "MONTHLY"
        self.realTimeUpdates()

    # Get time valuetime
    def periodTimeChanged(self):
        if self.tabWidget.currentIndex() == 0:
            UIC.taskTime = str("{:02}".format(self.timePeriod.time().hour())) + ":" + str(
                "{:02}".format(self.timePeriod.time().minute()))
        elif self.tabWidget.currentIndex() == 1:
            UIC.taskTime = str("{:02}".format(self.timePeriod2.time().hour())) + ":" + str(
                "{:02}".format(self.timePeriod2.time().minute()))
        self.realTimeUpdates()
        # print(UIC.taskTime)
        UIC.logger.info("Time is selected/changed.")

    # Get task name
    def taskNameChanged(self):
        UIC.taskName = self.lineTaskName.text()
        self.realTimeUpdates()
        # print(UIC.taskName)

    def realTimeUpdates(self):
        self.updateLabelCmdLine()
        self.createTaskCriteria()
        self.updateTaskCriteria()

    # Update cmdLine label
    def updateLabelCmdLine(self):
        if self.tabWidget.currentIndex() == 0:
            self.labelCmdLine.setText(UIC.createCmdLine())
        elif self.tabWidget.currentIndex() == 1:
            self.labelCmdLine.setText(UIC.updateCmdLine())
        self.labelNewTime.setText(UIC.taskTime)

    def createTaskCriteria(self):
        # Period Criteria
        if self.dropDownSchedule.currentText() == "Minute" or self.dropDownSchedule.currentText() == "Hourly" or \
                self.dropDownSchedule.currentText() == "Weekly" or self.dropDownSchedule.currentText() == "Monthly":
            if self.dropDownPeriod.currentIndex() != 0 and self.dropDownPeriod.currentIndex() != -1:
                UIC.periodCriteriaC = True
            else:
                UIC.periodCriteriaC = False
        elif self.dropDownSchedule.currentText() == "Daily":
            UIC.periodCriteriaC = True
        else:
            UIC.periodCriteriaC = False
        # Time Criteria
        if UIC.taskTime != "":
            UIC.timeCriteriaC = True
        else:
            UIC.timeCriteriaC = False
        # Name Criteria
        if UIC.taskName != "" and " " not in UIC.taskName:
            UIC.nameCriteriaC = True
        else:
            UIC.nameCriteriaC = False
        # Enable button
        if UIC.periodCriteriaC is True and UIC.timeCriteriaC is True and UIC.nameCriteriaC is True:
            print(UIC.cmdLineC)
            self.cudButton.setEnabled(True)
        else:
            self.cudButton.setEnabled(False)

    def updateTaskCriteria(self):
        if self.tabWidget.currentIndex() == 1:
            if self.dropDownTaskName.currentIndex() != 0 and self.dropDownTaskName.currentIndex() != -1:
                if self.labelOldTime.text() != self.labelNewTime.text():
                    UIC.timerCriteriaU = True
                else:
                    UIC.timerCriteriaU = False
            else:
                UIC.timerCriteriaU = False
            if UIC.timerCriteriaU is True:
                self.cudButton.setEnabled(True)
            else:
                self.cudButton.setEnabled(False)


    def triggerCUDBtn(self):
        if self.tabWidget.currentIndex() == 0:
            UIC.createTask()
            UIC.writeCSV(UIC.taskName, UIC.taskPeriod, UIC.taskTime)
        elif self.tabWidget.currentIndex() == 1:
            UIC.updateTask()


    def readTask(self):
        with open(UIC.csvFileName) as csvFile:
            lines = csvFile.readlines()

            UIC.taskNameList, UIC.taskPeriodList, UIC.taskTimeList = ["-"], ["-"], ["00:00"]
            self.dropDownTaskName.clear()

            for line in lines:
                if line != "taskName,taskPeriod,taskTime\n" and line != "\n":
                    UIC.taskNameList.append(line.split(",")[0])
                    UIC.taskPeriodList.append(line.split(",")[1])
                    UIC.taskTimeList.append(line.split(",")[2].strip("\n"))

                    self.dropDownTaskName.addItems(UIC.taskNameList)


    def populateUpdateData(self):
        if self.dropDownTaskName.currentIndex() != 0 and self.dropDownTaskName.currentIndex() != -1:
            currentTaskNameIndex = self.dropDownTaskName.currentIndex()
            UIC.taskName = self.dropDownTaskName.currentText()
            self.labelTaskName.setText(UIC.taskNameList[currentTaskNameIndex])
            self.labelPeriod.setText(UIC.taskPeriodList[currentTaskNameIndex])
            self.labelOldTime.setText(UIC.taskTimeList[currentTaskNameIndex])
        self.realTimeUpdates()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    window = Main()
    window.show()

    sys.exit(app.exec())
