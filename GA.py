import numpy as np
import random
from params import get_args
from Shop import Shop
from utils import *


class GA(object):
    def __init__(self, args, shop):
        self.shop = shop
        self.cross_rate = args.cross_rate
        self.mutate_rate = args.mutate_rate
        self.pop_size = args.pop_size
        self.elite_number = args.elite_number

        self.chrom_size = self.shop.job_nb * self.shop.op_nb
        self.pop = []

    def encode(self):
        init_pop = []
        for _ in range(self.pop_size):
            one_string = []
            for _ in range(self.shop.op_nb):
                one_string += list(np.random.permutation(self.shop.job_nb))
            random.shuffle(one_string)
            two_string = [random.randint(0, self.shop.machine_nb-1) for _ in range(self.chrom_size)]
            individual = np.vstack([one_string, two_string])
            init_pop.append(individual)
        return np.array(init_pop)

    def decode(self, pop1):
        fuzzy_fitness = []
        certain_fitness = []
        for individual in pop1:
            fuzzy_completion_time = self.shop.process_decode1(individual)
            fuzzy_fitness.append(fuzzy_completion_time)
            certain_fitness.append(value(fuzzy_completion_time))
        return fuzzy_fitness, certain_fitness

    def selection(self, pop2, fuzzy_fitness, certain_fitness):
        """
        tournament selection + elite_strategy
        """
        pop2 = pop2.tolist()
        sorted_pop = sorted(pop2, key=lambda x: certain_fitness[pop2.index(x)], reverse=False)
        new_pop = sorted_pop[:self.elite_number]
        while len(new_pop) < self.pop_size:
            index1, index2 = random.sample(list(range(10, self.pop_size)), 2)
            if rank(fuzzy_fitness[index1], fuzzy_fitness[index2]) == fuzzy_fitness[index1]:
                new_pop.append(pop[index2])
            else:
                new_pop.append(pop[index1])
        return np.array(new_pop)

    def crossover_machine(self, pop_machine):
        """
        two point crossover (TPX)
        """
        temp = pop_machine.copy().tolist()
        new_pop = []
        while len(temp) != 0:
            parent1, parent2 = random.sample(temp, 2)
            temp.remove(parent1)
            temp.remove(parent2)
            if random.random() < self.cross_rate:
                pos1, pos2 = sorted(random.sample(list(range(self.chrom_size)), 2))
                offspring1 = parent1[:pos1] + parent2[pos1:pos2] + parent1[pos2:]
                offspring2 = parent2[:pos1] + parent1[pos1:pos2] + parent2[pos2:]
            else:
                offspring1 = parent1
                offspring2 = parent2
            new_pop.append(offspring1)
            new_pop.append(offspring2)
        return np.array(new_pop)

    def crossover_job(self, pop_job):
        """
        generalisation of the precedence preservative crossover (PPX)
        """
        temp = pop_job.copy().tolist()
        new_pop = []
        for parent1 in temp:
            if random.random() < self.cross_rate:
                new_individual = []
                parent2 = pop_job[random.randint(0, self.pop_size-1)].tolist()
                string = random.choices([0, 1], k=self.chrom_size)
                for choose in string:
                    if int(choose) == 0:
                        new_individual.append(parent1[0])
                        parent2.remove(parent1[0])
                        parent1 = parent1[1:]
                    else:
                        new_individual.append(parent2[0])
                        parent1.remove(parent2[0])
                        parent2 = parent2[1:]
                new_pop.append(new_individual)
            else:
                new_pop.append(parent1)
        return np.array(new_pop)

    def mutation(self, part):
        """
        swap
        """
        for individual in part:
            if random.random() < self.mutate_rate:
                pos1, pos2 = random.sample(list(range(self.chrom_size)), 2)
                individual[pos1], individual[pos2] = individual[pos2], individual[pos1]
        return part

    @staticmethod
    def elite_strategy(pop3, fitness):
        best_fitness = [np.inf, np.inf, np.inf]
        best_individual = None
        for k, individual in enumerate(pop3):
            if rank(fitness[k], best_fitness) == best_fitness:
                best_fitness = fitness[k]
                best_individual = individual
        return best_individual, best_fitness


if __name__ == '__main__':
    args = get_args()
    job, machine, op, pt = read('./instance1.txt')
    shop = Shop(job, machine, op, pt)
    method = GA(args, shop)

    best_one = None
    best_fit = [np.inf, np.inf, np.inf]

    best_list = []
    mean_list = []

    pop = method.encode()
    for i in range(args.max_generation):
        fuzzy_fit, certain_fit = method.decode(pop)
        new_one, new_fit = method.elite_strategy(pop, fuzzy_fit)
        if i % 100 == 0:
            print(f'{i}:old best:{best_fit}, now best:{new_fit}, now mean:{np.mean(certain_fit)}')
        if rank(best_fit, new_fit) == best_fit:
            best_fit = new_fit
            best_one = new_one
        best_list.append(value(best_fit))
        mean_list.append(np.mean(certain_fit))

        pop_select = method.selection(pop, fuzzy_fit, certain_fit)
        pop_cross_job = method.crossover_job(pop_select[:, 0, :])
        pop_mutate_job = method.mutation(pop_cross_job)
        pop_cross_machine = method.crossover_machine(pop_select[:, 1, :])
        pop_mutate_machine = method.mutation(pop_cross_machine)
        new = []
        for a, b in zip(pop_mutate_job, pop_mutate_machine):
            new.append([a, b])
        pop = np.array(new)
    fct = shop.process_decode1(best_one)
    shop.draw_fuzzy_gantt()
    draw(best_list, mean_list)





