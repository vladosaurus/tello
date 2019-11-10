import numpy
import random
import matplotlib.pyplot as plt


class Population:
    def __init__(self):
        self.population_size = 20
        self.population = []

        for i in range(0, self.population_size, 1):
            self.population.append(Dron())

        #print(self.drons)

    def print_plot(self):
        for pop in self.population:
            plt.plot(*pop.get_dna()[:,:-1].T)
        plt.show()

class Dron:
    def __init__(self):
        self.dna = Dna()

    def get_dna(self):
        return self.dna.get_dna()

class Dna:
    def __init__(self):
        # x y current_rotation
        # start at beginning of curve, for test circle
        self.lifespan = 100
        self.dna = numpy.array([[1, 0, 0]])
        self.issued_commands = []

        for i in range(1, self.lifespan, 1):
            self.my_list = [self.command_rotate(numpy.random.randint(0, 359)), self.command_move(
                numpy.random.randint(10, 100), numpy.random.randint(10, 100))]
            self._select_random_function()

    def get_dna(self):
        return self.dna

    def translate_to_dronish(self):
        return '\n'.join(self.issued_commands)

    # allowed commands

    def command_move(self, x, y, z=0):
        # we dont use Z for simulation, for now 2D
        r_x, r_y = self._calculate_rotation_xy(x, y)

        self.dna = numpy.vstack(
            (self.dna, numpy.array([r_x, r_y, self.dna[-1][2]])))

        return f'go {x} {y} 0 60'

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
        # TODO: rotation clockwise, counterclockwise? or can they take negative? @Matej
        self.dna[-1, 2] = self._normalize_rotation(self.dna[-1][2] + deg)
        return f'cw {deg}'

    def _select_random_function(self):
        selected = random.choice(self.my_list)
        self.issued_commands.append(selected)


if __name__ == '__main__':
    population = Population()
    population.print_plot()
