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
        UIC.taskType = "CREATE"
        self.realTimeUpdates()
        self.initialiseObject()

    # Initialise objects
    def initialiseObject(self):
        self.initialiseTabs()
        self.initialiseButtons()
        self.initialiseField()

    # Initialise tabs
    def initialiseTabs(self):
        self.tabWidget.currentChanged.connect(self.tabChanged)

    def initialiseButtons(self):
        # Push Buttons
        self.createButton.setEnabled(False)
        self.createButton.clicked.connect(lambda: self.createTask())
        # Radio buttons
        self.radioDaily.clicked.connect(lambda: self.periodButtonChanged())
        self.radioWeekly.clicked.connect(lambda: self.periodButtonChanged())
        self.radioMonthly.clicked.connect(lambda: self.periodButtonChanged())
        # Combo box
        self.dropDownPeriod.currentTextChanged.connect(lambda: self.periodValue())
        # QTimeEdit
        self.timePeriod.setTime(QTime(0, 0))
        self.timePeriod.timeChanged.connect(lambda: self.periodTimeChanged())

    def initialiseField(self):
        # QLineEdit
        self.lineTaskName.textChanged.connect(lambda: self.taskNameChanged())

    def resetDefault(self):
        # reset radio buttons
        self.radioDaily.setAutoExclusive(False)
        self.radioDaily.setChecked(False)
        self.radioDaily.setAutoExclusive(True)
        self.radioWeekly.setAutoExclusive(False)
        self.radioWeekly.setChecked(False)
        self.radioWeekly.setAutoExclusive(True)
        self.radioMonthly.setAutoExclusive(False)
        self.radioMonthly.setChecked(False)
        self.radioMonthly.setAutoExclusive(True)
        UIC.taskPeriod = ""
        # reset dropdown menu
        self.dropDownPeriod.clear()
        self.dropDownPeriod.addItem("-")
        # reset task name
        self.lineTaskName.setText("")
        UIC.taskName = ""
        # reset task time
        self.timePeriod.setTime(QTime(0, 0))
        UIC.taskTime = str("{:02}".format(self.timePeriod.time().hour())) + ":" + str(
            "{:02}".format(self.timePeriod.time().minute()))
        # reset labelcmdline
        self.realTimeUpdates()
        # Reset criteria
        UIC.radioCriteria, UIC.timeCriteria, UIC.nameCriteria = False, False, False
        # reset createButton
        self.createButton.setEnabled(False)

    # Get task type
    def tabChanged(self):
        if self.tabWidget.currentIndex() == 0:
            UIC.taskType = "CREATE"
            UIC.logger.info("CREATE Tab is selected.")
        elif self.tabWidget.currentIndex() == 1:
            UIC.taskType = "CHANGE"
            UIC.logger.info("UPDATE Tab is selected.")
        elif self.tabWidget.currentIndex() == 2:
            UIC.taskType = "DELETE"
            UIC.logger.info("DELETE Tab is selected.")
        self.resetDefault()
        self.realTimeUpdates()

    # Get task period
    def periodButtonChanged(self):
        if self.radioDaily.isChecked():
            UIC.taskPeriod = "DAILY"
            self.dailyComboBox()
            UIC.logger.info("Daily Period is selected.")
        elif self.radioWeekly.isChecked():
            UIC.taskPeriod = "WEEKLY"
            self.weeklyComboBox()
            UIC.logger.info("Weekly Period is selected.")
        elif self.radioMonthly.isChecked():
            UIC.taskPeriod = "MONTHLY"
            self.monthlyComboBox()
            UIC.logger.info("Monthly Period is selected.")
        self.realTimeUpdates()

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
        if self.radioDaily.isChecked():
            # print(UIC.taskPeriod)
            pass
        elif self.radioWeekly.isChecked():
            if self.dropDownPeriod.currentIndex() != 0 and self.dropDownPeriod.currentIndex() != -1:
                UIC.taskPeriod = "WEEKLY"
                UIC.taskPeriod = UIC.taskPeriod + " /D " + self.dropDownPeriod.currentText()[:3]
                # print(UIC.taskPeriod)
                UIC.logger.info("Day is selected.")
            else:
                UIC.taskPeriod = "WEEKLY"
        elif self.radioMonthly.isChecked():
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
        self.labelCmdLine.setText(UIC.updateCmdLine())

    def createTaskCriteria(self):

        # Period Criteria
        if self.radioWeekly.isChecked() or self.radioMonthly.isChecked():
            if self.dropDownPeriod.currentIndex() != 0 and self.dropDownPeriod.currentIndex() != -1:
                UIC.radioCriteria = True
            else:
                UIC.radioCriteria = False
        elif self.radioDaily.isChecked():
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
            print(UIC.cmdLine)
            self.createButton.setEnabled(True)
        else:
            self.createButton.setEnabled(False)

    def createTask(self):
            UIC.createTask()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    window = Main()
    window.show()

    sys.exit(app.exec())
