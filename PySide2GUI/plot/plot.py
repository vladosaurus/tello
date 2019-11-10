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
        # calculate global x and y movement per curent rotation
        r_x, r_y = self._calculate_rotation_xy(x, y)
        self.current_coordinates[0] += r_x
        self.current_coordinates[1] += r_y
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

    def _calculate_rotation_xy(self, x, y):
        radians = numpy.radians(self.current_rotation)
        c, s = numpy.cos(radians), numpy.sin(radians)
        j = numpy.matrix([[c, s], [-s, c]])
        m = numpy.dot(j, [x, y])

        return float(m.T[0]), float(m.T[1])

    def receive_rotation(self, deg: int):
        self.current_rotation = self._normalize_rotation(self.current_rotation + deg)


class PlotWindow(FigureCanvas):  # Class for 3D window
    def __init__(self):
        self.fig = plt.figure()
        FigureCanvas.__init__(self, self.fig)
        self.axes = self.fig.gca(projection='3d', proj_type = 'ortho')

        # NOTE: This is not implemented yet in API for 3d plots
        # plt.gca().set_aspect('equal', adjustable='box')

        self.axes.set_xlabel('X axis')
        self.axes.set_ylabel('Y axis')
        self.axes.set_zlabel('Z axis')

    def draw_plot(self, x: int, y: int, z: int):
        self.axes.clear()
        self.axes.plot(x, y, z, marker='x')
        # self.set_equal_axis(x, y, z)
        self.draw()

    # def set_equal_axis(self, X, Y, Z):
    #     max_range = numpy.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max() / 2.0

    #     mid_x = (X.max()+X.min()) * 0.5
    #     mid_y = (Y.max()+Y.min()) * 0.5
    #     mid_z = (Z.max()+Z.min()) * 0.5
    #     self.axes.set_xlim(mid_x - max_range, mid_x + max_range)
    #     self.axes.set_ylim(mid_y - max_range, mid_y + max_range)
    #     self.axes.set_zlim(mid_z - max_range, mid_z + max_range)


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
        self.plot.draw_plot(*coords)

    def command_rotate(self, command: str, rotation: int):
        print('Rotating...')
        print(self.drone.get_current_rotation())
        self.drone.receive_rotation(rotation)


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
