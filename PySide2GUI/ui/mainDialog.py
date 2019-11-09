from ui.WubaGUI import Ui_MainWindow
from PySide2 import QtCore, QtGui, QtWidgets

from API.tello_test import movements as go
from API.tello_test import angles as degrees

# import PyPlot widget for our 3D plot
from ..plot.plot import PlotWidget


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    HORIZONTAL_MOVE = 30
    VERTICAL_MOVE = 30
    ROTATION_MOVE = 30

    def __init__(self):
        # This is equivalent to super(self.__class__, self).__init__()
        super().__init__()

        # Commands
        self.commands = { "go", "back", "forward", "cw", "ccw", "takeoff", "land" }
        self._flying = False

        self.setupUi(self)

        # Any changes to layout, etc. has to be done after UI setup
        self.gRoot.addWidget(self.plot, 1, 1, 1, 1)
    
    # ------------------------
    # PROPERTIES
    # ------------------------

    @property
    def command_text(self):
        return self.lineEdit.text()

    # ------------------------
    # METHODS
    # ------------------------
    
    def append_command(self, command):
        self.teCommands.appendPlainText(command)

    # ------------------------
    # EVENT HANDLERS
    # ------------------------

    def on_turn_left(self):
        # coord = (0, 0, self.VERTICAL_MOVE)
        # self.plot.command_go(*coord)
        self.append_command(degrees("ccw", self.ROTATION_MOVE))

    def on_turn_right(self):
        # coord = (0, 0, self.VERTICAL_MOVE)
        # self.plot.command_go(*coord)
        self.append_command(degrees("cw", self.ROTATION_MOVE))

    def on_forward(self):
        coord = (self.HORIZONTAL_MOVE, 0, 0)
        self.plot.command_go(*coord)
        self.append_command(go(*coord, self.leSpeed.text()))

    def on_back(self):
        coord = (-self.HORIZONTAL_MOVE, 0, 0)
        self.plot.command_go(*coord)
        self.append_command(go(*coord, self.leSpeed.text()))

    def on_strafe_left(self):
        coord = (0, -self.HORIZONTAL_MOVE, 0)
        self.plot.command_go(*coord)
        self.append_command(go(*coord, self.leSpeed.text()))

    def on_strafe_right(self):
        coord = (0, self.HORIZONTAL_MOVE, 0)
        self.plot.command_go(*coord)
        self.teCommands.appendPlainText(go(*coord, self.leSpeed.text()))

    def on_down(self):
        coord = (0, 0, -self.VERTICAL_MOVE)
        self.plot.command_go(*coord)
        self.append_command(go(*coord, self.leSpeed.text()))

    def on_up(self):
        coord = (0, 0, self.VERTICAL_MOVE)
        self.plot.command_go(*coord)
        self.append_command(go(*coord, self.leSpeed.text()))

    def on_add_command(self):
        command = self.command_text.split(" ")[0]
        if command in self.commands:
            self.append_command(self.command_text)
            return
        raise ValueError('Non-existing command!')

    def on_takeoff_land(self):
        self._flying = not self._flying

        if self._flying:
            self.bTakeOffLand_2.text("Land")
            self.append_command("takeoff")
        else:
            self.bTakeOffLand_2.text("Take Off")
            self.append_command("land")

    def on_pitch_up(self):
        print("on_pitch_up")

    def on_pitch_down(self):
        print("on_pitch_down")

    def on_pitch_reset(self):
        print("on_pitch_reset")

    def on_simulation(self):
        print("Simulatiooooon")

    def on_push_to_drone(self):
        print("pushing to drone... nothing")
