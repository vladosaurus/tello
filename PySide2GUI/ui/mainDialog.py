from ui.WubaGUI import Ui_MainWindow
from PySide2 import QtCore, QtGui, QtWidgets

from API.api import API

# import PyPlot widget for our 3D plot
from plot.plot import PlotWidget


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        # This is equivalent to super(self.__class__, self).__init__()
        super().__init__()

        # Intialize plot widget
        self.plot = PlotWidget()

        # Initialize API
        self.api = API()

        # Commands
        # self.available_commands = { "go", "cw", "ccw" }
        self._flying = False

        self.setupUi(self)

        # Any changes to layout, etc. has to be done after UI setup
        self.gRoot.addWidget(self.plot, 1, 1, 1, 1)
    
    # ------------------------
    # PROPERTIES
    # ------------------------

    @property
    def distance(self):
        return int(self.leDistance.text())

    @property
    def degrees(self):
        return int(self.leDegrees.text())

    @property
    def speed(self):
        return int(self.leSpeed.text())

    @property
    def command_text(self):
        return self.leCommand.text()

    # ------------------------
    # METHODS
    # ------------------------
    
    def append_command(self, command):
        self.teCommands.appendPlainText(command)

    def get_commands(self):
        return self.teCommands.toPlainText().split("\n")

    # ------------------------
    # EVENT HANDLERS
    # ------------------------

    def on_turn_left(self):
        cmd = 'cw'
        rotation = (cmd, -self.degrees)
        self.plot.command_rotate(*rotation)
        self.append_command(self.api.command_rotation(*rotation))

    def on_turn_right(self):
        rotation = ("cw", self.degrees)
        self.plot.command_rotate(*rotation)
        self.append_command(self.api.command_rotation(*rotation))

    def on_forward(self):
        coord = (self.distance, 0, 0)
        self.plot.command_go(*coord)
        self.append_command(self.api.command_go(*coord, self.speed))

    def on_back(self):
        coord = (-self.distance, 0, 0)
        self.plot.command_go(*coord)
        self.append_command(self.api.command_go(*coord, self.speed))

    def on_strafe_left(self):
        coord = (0, -self.distance, 0)
        self.plot.command_go(*coord)
        self.append_command(self.api.command_go(*coord, self.speed))

    def on_strafe_right(self):
        coord = (0, self.distance, 0)
        self.plot.command_go(*coord)
        self.append_command(self.api.command_go(*coord, self.speed))

    def on_down(self):
        coord = (0, 0, -self.distance)
        self.plot.command_go(*coord)
        self.append_command(self.api.command_go(*coord, self.speed))

    def on_up(self):
        coord = (0, 0, self.distance)
        self.plot.command_go(*coord)
        self.append_command(self.api.command_go(*coord, self.speed))

    def on_add_command(self):
        self.append_command(self.command_text)

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
    
    def on_run_simulation(self):
        self.plot.reset()

        commands = self.get_commands()
        for command in commands:
            command_values = command.split(" ")

            if command_values[0] == "go":
                self.plot.command_go(*[int(c) for c in command_values[1:4]])
            elif command_values[0] == "cw":
                self.plot.command_rotate(command_values[0], int(command_values[1]))


    def on_push_to_drone(self):
        commands = ["command", "takeoff"] + self.get_commands() + ["land"]
        self.api.run_commands(commands)
