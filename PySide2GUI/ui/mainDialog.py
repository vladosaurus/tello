from ui.WubaGUI import Ui_MainWindow
from PySide2 import QtCore, QtGui, QtWidgets

# import PyPlot widget for our 3D plot
from plot.plot import PlotWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        # This is equivalent to super(self.__class__, self).__init__()
        super().__init__()

        self.plot = PlotWindow()

        self.setupUi(self)

        # Any changes to layout, etc. has to be done after UI setup
        self.gRoot.addWidget(self.plot, 1, 1, 1, 1)

    def on_turn_left(self):
        print("on_turn_left")

    def on_turn_right(self):
        print("on_turn_right")

    def on_forward(self):
        print("on_forward")

    def on_back(self):
        print("on_back")

    def on_strafe_left(self):
        print("on_strafe_left")

    def on_strafe_right(self):
        print("on_strafe_right")

    def on_down(self):
        print("on_down")

    def on_up(self):
        self.teCommands.appendPlainText("up")

    def on_add_command(self):
        command = self.lineEdit.text()
        commands = ["flip"]
        if command in commands:
            self.teCommands.appendPlainText(command)
            return True
        raise ValueError('Non-existing command!')


    def on_takeoff_land(self):
        print("on_takeoff_land")

    def on_pitch_up(self):
        print("on_pitch_up")

    def on_pitch_down(self):
        print("on_pitch_down")

    def on_pitch_reset(self):
        print("on_pitch_reset")


