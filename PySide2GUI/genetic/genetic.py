import numpy
import random
import matplotlib.pyplot as plt

import functools


class Population:
    def __init__(self):
        self.population_size = 20
        self.population = []

        for i in range(0, self.population_size, 1):
            self.population.append(Dron())

        # print(self.drons)

    def print_plot(self):
        for pop in self.population:
            plt.plot(*pop.get_dna()[:, :-1].T)
        plt.show()


class Dron:
    def __init__(self):
        self.dna = Dna()

    def get_dna(self):
        return self.dna.get_dna()


class Dna:
    def __init__(self, genes=None, commands=[['move', 10, 20], ['rotate', 30], ['move', 10, 10]]):
        # def __init__(self, genes=None, commands=None):
        # x y current_rotation
        # start at beginning of curve, for test circle
        self.lifespan = 100
        self.genes = numpy.array([[1, 0, 0]])
        self.issued_commands = []
        # Commands called from the list!
        self.called_commands = []

        if commands:
            #self.genes = genes
            self.old_called_commands = commands

            for i in self.old_called_commands:
                if i[0] == 'move':
                    self.command_move(i[1], i[2])
                elif i[0] == 'rotate':
                    self.command_rotate(i[1])
        else:
            for i in range(1, self.lifespan, 1):
                self.my_list = [self.command_rotate(numpy.random.randint(0, 359)), self.command_move(
                    numpy.random.randint(10, 100), numpy.random.randint(10, 100))]
                self._select_random_function()

    def get_dna(self):
        return self.genes

    def crossover(self):
        # TODO
        return

    def mutation(self):
        # TODO
        return

    def translate_to_dronish(self):
        return '\n'.join(self.issued_commands)

    # allowed commands

    def command_move(self, x, y, z=0):
        # we dont use Z for simulation, for now 2D
        r_x, r_y = self._calculate_rotation_xy(x, y)

        self.genes = numpy.vstack(
            (self.genes, numpy.array([r_x, r_y, self.genes[-1][2]])))

        self.called_commands.append(['move', x, y])
        self.issued_commands.append(f'go {x} {y} 0 60')

    @staticmethod
    def _normalize_rotation(deg: int):
        angle = deg % 360

        angle = (angle + 360) % 360

        if (angle > 180):
            angle -= 360

        return angle

    def _calculate_rotation_xy(self, x, y):
        radians = numpy.radians(self.genes[-1][2])
        c, s = numpy.cos(radians), numpy.sin(radians)
        j = numpy.matrix([[c, s], [-s, c]])
        m = numpy.dot(j, [x, y])

        return float(m.T[0]), float(m.T[1])

    def command_rotate(self, deg: int):
        # TODO: rotation clockwise, counterclockwise? or can they take negative? @Matej
        self.genes[-1, 2] = self._normalize_rotation(self.genes[-1][2] + deg)
        self.called_commands.append(['rotate', deg])
        self.issued_commands.append(f'cw {deg}')

    def _select_random_function(self):
        random.choice(self.my_list)


if __name__ == '__main__':
    population = Population()
    population.print_plot()
