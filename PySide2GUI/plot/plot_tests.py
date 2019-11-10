from unittest import TestCase, mock
import plot
import numpy


class TestGraph(TestCase):
    def test_zero_coord(self):
        drone = plot.Drone()

        expected_result = numpy.array([0, 0, 0])

        numpy.testing.assert_array_equal(
            drone.get_current_coord(), expected_result)

    #@mock.patch('plot.Plot.')
    def test_receive_up_twice(self):
        drone = plot.Drone()

        drone.receive_go(0, 0, 10)

        expected_result = numpy.array([0, 0, 10])

        numpy.testing.assert_array_equal(
            drone.get_current_coord(), expected_result)

        drone.receive_go(0, 0, 15)

        expected_result = numpy.array([0, 0, 25])

        numpy.testing.assert_array_equal(
            drone.get_current_coord(), expected_result)

    def test_receive_rotation_below_zero(self):
        drone = plot.Drone()

        drone.receive_rotation(-30)

        numpy.testing.assert_equal(drone.get_current_rotation(), -30)


    def test_receive_rotation_above_180(self):
        drone = plot.Drone()

        drone.receive_rotation(190)

        numpy.testing.assert_equal(drone.get_current_rotation(), -170)

    def test_receive_rotation_above_360(self):
        drone = plot.Drone()

        drone.receive_rotation(370)

        numpy.testing.assert_equal(drone.get_current_rotation(), 10)

    def test_arctan(self):
        x = 1
        y = 0

        print(numpy.arctan(y/x))

        # Expected angle of 0 rad
        numpy.testing.assert_equal(int(numpy.arctan(y/x)), 0)

