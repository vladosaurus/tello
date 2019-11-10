from unittest import TestCase, mock
import numpy
import matplotlib.pyplot as plt

# from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

def create_circle(center_x=0 , center_y=0, radius=500):
    ''' testing code for equality to calculate validity and weight of gen alg
    
    :param center_x: center x-axis coord, defaults to 0
    :type center_x: int, optional
    :param center_y: center y-axis coord, defaults to 0
    :type center_y: int, optional
    :param radius: circle radius, defaults to 1
    :type radius: int, optional
    '''
    # testing code for equality to calculate validity and weight of gen alg
    # NOTE: test confirmed that weight calculated by this procedure can be used to evaluate fitness of gen alg
    best_points = numpy.array([[radius, 0]])
    bad_points = numpy.array([[radius, 0]])
    worst_points = numpy.array([[radius, 0]])

    for degree in range(1, 360, 1):
        radians = numpy.radians(degree)
        x = center_x + radius * numpy.cos(radians)
        y = center_y + radius * numpy.sin(radians)
        best_points = numpy.vstack((best_points, [x, y]))

    for degree in range(1, 360, 15):
        radians = numpy.radians(degree)
        x = center_x + radius * numpy.cos(radians)
        y = center_y + radius * numpy.sin(radians)
        bad_points = numpy.vstack((bad_points, [x, y]))

    for degree in range(1, 360, 30):
        radians = numpy.radians(degree)
        x = center_x + radius * numpy.cos(radians)
        y = center_y + radius * numpy.sin(radians)
        worst_points = numpy.vstack((worst_points, [x, y]))

    plt.plot(*best_points.T)
    plt.plot(*bad_points.T)
    plt.plot(*worst_points.T)

    distance, path = fastdtw(best_points, bad_points)

    print(distance, path)

    distance, path = fastdtw(best_points, worst_points)

    print(distance, path)

    plt.show()
    # print(points)


class TestGraph(TestCase):
    def test_arctan(self):
        x = 1
        y = 0

        print(numpy.arctan(y/x))

        # Expected angle of 0 rad
        numpy.testing.assert_equal(int(numpy.arctan(y/x)), 0)


if __name__ == '__main__':
    create_circle()
