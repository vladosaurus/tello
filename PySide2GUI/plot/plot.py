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
        self.current_coordinates = numpy.array([[0, 0, 0]]).T
        #self.plot = Plot()

    def get_current_coord(self) -> numpy.array:
        return self.current_coordinates

    def receive_movement(self, direction: str, distance: int):
        '''[summary]

        :param direction: Per API this can be up, down,
        :type direction: string
        :param distance: [description]
        :type distance: int

        # 		'left': f'left {dst}',
        # 		'right': f'right {dst}',
        # 		'forward': f'forward {dst}',
        # 		'back': f'back {dst}',
        # 		'takeoff': f'takeoff',
        # 		'land': f'land'
        '''
        if direction.lower() == 'up':
            self.current_coordinates[2] += distance


class PlotWindow(FigureCanvas):  # Class for 3D window
    def __init__(self):
        self.fig = plt.figure(figsize=(7, 7))
        FigureCanvas.__init__(self, self.fig)  # creating FigureCanvas
        self.axes = self.fig.gca(projection='3d')  # generates 3D Axes object

        self.axes.set_xlabel('X axis')
        self.axes.set_ylabel('Y axis')
        self.axes.set_zlabel('Z axis')

        # self.axes.hold(False)#clear axes on each run
        # self.setWindowTitle("Main") # sets Window title

    def draw_plot(self, x, y, z):  # Fun for Graph plotting
        self.axes.clear()
        self.axes.plot(x, y, z, marker='x')
        # self.axes.plot_surface(x, y, z) #plots the 3D surface plot
        self.draw()


class PlotWidget(QtWidgets.QWidget):  # The QWidget in which the 3D window is been embedded
    def __init__(self, drone: Drone, parent=None):
        super(PlotWidget, self).__init__(parent)

        # Initialize instance of our drone for calculations, etc.
        self.drone = Drone()

        # TODO: Test button, to be extended
        self.button = QtWidgets.QPushButton('Fly up!')
        self.button.clicked.connect(self.fly_up)

        self.plot = PlotWindow()  # creating 3D Window
        MainLayout = QtWidgets.QGridLayout()  # Layout for Main Tab Widget

        MainLayout.setRowMinimumHeight(0, 5)  # setting layout parameters
        MainLayout.setRowMinimumHeight(2, 10)
        MainLayout.setRowMinimumHeight(4, 5)

        MainLayout.addWidget(self.button, 1, 1)  # add button to Main layout
        MainLayout.addWidget(self.plot, 2, 1)  # add 3D Window to Main layout

        self.setLayout(MainLayout)  # sets Main layout

    def f(self, x, y):  # For Generating Z coordinates
        return numpy.sin(numpy.sqrt(x**2+y**2))

    def fly_up(self):
        self.drone.receive_movement('up', 10)
        coords = self.drone.get_current_coord()
        self.plot.draw_plot(*coords)  # call Fun for Graph plot

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
    Window = PlotWidget(drone)
    Window.setWindowTitle("Main")
    qr = Window.frameGeometry()
    Window.move(qr.topLeft())
    Window.showMaximized()
    app.processEvents()
    sys.exit(app.exec_())
