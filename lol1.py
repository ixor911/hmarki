from Pyro4 import expose
import random

class DictionaryCreator:
    def __int__(self):
        self.rules = [
            "qwertyuiopasdfghjklzxcvbnm",
            "QWERTYUIOPASDFGHJKLZXCVBNM",
            "1234567890",
            "!@#-=$%^&*()_+}{;:'/.,<>?|[]",
        ]
        self.vocabulary = self.get_full_voc(self.rules)

    def get_vocabulary(self):
        return self.vocabulary

    @staticmethod
    def get_full_voc(rules):
        voc = ""
        for rule in rules:
            voc += rule

        return voc

    @staticmethod
    def create_pass(vocabulary, length):
        password = ""
        for i in range(0, length):
            j = random.randint(0, len(vocabulary) - 1)
            password += vocabulary[j]

        return password

    @staticmethod
    def calc_max_varieties(vocabulary, length):
        varieties = 0
        for i in range(1, length + 1):
            varieties += len(vocabulary) ** length
        return varieties

    @staticmethod
    def find_elem_index_small(current_index, prev_max_index):
        index = 0
        while current_index - prev_max_index * index > 0:
            index += 1

        return index, current_index - prev_max_index * (index - 1)

    @staticmethod
    def find_pass_len(index, voc_len):
        true_index = index
        pass_len = 1
        while true_index - voc_len ** pass_len > 0:
            true_index -= voc_len ** pass_len
            pass_len += 1

        return pass_len, true_index

    def find_indexes_list_by_index(self, vocabulary, index):
        voc_len = len(vocabulary)
        pass_len, index = self.find_pass_len(index, voc_len)

        list_indexes = []
        for i in range(pass_len - 1, -1, -1):
            elem_index, index = self.find_elem_index_small(index, voc_len ** i)
            list_indexes.append(elem_index - 1)

        return list_indexes

    @staticmethod
    def get_pass_by_indexes(vocabulary, list_indexes):
        password = ""
        for index in list_indexes:
            password += vocabulary[index]

        return password

    def find_pass_by_index(self, index):
        list_indexes = self.find_indexes_list_by_index(self.vocabulary, index)
        return self.get_pass_by_indexes(self.vocabulary, list_indexes)



class Solver:
    def __int__(self, workers=[], input_file_name=[None], output_file_name=[None]):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        self.dictCreator = DictionaryCreator()
        self.max_pass_len = 2
        print("Inited")

    def solve(self):
        print("Job Started")
        print(self.max_pass_len)
        print("Workers %d" % len(self.workers))

        vocabulary = self.dictCreator.get_vocabulary()
        full_amount = self.dictCreator.calc_max_varieties(vocabulary, self.max_pass_len)
        step = int(full_amount / len(self.workers))


    @staticmethod
    @expose
    def mymap(start, end, dict_creator):
        passes = []
        for i in range(start, end + 1):
            passes.append(dict_creator.find_pass_by_index(i))

        return passes

    def write_output(self, output):
        output = output.sort()

        f = open(self.output_file_name, "w")
        for a in output:
            for i in a.value:
                f.write(str(i) + '\n')

        f.close()
        print("output done")


s = Solver()
s.solve()




