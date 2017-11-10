import order
import random
import copy
class MinHashing:
    my_order=order.ListOrder()
    orders=[]
    total_union_list=[]
    number_of_permutations=0
    def __init__(self, number_of_permutations):
        self.number_of_permutations=number_of_permutations
    def min_hash(self, sets):
        boolean_matrix=self.make_boolean_matrix(sets)
        signature_matrix=self.find_signature_matrix(boolean_matrix, self.number_of_permutations)
        return self.estimate_jaccard_similarity(signature_matrix)
    def estimate_jaccard_similarity(self,signature_matrix):
        number_of_columns=len(signature_matrix)
        number_of_rows=len(signature_matrix[0])
        result_list=[0 for i in range(number_of_rows-1)]
        for i in range(number_of_rows-1):
            for j in range(number_of_columns):
                if signature_matrix[j][i] == signature_matrix[j][number_of_rows-1]:
                    result_list[i]+=1
        # Change result_list to probabilities
        result_list = map(lambda x: float(float(x)/float(self.number_of_permutations)), result_list)
        return result_list
    def find_signature_matrix(self, boolean_matrix, number_of_permutations):
        number_of_sets=len(boolean_matrix)
        signature_matrix=[[0]*number_of_sets for i in range(number_of_permutations)]
        for i in range(number_of_permutations):
            self.my_order.highest_used_index = 0
            for j in range(number_of_sets):
                steps_to_next_one = self.find_next_column_one(boolean_matrix, j)
                self.my_order.used_indices(steps_to_next_one)
                signature_matrix[i][j]=steps_to_next_one
            self.orders.append(copy.copy(self.my_order))
        return signature_matrix
    def find_next_column_one(self, matrix, column_index):
        number_of_shingles=len(matrix[0])
        for i in range(number_of_shingles):
            if i>= len(self.my_order):
                self.my_order.append(random.randint(0, number_of_shingles-1))
                self.my_order.highest_used_index += 1
            elif i >= self.my_order.highest_used_index:
                self.my_order[i] = random.randint(0, number_of_shingles-1)
                self.my_order.highest_used_index += 1
            current=self.my_order[i]
            if matrix[column_index][current] == 1:
                return i
        return 0
    def union_all(self, sets):
        union=set()
        inters=sets[0].intersection(sets[1])
        for current_set in sets:
            if not isinstance(current_set, set):
                return "Error"
            union=union.union(current_set)
        return union
    def make_boolean_matrix(self, sets):
        union = self.union_all(sets)
        rows = list(union)
        self.total_union_list=rows
        number_of_columns = len(sets)
        number_of_rows = len(rows)
        matrix = [[0]*number_of_rows for i in range(number_of_columns)]
        for i in range (number_of_columns):
            for j in range (number_of_rows):
                if rows[j] in sets[i]:
                    matrix[i][j]=1
        return matrix
    def make_boolean_single(self, set):
        number_of_rows = len(self.total_union_list)
        column=[]
        for j in range(number_of_rows):
            if self.total_union_list[j] in set:
                column.append(1)
            else:
                column.append(0)
        return column
    def find_signature_row(self, row):
        number_of_sets=len(row)
        result=[]
        for i in range(self.number_of_permutations):
            steps_to_next_one = self.find_next_single_one(row, i)
            result.append(steps_to_next_one)
        return result
    def find_next_single_one(self, row, permutation_number):
        number_of_shingles=len(self.total_union_list)
        for i in range(len(row)):
            temp_list=self.orders[permutation_number]
            if i>= len(temp_list):
                temp_list.append(random.randint(0, number_of_shingles-1))
                temp_list.highest_used_index += 1
            elif i >= temp_list.highest_used_index:
                temp_list[i] = random.randint(0, number_of_shingles-1)
                temp_list += 1
            current=temp_list[i]
            self.orders[permutation_number]=temp_list
            if row[current] == 1:
                return i
        return 0