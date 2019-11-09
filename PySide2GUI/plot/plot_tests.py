from unittest import TestCase, mock
import plot
import numpy


class TestGraph(TestCase):
    def test_zero_coord(self):
        drone = plot.Drone()

        expected_result = numpy.array([[0, 0, 0]]).T

        numpy.testing.assert_array_equal(
            drone.get_current_coord(), expected_result)

    #@mock.patch('plot.Plot.')
    def test_receive_up_twice(self):
        drone = plot.Drone()

        drone.receive_movement('up', 10)

        expected_result = numpy.array([[0, 0, 10]]).T

        numpy.testing.assert_array_equal(
            drone.get_current_coord(), expected_result)

        drone.receive_movement('up', 15)

        expected_result = numpy.array([[0, 0, 25]]).T

        numpy.testing.assert_array_equal(
            drone.get_current_coord(), expected_result)

