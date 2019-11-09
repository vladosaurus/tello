import sys

from mpl_toolkits import mplot3d

import numpy
from matplotlib import colors
import matplotlib.pyplot as plt

# Canvas for PyQt
from PySide2 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class Drone:
    def __init__(self):
        '''Set up Drone object with start coordinates
        '''
        self.current_coordinates = numpy.array([0, 0, 0])
        self.trajectory = numpy.array([[0, 0, 0]])
        # rotation in degrees
        self.current_rotation = 0

    def get_current_coord(self) -> numpy.array:
        return self.current_coordinates

    def get_trajectory(self) -> numpy.array:
        return numpy.array(self.trajectory.T)

    def get_current_rotation(self) -> int:
        return self.current_rotation

    def receive_go(self, x: int, y: int, z: int):
        self.current_coordinates[0] += x
        self.current_coordinates[1] += y
        self.current_coordinates[2] += z

        self.trajectory = numpy.vstack(
            (self.trajectory, self.current_coordinates))

    @staticmethod
    def _normalize_rotation(deg: int):
        angle = deg % 360

        angle = (angle + 360) % 360

        if (angle > 180):
            angle -= 360

        return angle

    def receive_roration(self, deg: int):
        self.current_rotation = self._normalize_rotation(deg)


class PlotWindow(FigureCanvas):  # Class for 3D window
    def __init__(self):
        self.fig = plt.figure(figsize=(7, 7))
        FigureCanvas.__init__(self, self.fig)  # creating FigureCanvas
        self.axes = self.fig.gca(projection='3d')  # generates 3D Axes object

        self.axes.set_xlabel('X axis')
        self.axes.set_ylabel('Y axis')
        self.axes.set_zlabel('Z axis')

    def draw_plot(self, x: int, y: int, z: int):  # Fun for Graph plotting
        self.axes.clear()
        self.axes.plot(x, y, z, marker='x')
        # self.axes.plot_surface(x, y, z) #plots the 3D surface plot
        self.draw()


class PlotWidget(QtWidgets.QWidget):  # The QWidget in which the 3D window is been embedded
    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent)

        # Initialize instance of our drone for calculations, etc.
        self.drone = Drone()

        self.plot = PlotWindow()  # creating 3D Window
        MainLayout = QtWidgets.QGridLayout()  # Layout for Main Tab Widget

        MainLayout.addWidget(self.plot, 1, 1)  # add 3D Window to Main layout

        self.setLayout(MainLayout)  # sets Main layout

    def command_go(self, x=10, y=10, z=10):
        self.drone.receive_go(x, y, z)
        coords = self.drone.get_trajectory()
        self.plot.draw_plot(*coords)  # call Fun for Graph plot

    def command_rotate(self, rotation: int):
        print('Rotating...')

    def reset(self):
        self.drone = Drone()
        coords = self.drone.get_trajectory()
        self.plot.draw_plot(*coords)

    #     # TODO: Draw arrows, direction

    #     self.axes.scatter(*current_coordinates.T[-1], color='red')


# 'up': f'up {dst}',
# 		'down': f'down {dst}',
# 		'left': f'left {dst}',
# 		'right': f'right {dst}',
# 		'forward': f'forward {dst}',
# 		'back': f'back {dst}',
# 		'takeoff': f'takeoff',
# 		'land': f'land'

# object dron coords?

# TODO: Create object representing drone, store his values (pitch, rotation, altitude, speed?, )

if __name__ == '__main__':  # The Fun for Main()
    drone = Drone()
    app = QtWidgets.QApplication(sys.argv)
    Window = PlotWidget()
    Window.setWindowTitle("Main")
    qr = Window.frameGeometry()
    Window.move(qr.topLeft())
    Window.showMaximized()
    app.processEvents()
    sys.exit(app.exec_())
