from utils import *
import matplotlib.pyplot as plt
import matplotlib.colors as mc


class Job(object):
    def __init__(self, index, op_nb, total_fuzzy_pt):
        self.index = index
        self.op_nb = op_nb
        self.fuzzy_pt = total_fuzzy_pt[index]

        self.current_op = 0
        self.current_time = [0, 0, 0]

    def process(self, start_time, process_time):
        self.current_op += 1
        self.current_time = addition(start_time, process_time)


class Machine(object):
    def __init__(self, index):
        self.index = index
        self.current_time = [0, 0, 0]

        self.op_start_time = []
        self.op_end_time = []
        self.job_index = []
        self.op_index = []

    def process(self, start_time, process_time, job_index, op_index):
        self.current_time = addition(start_time, process_time)
        self.op_start_time.append(start_time)
        self.op_end_time.append(self.current_time)
        self.job_index.append(job_index)
        self.op_index.append(op_index)


class Shop(object):
    def __init__(self, job_nb, machine_nb, op_nb, total_fuzzy_pt):
        self.job_nb = job_nb
        self.machine_nb = machine_nb
        self.op_nb = op_nb
        self.total_fuzzy_pt = total_fuzzy_pt

        self.job_list = []
        self.machine_list = []

    def create(self):
        self.job_list = []
        self.machine_list = []
        for i in range(self.job_nb):
            self.job_list.append(Job(i, self.op_nb, self.total_fuzzy_pt))
        for i in range(self.machine_nb):
            self.machine_list.append(Machine(i))

    def process_decode1(self, solution):
        self.create()
        op_se, ma_se = solution[0], solution[1]
        for k in range(len(op_se)):
            job_index = op_se[k]
            job = self.job_list[job_index]
            machine_index = ma_se[k]
            machine = self.machine_list[machine_index]
            start_time = rank(job.current_time, machine.current_time)
            process_time = job.fuzzy_pt[job.current_op][machine_index]
            machine.process(start_time, process_time, job_index, job.current_op)
            job.process(start_time, process_time)
        fuzzy_completion_time = [0, 0, 0]
        for ma in self.machine_list:
            fuzzy_completion_time = rank(fuzzy_completion_time, ma.current_time)
        return fuzzy_completion_time

    def draw_fuzzy_gantt(self):
        plt.figure(figsize=(12, 8))
        colors = list(mc.TABLEAU_COLORS.keys())
        for ma in self.machine_list:
            y = ma.index
            plt.axhline(y, color='black')
            plt.yticks(list(range(self.machine_nb)))
            for k, start, end, o in zip(ma.job_index, ma.op_start_time, ma.op_end_time, ma.op_index):
                if start == [0, 0, 0]:
                    plt.scatter(0, y, color=colors[k])
                    plt.text(start[1], y-0.2, str(k)+str(o), verticalalignment='center', horizontalalignment='center',
                             fontsize=6)
                else:
                    triangleX = start
                    triangleY = [y, y-0.2, y]
                    plt.fill(triangleX, triangleY, colors[k])
                    plt.text(start[1], y-0.3, str(k)+str(o)+str(start), verticalalignment='center', horizontalalignment='center',
                             fontsize=6)
                triangleX = end
                triangleY = [y, y+0.2, y]
                plt.fill(triangleX, triangleY, colors[k])
                plt.text(end[1], y+0.3, str(k)+str(o)+str(end), verticalalignment='center', horizontalalignment='center', fontsize=6)
        plt.show()