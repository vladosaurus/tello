import numpy
import random


class Dna:
    def __init__(self):
        # x y rotation
        self.dna = numpy.array([[0, 0, 0]])
        #print(self.dna[-1][2])

        for i in range(1, 10, 1):
            self.my_list = [self.command_rotate(numpy.random.randint(0, 359)), self.command_move(
                numpy.random.randint(10, 100), numpy.random.randint(10, 100))]
            #print(self.my_list)
            print('----')
            self._select_random_function()

    def translate_to_dronish(self):
        # TODO: return textfile for dron in dronish
        return self.dna

    # allowed commands

    def command_move(self, x, y, z=0):
        # we dont use Z for simulation, for now 2D
        r_x, r_y = self._calculate_rotation_xy(x, y)

        self.dna = numpy.vstack(
            (self.dna, numpy.array([r_x, r_y, self.dna[-1][2]])))

    @staticmethod
    def _normalize_rotation(deg: int):
        angle = deg % 360

        angle = (angle + 360) % 360

        if (angle > 180):
            angle -= 360

        return angle

    def _calculate_rotation_xy(self, x, y):
        radians = numpy.radians(self.dna[-1][2])
        c, s = numpy.cos(radians), numpy.sin(radians)
        j = numpy.matrix([[c, s], [-s, c]])
        m = numpy.dot(j, [x, y])

        return float(m.T[0]), float(m.T[1])

    def command_rotate(self, deg: int):
        #self.current_rotation = self._normalize_rotation(self.current_rotation + deg)
        print(self.dna[-1])
        print(deg)
        print(self._normalize_rotation(self.dna[-1][2] + deg))
        self.dna[-1, 2] = self._normalize_rotation(self.dna[-1][2] + deg)

    def _select_random_function(self):
        random.choice(self.my_list)


if __name__ == '__main__':
    dna = Dna()
    print(dna.translate_to_dronish())
