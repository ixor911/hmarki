
import random



class DictionaryCreator:
    def __init__(self):
        self.rules = [
            "qwertyuiopasdfghjklzxcvbnm",
            "QWERTYUIOPASDFGHJKLZXCVBNM",
            "1234567890",
            "!@#-=$%^&*()_+}{;:'/.,<>?|[]"
        ]

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
            varieties += len(vocabulary) ** i
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

    def find_pass_by_index(self, index, vocabulary):
        list_indexes = self.find_indexes_list_by_index(vocabulary, index)
        return self.get_pass_by_indexes(vocabulary, list_indexes)


lol = DictionaryCreator()
print(lol.calc_max_varieties(lol.get_full_voc(lol.rules), 2))
print(lol.find_pass_by_index(8190, lol.get_full_voc(lol.rules)))

passes = ['z^Z',
          'tQ_o',
          'RlX7%',
          'Xlfp#-',
          'L.FRZP:',
          'KR8)sLZi',
          'W_R[aGA$@',
          ']1+wY)=)Zw',
          'e)@q/c6=*FZ',
          'Rhcle7Q<uT2I',
          'C1<7k1/TTRe/U',
          'D^x,;#?&W9BWjA']

