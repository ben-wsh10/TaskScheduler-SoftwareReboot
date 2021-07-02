import re
import sys

from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from UserInterface import Ui_MainWindow
import UIController as UIC


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        # Set up User Interface
        QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)

        UIC.startLogging()
        UIC.newCSV()
        UIC.taskType = "CREATE"
        self.realTimeUpdates()
        self.initialiseObject()

    # Initialise objects
    def initialiseObject(self):
        # Initialise tabs
        self.tabWidget.currentChanged.connect(self.tabChanged)
        self.tabWidget.setTabVisible(1, False)
        # Initialise create/update/delete Buttons
        self.cudButton.setText("Create")
        self.cudButton.setEnabled(False)
        self.cudButton.clicked.connect(lambda: self.triggerCUDBtn())
        # Initialise start time
        self.timePeriod.setTime(QTime(0, 0))
        self.timePeriod2.setTime(QTime(0, 0))
        self.timePeriod.timeChanged.connect(lambda: self.periodTimeChanged())
        self.timePeriod2.timeChanged.connect(lambda: self.periodTimeChanged())
        # Initialise task name
        self.lineTaskName.textChanged.connect(lambda: self.taskNameChanged())
        self.labelTaskName.setText("-")
        self.labelPeriod.setText("-")
        # Initialise dropDownMenu
        self.dropDownSchedule.addItems(UIC.periodList)
        self.dropDownSchedule.currentTextChanged.connect(lambda: self.periodMenuChanged())
        self.dropDownPeriod.currentTextChanged.connect(lambda: self.periodValue())
        self.dropDownTaskName.currentTextChanged.connect(lambda: self.populateUpdateData())
        self.dropDownTaskName2.currentTextChanged.connect(lambda: self.populateUpdateData())

    # Reset settings to default when changing tabs
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
            self.readTask()
            UIC.logger.info("DELETE Tab is selected.")
        self.resetDefault()
        self.realTimeUpdates()

    # Get task period
    def periodMenuChanged(self):
        if self.dropDownSchedule.currentText() == "Minute":
            UIC.taskPeriod = "MINUTE"
            self.minuteComboBox()
        elif self.dropDownSchedule.currentText() == "Hourly":
            UIC.taskPeriod = "HOURLY"
            self.hourlyComboBox()
        elif self.dropDownSchedule.currentText() == "Daily":
            UIC.taskPeriod = "DAILY"
            self.dailyComboBox()
        elif self.dropDownSchedule.currentText() == "Weekly":
            UIC.taskPeriod = "WEEKLY"
            self.weeklyComboBox()
        elif self.dropDownSchedule.currentText() == "Monthly":
            UIC.taskPeriod = "MONTHLY"
            self.monthlyComboBox()
        self.realTimeUpdates()

    # DropDownMenu for minute period
    def minuteComboBox(self):
        self.dropDownPeriod.clear()
        self.dropDownPeriod.addItems(UIC.minuteList)

    # DropDownMenu for hourly period
    def hourlyComboBox(self):
        self.dropDownPeriod.clear()
        self.dropDownPeriod.addItems(UIC.hourlyList)

    # DropDownMenu for daily period
    def dailyComboBox(self):
        self.dropDownPeriod.clear()
        self.dropDownPeriod.addItems(UIC.dailyList)

    # DropDownMenu for weekly period
    def weeklyComboBox(self):
        self.dropDownPeriod.clear()
        self.dropDownPeriod.addItems(UIC.weekList)

    # DropDownMenu for monthly period
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
            else:
                UIC.taskPeriod = "HOURLY"
        elif self.dropDownSchedule.currentText() == "Daily":
            pass
        elif self.dropDownSchedule.currentText() == "Weekly":
            if self.dropDownPeriod.currentIndex() != 0 and self.dropDownPeriod.currentIndex() != -1:
                UIC.taskPeriod = "WEEKLY"
                UIC.taskPeriod = UIC.taskPeriod + " /D " + self.dropDownPeriod.currentText()[:3]
            else:
                UIC.taskPeriod = "WEEKLY"
        elif self.dropDownSchedule.currentText() == "Monthly":
            if self.dropDownPeriod.currentIndex() != 0 and self.dropDownPeriod.currentIndex() != -1:
                UIC.taskPeriod = "MONTHLY"
                UIC.taskPeriod = UIC.taskPeriod + " /D " + str(
                    re.search(r'\d+', self.dropDownPeriod.currentText()).group())
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

    # Get task name
    def taskNameChanged(self):
        UIC.taskName = self.lineTaskName.text()
        self.realTimeUpdates()

    # Provide real time updates
    def realTimeUpdates(self):
        self.updateLabelCmdLine()
        self.createTaskCriteria()
        self.updateTaskCriteria()
        self.deleteTaskCriteria()

    # Update cmdLine label
    def updateLabelCmdLine(self):
        if self.tabWidget.currentIndex() == 0:
            self.labelCmdLine.setText(UIC.createCmdLine())
        elif self.tabWidget.currentIndex() == 1:
            self.labelCmdLine.setText(UIC.updateCmdLine())
            self.labelNewTime.setText(UIC.taskTime)
        elif self.tabWidget.currentIndex() == 2:
            self.labelCmdLine.setText(UIC.deleteCmdLine())

    # Criteria to enable create button
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

    # Criteria to enable update button
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

    # Criteria to enable delete button
    def deleteTaskCriteria(self):
        if self.tabWidget.currentIndex() == 2:
            if self.dropDownTaskName2.currentIndex() != 0 and self.dropDownTaskName2.currentIndex() != -1:
                UIC.nameCriteriaD = True
            else:
                UIC.nameCriteriaD = False
            if UIC.nameCriteriaD is True:
                self.cudButton.setEnabled(True)
            else:
                self.cudButton.setEnabled(False)

    # actions upon triggering cudButton
    def triggerCUDBtn(self):
        if self.tabWidget.currentIndex() == 0:
            UIC.createTask()
            UIC.createCSV(UIC.taskName, UIC.taskPeriod, UIC.taskTime)
            QMessageBox.about(self, "Success", "Task created successfully!")
            UIC.logger.info(
                "Task Created : " + str(UIC.taskName) + ", " + str(UIC.taskPeriod) + ", " + str(UIC.taskTime))
        elif self.tabWidget.currentIndex() == 1:
            UIC.updateTask()
            UIC.updateCSV(UIC.taskName, UIC.taskTime)
            self.labelOldTime.setText(UIC.taskTime)
            self.realTimeUpdates()
            QMessageBox.about(self, "Updates", "Task updated successfully!")
            UIC.logger.info(
                "Task Updated : " + str(UIC.taskName) + ", " + str(UIC.taskPeriod) + ", " + str(UIC.taskTime))
        elif self.tabWidget.currentIndex() == 2:
            UIC.deleteTask()
            UIC.deleteCSV(UIC.taskName)
            self.dropDownTaskName2.setCurrentIndex(0)
            self.labelPeriod2.setText("-")
            self.labelTime.setText("00:00")
            self.realTimeUpdates()
            QMessageBox.about(self, "Completed", "Task deleted successfully!")
            UIC.logger.info(
                "Task Deleted : " + str(UIC.taskName) + ", " + str(UIC.taskPeriod) + ", " + str(UIC.taskTime))

    # reading csv file and populating task name dropdownmenu
    def readTask(self):
        with open(UIC.csvFileName) as csvFile:
            lines = csvFile.readlines()

            UIC.taskNameList, UIC.taskPeriodList, UIC.taskTimeList = ["-"], ["-"], ["00:00"]

            for line in lines:
                if line != "taskName,taskPeriod,taskTime\n" and line != "\n":
                    UIC.taskNameList.append(line.split(",")[0])
                    UIC.taskPeriodList.append(line.split(",")[1])
                    UIC.taskTimeList.append(line.split(",")[2].strip("\n"))

            if self.tabWidget.currentIndex() == 1:
                self.dropDownTaskName.clear()
                self.dropDownTaskName.addItems(UIC.taskNameList)
            elif self.tabWidget.currentIndex() == 2:
                self.dropDownTaskName2.clear()
                self.dropDownTaskName2.addItems(UIC.taskNameList)

    # populating other contents based on selected taskname
    def populateUpdateData(self):
        if self.tabWidget.currentIndex() == 1:
            if self.dropDownTaskName.currentIndex() != 0 and self.dropDownTaskName.currentIndex() != -1:
                currentTaskNameIndex = self.dropDownTaskName.currentIndex()
                UIC.taskName = self.dropDownTaskName.currentText()
                self.labelTaskName.setText(UIC.taskNameList[currentTaskNameIndex])
                self.labelPeriod.setText(UIC.taskPeriodList[currentTaskNameIndex])
                self.labelOldTime.setText(UIC.taskTimeList[currentTaskNameIndex])
        elif self.tabWidget.currentIndex() == 2:
            if self.dropDownTaskName2.currentIndex() != 0 and self.dropDownTaskName2.currentIndex() != -1:
                currentTaskNameIndex = self.dropDownTaskName2.currentIndex()
                UIC.taskName = self.dropDownTaskName2.currentText()
                self.labelPeriod2.setText(UIC.taskPeriodList[currentTaskNameIndex])
                self.labelTime.setText(UIC.taskTimeList[currentTaskNameIndex])
        self.realTimeUpdates()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    window = Main()
    window.show()

    sys.exit(app.exec())
