"""
My Python spin on this:
http://burakkanber.com/blog/machine-learning-genetic-algorithms-in-javascript-part-2/
"""

import sys
import random
import math
import time
from elements import elements


class Chromosome(object):
    def __init__(self, members):
        self.members = members
        self.weight = 0
        self.value = 0
        self.max_weight = 1000
        self.mutation_rate = 0.7
        self.score = 0
        for element in self.members:
            if not self.members[element].get('active') is None:
                self.members[element]['active'] = int(round(random.random()))
        self.mutate()
        self.calc_score()

    def mutate(self):
        if self.mutation_rate < random.random():
            return
        element = self.members.keys()[random.randint(0, len(self.members.keys()) - 1)]
        self.members[element]['active'] = 0 if self.members[element]['active'] else 1

    def calc_score(self):
        self.value = 0
        self.weight = 0
        self.score = 0
        for element in self.members:
            if self.members[element]['active']:
                self.value += self.members[element]['value']
                self.weight += self.members[element]['weight']
        self.score = self.value
        if self.weight > self.max_weight:
            self.score -= (self.weight - self.max_weight) * 50
        return self.score

    def crossover(self, other):
        child1 = {}
        child2 = {}
        i = 0
        for element in elements:
            if i % 2 == 0:
                child1[element] = self.members[element]
                child2[element] = other.members[element]
            else:
                child2[element] = self.members[element]
                child1[element] = other.members[element]
            i += 1
        child1 = Chromosome(child1)
        child2 = Chromosome(child2)
        return [child1, child2]


class Population(object):
    def __init__(self, size=20, elements=elements):
        self.size = size
        self.elements = elements
        self.elitism = 0.2
        self.chromosomes = []
        self.fill()

    def fill(self):
        while len(self.chromosomes) < self.size:
            if len(self.chromosomes) < self.size / 3:
                self.chromosomes.append(Chromosome(self.elements))
            else:
                self.mate()

    def sort(self):
        self.chromosomes.sort(key=lambda x: x.calc_score())

    def kill(self):
        target = math.floor(self.elitism * len(self.chromosomes))
        while len(self.chromosomes) > target:
            self.chromosomes.pop()

    def mate(self):
        key1 = self.chromosomes[random.randint(0, len(self.chromosomes) - 1)]
        key2 = key1
        while key2 == key1:
            key2 = self.chromosomes[random.randint(0, len(self.chromosomes) - 1)]
        children = key1.mate_with(key2)
        self.chromosomes += children

    def generation(self):
        self.sort()
        self.kill()
        self.mate()
        self.fill()
        self.sort()

    def run(self, threshold, no_improvement, last_score, i):
        if not threshold:
            threshold = 1000
        if not no_improvement:
            no_improvement = 0
        if not last_score:
            last_score = False
        if not i:
            i = 0

        if no_improvement < threshold:
            last_score = self.chromosomes[0].calc_score()
            self.generation()

            if last_score >= self.chromosomes[0].calc_score():
                no_improvement += 1
            else:
                no_improvement = 0

            i += 1

            if i % 10 == 0:
                self.display(i, no_improvement)
            time.sleep(0.1)
            self.run(threshold, no_improvement, last_score, i)
            return False

        self.display(i, no_improvement)

    def display(self, i, no_improvement):
        print "Generation:\t" + str(i)
        print "Best Value:\t" + str(self.chromosomes[0].score)
        print "Weight:\t"+ str(self.chromosomes[0].weight)
        print "No change in:\t" + str(no_improvement)


def main():
    p = Population()
    p.run()

if __name__ == '__main__':
    sys.exit(main())