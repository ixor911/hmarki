from Pyro4 import expose
import random
import pickle


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.max_pass_len = None
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers


        self.rules = [
            "qwertyuiopasdfghjklzxcvbnm",
            "QWERTYUIOPASDFGHJKLZXCVBNM",
            "1234567890",
            "!@#-=$%^&*()_+}{;:'/.,<>?|[]"
        ]

        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))

        self.max_pass_len = self.read_input()

        vocabulary = self.get_full_voc(self.rules)
        full_amount = self.calc_max_varieties(vocabulary, self.max_pass_len)
        step = int(full_amount / len(self.workers))

        mapped = []
        for i in range(0, len(self.workers)):
            start = i * step + 1
            end = (i + 1) * step

            mapped.append(self.workers[i].mymap(start, end, vocabulary))

        self.write_output(mapped)

    @staticmethod
    @expose
    def mymap(start, end, vocabulary):
        passes = []
        for i in range(start, end + 1):
            passes.append(Solver.find_pass_by_index(i, vocabulary))

        return passes

    def read_input(self):

        f = open(self.input_file_name, 'r')
        pass_len = int(f.readline())

        return pass_len

    def write_output(self, output):
        with open(self.output_file_name, 'w') as f:
            for a in output:
                f.write('\n'.join(a.value))

        print("output done")

    @staticmethod
    @expose
    def get_full_voc(rules):
        voc = ""
        for rule in rules:
            voc += rule

        return voc

    @staticmethod
    @expose
    def create_pass(vocabulary, length):
        password = ""
        for i in range(0, length):
            j = random.randint(0, len(vocabulary) - 1)
            password += vocabulary[j]

        return password

    @staticmethod
    @expose
    def calc_max_varieties(vocabulary, length):
        varieties = 0
        for i in range(1, length + 1):
            varieties += len(vocabulary) ** i
        return varieties

    @staticmethod
    @expose
    def find_elem_index_small(current_index, prev_max_index):
        index = 0
        while current_index - prev_max_index * index > 0:
            index += 1

        return index, current_index - prev_max_index * (index - 1)

    @staticmethod
    @expose
    def find_pass_len(index, voc_len):
        true_index = index
        pass_len = 1
        while true_index - voc_len ** pass_len > 0:
            true_index -= voc_len ** pass_len
            pass_len += 1

        return pass_len, true_index

    @staticmethod
    @expose
    def find_indexes_list_by_index(vocabulary, index):
        voc_len = len(vocabulary)
        pass_len, index = Solver.find_pass_len(index, voc_len)

        list_indexes = []
        for i in range(pass_len - 1, -1, -1):
            elem_index, index = Solver.find_elem_index_small(index, voc_len ** i)
            list_indexes.append(elem_index - 1)

        return list_indexes

    @staticmethod
    @expose
    def get_pass_by_indexes(vocabulary, list_indexes):
        password = ""
        for index in list_indexes:
            password += vocabulary[index]

        return password

    @staticmethod
    @expose
    def find_pass_by_index(index, vocabulary):
        list_indexes = Solver.find_indexes_list_by_index(vocabulary, index)
        return Solver.get_pass_by_indexes(vocabulary, list_indexes)
