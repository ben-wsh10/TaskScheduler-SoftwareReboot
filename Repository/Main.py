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
        self.cudButton.clicked.connect(lambda: self.createTask())
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
        UIC.radioCriteria, UIC.timeCriteria, UIC.nameCriteria = False, False, False
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
        UIC.taskTime = str("{:02}".format(self.timePeriod.time().hour())) + ":" + str(
            "{:02}".format(self.timePeriod.time().minute()))
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

    # Update cmdLine label
    def updateLabelCmdLine(self):
        # print(UIC.updateCmdLine())
        self.labelCmdLine.setText(UIC.createCmdLine())
        self.labelNewTime.setText(UIC.taskTime)

    def createTaskCriteria(self):
        # Period Criteria
        if self.dropDownSchedule.currentText() == "Minute" or self.dropDownSchedule.currentText() == "Hourly" or \
                self.dropDownSchedule.currentText() == "Weekly" or self.dropDownSchedule.currentText() == "Monthly":
            if self.dropDownPeriod.currentIndex() != 0 and self.dropDownPeriod.currentIndex() != -1:
                UIC.radioCriteria = True
            else:
                UIC.radioCriteria = False
        elif self.dropDownSchedule.currentText() == "Daily":
            UIC.radioCriteria = True
        else:
            UIC.radioCriteria = False
        # Time Criteria
        if UIC.taskTime != "":
            UIC.timeCriteria = True
        else:
            UIC.timeCriteria = False
        # Name Criteria
        if UIC.taskName != "" and " " not in UIC.taskName:
            UIC.nameCriteria = True
        else:
            UIC.nameCriteria = False
        # Enable button
        if UIC.radioCriteria is True and UIC.timeCriteria is True and UIC.nameCriteria is True:
            print(UIC.cmdLineC)
            self.cudButton.setEnabled(True)
        else:
            self.cudButton.setEnabled(False)

    def createTask(self):
        UIC.createTask()
        UIC.writeCSV(UIC.taskName, UIC.taskPeriod, UIC.taskTime)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    window = Main()
    window.show()

    sys.exit(app.exec())
