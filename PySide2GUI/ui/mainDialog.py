from ui.WubaGUI import Ui_MainWindow
from PySide2 import QtCore, QtGui, QtWidgets

from API.api import API

# import PyPlot widget for our 3D plot
from plot.plot import PlotWidget


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    HORIZONTAL_MOVE = 30
    VERTICAL_MOVE = 30
    ROTATION_MOVE = 30

    def __init__(self):
        # This is equivalent to super(self.__class__, self).__init__()
        super().__init__()

        # Intialize plot widget
        self.plot = PlotWidget()

        # Initialize API
        self.api = API()

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
        cmd = 'cw'
        rotation = (cmd, -self.ROTATION_MOVE)
        self.plot.command_rotate(*rotation)
        self.append_command(self.api.command_rotation(*rotation))

    def on_turn_right(self):
        cmd = 'cw'
        rotation = (cmd, self.ROTATION_MOVE)
        self.plot.command_rotate(*rotation)
        self.append_command(self.api.command_rotation(*rotation))

    def on_forward(self):
        coord = (self.HORIZONTAL_MOVE, 0, 0)
        self.plot.command_go(*coord)
        self.append_command(self.api.command_go(*coord, self.leSpeed.text()))

    def on_back(self):
        coord = (-self.HORIZONTAL_MOVE, 0, 0)
        self.plot.command_go(*coord)
        self.append_command(self.api.command_go(*coord, self.leSpeed.text()))

    def on_strafe_left(self):
        coord = (0, -self.HORIZONTAL_MOVE, 0)
        self.plot.command_go(*coord)
        self.append_command(self.api.command_go(*coord, self.leSpeed.text()))

    def on_strafe_right(self):
        coord = (0, self.HORIZONTAL_MOVE, 0)
        self.plot.command_go(*coord)
        self.teCommands.appendPlainText(self.api.command_go(*coord, self.leSpeed.text()))

    def on_down(self):
        coord = (0, 0, -self.VERTICAL_MOVE)
        self.plot.command_go(*coord)
        self.append_command(self.api.command_go(*coord, self.leSpeed.text()))

    def on_up(self):
        coord = (0, 0, self.VERTICAL_MOVE)
        self.plot.command_go(*coord)
        self.append_command(self.api.command_go(*coord, self.leSpeed.text()))

    def on_add_command(self):
        command = self.command_text.split(" ")[0]
        if command in self.commands:
            self.append_command(self.command_text)
            return
        raise ValueError('Non-existing command!')

    def on_takeoff_land(self):
        self._flying = not self._flying

        if self._flying:
            self.bTakeOffLand_2.setText("Land")
            self.append_command("takeoff")
        else:
            self.bTakeOffLand_2.setText("Take Off")
            self.append_command("land")

    def on_pitch_up(self):
        print("on_pitch_up")

    def on_pitch_down(self):
        print("on_pitch_down")

    def on_pitch_reset(self):
        print("on_pitch_reset")

    def on_reset_simulation(self):
        self.plot.reset()

    def on_push_to_drone(self):
        commands = ["command", "takeoff"] + self.teCommands.toPlainText().split("\n") + ["land"]
        self.api.run_commands(commands)
