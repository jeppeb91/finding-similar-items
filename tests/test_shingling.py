import unittest
import sys
import os
from os.path import dirname, abspath
parent_dir=dirname(dirname(abspath(__file__)))
sys.path.append(parent_dir)
from source import shingling, min_hashing, order, document_base
class TestShingling(unittest.TestCase):
    SHINGLE_SIZE=3
    NUMBER_OF_PERMUTATIONS=100
    file_path=os.path.join(parent_dir, "source\\resources\\dataset-CalheirosMoroRita-2017.csv")
    file_path2=os.path.join(parent_dir, "source\\resources\\new_york.txt")
    shing=shingling.Shingling(document_base.DocumentBase(os.path.join(parent_dir, "source\\resources"), SHINGLE_SIZE, NUMBER_OF_PERMUTATIONS))
    min_hasher=min_hashing.MinHashing(NUMBER_OF_PERMUTATIONS)
    def test_read_file(self):
        read_file=self.shing.read_file(self.file_path)
        self.assertFalse(not isinstance(read_file, str), "Did not read an input String")
    def test_shingle_all(self):
        shingles=self.shing.shingle_all(self.file_path, self.SHINGLE_SIZE)
        while True:
            if len(shingles) == 0:
                break
            elif not len(shingles.pop()) == self.SHINGLE_SIZE:
                self.assertFalse(1, "Shingle length wrong")
        self.assertTrue(1)
    def test_union(self):
        shingles=self.shing.shingle_all(self.file_path, self.SHINGLE_SIZE)
        list=[shingles, shingles, shingles]
        union=self.min_hasher.union_all(list)
        self.assertTrue(len(union)==len(shingles))
    def test_matrix(self):
        matrix=self.min_hasher.make_boolean_matrix([set("a"), set("ab"), set("abc")])
        sums = []
        for i in range(3):
            sum = 0
            for j in range(3):
                sum += matrix[i][j]
            sums.append(sum)
        self.assertTrue(sums[0]==1 and sums[1]==2 and sums[2]==3, "not correct amount of ones in boolean matrix")
    def test_signature_matrix(self):
        shingles_one=self.shing.shingle_all(self.file_path, self.SHINGLE_SIZE)
        shingling_two=self.shing.shingle_all(self.file_path2, self.SHINGLE_SIZE)
        shingling_three=self.shing.shingle_all(self.file_path2, self.SHINGLE_SIZE)
        shingles=[shingles_one, shingling_two, shingling_three]
        matrix=self.min_hasher.make_boolean_matrix(shingles)

        print self.min_hasher.min_hash(shingles)
    def test_swap(self):
        list=[1,2,3,4,5]
        self.min_hasher.swap(list, 0, 4)
        self.assertTrue(list[0]==5, "Incorrect value of index 0 after swap")
    def test_shuffle(self):
        list=[1,2,3,4,5]
        sum=0
        for i in range(1000):
            self.min_hasher.shuffle(list)
            if list[0]==5:
                sum+=1
        self.assertTrue(150<sum and 250>sum, "Shuffling not approx. equally distributed")
    def test_order_list(self):
        my_list=order.ListOrder()
        my_list.append(1)
        my_list.append(2)
        my_list.used_indices(1)
        self.assertTrue(my_list.highest_used_index == 1, "List extension not working")
if __name__ == '__main__':
    unittest.main()