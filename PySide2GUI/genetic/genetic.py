import numpy
import random
import matplotlib.pyplot as plt

from fastdtw import fastdtw

STEP = 0


class Population:
    def __init__(self, test_data):
        self.population_size = 100
        self.population = []
        self.matingpool = []
        self.test_data = test_data
        self.max_fitness = 1
        self.best = 0

        for i in range(0, self.population_size, 1):
            self.population.append(Dron(test_data))
        #print('expected population size:', self.population_size)
        #print('created pop len:', len(self.population))

    def print_plot(self):
        while True:
            # i = True
            if all(item.get_dna().get_lifespan() == True for item in self.population):
                self.evaluate_fitness()
                self.natural_selection()
                print('max fitness', self.max_fitness)
                print('----------------------\n')
                # if i:
                #     for pop in self.population:
                #         #print(self.population)
                #         print('Genes?', pop.get_dna().get_genes()[:, :-1].T)
                #         plt.plot(*pop.get_dna().get_genes()[:, :-1].T)
                #         #print('test_data', self.test_data)
                #         plt.plot(*self.test_data.T)
                #     plt.show()
                # break
                if (self.max_fitness > 20):
                    for pop in self.population:
                        plt.plot(*pop.get_dna().get_genes()[:, :-1].T)
                    plt.show()

    def evaluate_fitness(self):
        maxfit = 0
        self.best = 0
        # Iterate through all rockets and calcultes their fitness
        for i in range(0, len(self.population)-1):
            # calculate fitness
            self.population[i].calculate_fitness()

            # normalize fitness

            if (self.population[i].get_fitness() > maxfit):
                maxfit = self.population[i].get_fitness()
                self.best = i
                self.max_fitness = maxfit

        for i in range(0, len(self.population)-1):
            self.population[i].set_fitness(maxfit)

        # Take population fitness  and scale it from 1 to 100

        for i in range(0, len(self.population)-1):

            if i == self.best:
                #print('best')
                n = int(self.population[i].get_fitness() * 200)
                # import sys
                # sys.exit()

            else:
                self.population[i]._fitness = self.population[i]._fitness * 0.5
                n = int(self.population[i].get_fitness() * 100)

            for j in range(0, n, 1):

                self.matingpool.append(self.population[i])

        # print('best', best)
        # import sys
        # sys.exit()

        #print('mating pool', len(self.matingpool))

    def natural_selection(self):
        new_population = []

        for i in (0, len(self.population)):
            if i == self.best:
                child = self.population[i]
            else:
                # pick random DNA
                parentA = random.choice(self.matingpool).get_dna()
                parentB = random.choice(self.matingpool).get_dna()
                # Create child by crossover
                #child_dna = Dna()
                orig_child_genes = parentA.crossover(parentB)
                # print('TEST_OUR_PRE!', child_genes)
                # child_dna.reset_commands(child_genes)

                #print('child', child_genes)
                # import sys
                # sys.exit("Error message")
                #mute = Dna.mutation(child)
                # print(child_genes)
                # print(child_dna)
                # print(child_dna.get_commands())

                #child = Dron(self.test_data)
                
                child_genes = self.population[i]._dna.mutation(orig_child_genes)
                # numpy.testing.assert_equal
                print(numpy.array_equal(orig_child_genes, child_genes))
                # print('TEST_OUR', child_genes)
                # import sys
                # sys.exit("Error message")
                # child.set_commands(child_genes)
            

            #print('TEST', Dron(self.test_data).set_commands(child_genes))
            new_population.append(
                child)
            #print('new_pop', new_population)
        #print('before selection', self.population)
        self.matingpool = []
        self.population = new_population


class Dron:
    def __init__(self, test_data, commands=None):
        self._dna = Dna(commands=commands)
        # print(self._dna)
        self._fitness = 0
        self.test_data = test_data

    def get_dna(self):
        return self._dna

    def get_commands(self):
        return self._dna.get_commands()

    def set_commands(self, commands):
        self._dna = Dna(commands=commands)

    def get_fitness(self):
        return self._fitness

    def set_fitness(self, maxfit):
        self._fitness /= maxfit
        #print('fitness', self._fitness)

    def calculate_fitness(self):
        distance, path = fastdtw(
            self.test_data, numpy.array(self.get_dna().get_genes())[:, :-1])
        # First iteration of fitness
        self._fitness = 400000 / (distance * 2)


class Dna:
    # def __init__(self, commands=[['move', 10, 20], ['rotate', 30], ['move', 10, 10]]):
    def __init__(self, commands=None):
        # x y current_rotation
        # start at beginning of curve, for test circle
        self.genes_length = 50
        self.lifespan = False
        self.count = 0
        self.genes = numpy.array([[75, 0, 0]])
        self.recall = False

        # Commands issued to drone
        self.issued_commands = []
        # Commands called from the list!
        self.called_commands = []

        # command setting
        self.my_list = [self.command_rotate, self.command_move]

        #print('commands', commands)
        if (commands is not None):
            # print()
            if len(commands):

                #self.genes = genes
                #print('do we inherit', commands)
                # import sys
                # sys.exit("Error message")
                self.old_called_commands = commands
                #print('init1', self.called_commands)

                #print('length', len(self.old_called_commands))

                for i in self.old_called_commands:
                    #print('we are running child', i)
                    # print(i)
                    self.count += 0
                    if i[0] == 'move':
                        self.command_move(i[1], i[2], None)
                    elif i[0] == 'rotate':
                        self.command_rotate(None, None, i[1])
                # it died\
                #print('DONE', i)
                self.lifespan = True
        else:
            for i in range(1, self.genes_length, 1):
                # print(i)
                self.count += 1
                random.choice(self.my_list)(
                    numpy.random.randint(20, 40), numpy.random.randint(20, 40), numpy.random.randint(-30, 30))
                # self._select_random_function()
            # it died
            self.lifespan = True

    def get_lifespan(self):
        return self.lifespan

    def get_genes(self):
        # print(self.genes)
        return self.genes

    def set_commands(self, genes):
        #self.genes = None
        self.called_commands = genes

    def get_commands(self):
        return self.called_commands

    def get_count(self):
        return self.count

    def crossover(self, partner):
        new_genes = []
        # random mid
        mid = numpy.floor(numpy.random.randint(len(self.called_commands)))
        # print(self.called_commands)
        # print(mid)
        for i in range(0, len(self.called_commands), 1):
            # take one half of genes from partner
            if (i > mid):
                new_genes.append(self.called_commands[i])
                #print('my', self.called_commands[i])
            else:
                new_genes.append(partner.called_commands[i])
                #print('partner', partner.called_commands[i])
        # print('new',new_genes)
        # import sys
        # sys.exit("Error message")
        return new_genes

    def mutation(self, genes):
        for i in range(0, len(genes)-1):
            # 1% chance to evolve
            if (numpy.random.uniform() < 0.05):
                print('It is mutating!')
                random.choice([self.command_rotate, self.command_move])(
                    numpy.random.randint(20, 40), numpy.random.randint(20, 40), numpy.random.randint(-30, 30), True)
                genes[i] = self.recall
        return genes

    def translate_to_dronish(self):
        return '\n'.join(self.issued_commands)

    # allowed commands

    def command_move(self, *args):  # x, y, z=0):
        x = args[0]
        y = args[1]
        # print(x)
        # print(y)
        # we dont use Z for simulation, for now 2D
        r_x, r_y = self._calculate_rotation_xy(x, y)

        self.genes = numpy.vstack(
            (self.genes, numpy.array([r_x, r_y, self.genes[-1][2]])))

        if len(args) == 4:
            print('True')
            self.recall = numpy.array(['move', x, y])
        else:
            print('Lie')
            self.called_commands.append(['move', x, y])
        #print('move', self.called_commands)

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

    def command_rotate(self, *args):  # deg: int):
        deg = args[2]
        # TODO: rotation clockwise, counterclockwise? or can they take negative? @Matej
        self.genes[-1, 2] = self._normalize_rotation(self.genes[-1][2] + deg)

        if len(args) == 4:
            print('True')
            self.recall = numpy.array(['rotate', deg])
        else:
            print('Lie')
            self.called_commands.append(['rotate', deg])
        #print('rotate', self.called_commands)

        self.issued_commands.append(f'cw {deg}')

    def _select_random_function(self):
        random.choice(self.my_list)


class TestCurve:
    @staticmethod
    def create_circle(center_x=0, center_y=0, radius=1):
        # testing code for equality to calculate validity and weight of gen alg
        # NOTE: test confirmed that weight calculated by this procedure can be used to evaluate fitness of gen alg
        points = numpy.array([[radius, 0]])

        for degree in range(1, 360, 1):
            radians = numpy.radians(degree)
            x = center_x + radius * numpy.cos(radians)
            y = center_y + radius * numpy.sin(radians)
            points = numpy.vstack((points, [x, y]))

        return points


if __name__ == '__main__':
    test_data = TestCurve.create_circle(0, 0, 75)
    population = Population(test_data)
    population.print_plot()
