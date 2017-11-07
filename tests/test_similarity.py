import unittest
import sys
import os
from os.path import dirname, abspath
parent_dir=dirname(dirname(abspath(__file__)))
sys.path.append(parent_dir)

from source import shingling, min_hashing, document_base
class TestSimilarity(unittest.TestCase):
    file_path=os.path.join(parent_dir, "source\\resources\\dataset-CalheirosMoroRita-2017.csv")
    file_path2=os.path.join(parent_dir, "source\\min_hashing.py")
    #shing=shingling.Shingling()
    #min_hasher=min_hashing.MinHashing()
    SHINGLE_SIZE=3
    NUMBER_OF_PERMUTATIONS=100
    def test_compare(self):
        my_path_to_dir=os.path.join(parent_dir, "source", "resources")
        my_docs=document_base.DocumentBase(my_path_to_dir, self.SHINGLE_SIZE, self.NUMBER_OF_PERMUTATIONS)
        result_list=my_docs.extend_and_compare(self.file_path)
        true_jaccards=self.get_exact_jaccard(my_docs)
        print true_jaccards
        print result_list
        for i in range(len(result_list)-1):
            lower=true_jaccards[i]*0.2
            upper=true_jaccards[i]*5
            if(result_list[i]<lower or result_list[i]>upper):
                self.assertFalse(1, "At least one result outside of accepted interval")
            else:
                self.assertTrue(1)
    def get_exact_jaccard(self, my_docs):
        true_value_list=[]
        for i in range(len(my_docs.shingle_sets)-1):
            intersection=my_docs.shingle_sets[i].intersection(my_docs.shingle_sets[len(my_docs.shingle_sets)-1])
            union=my_docs.shingle_sets[i].union(my_docs.shingle_sets[len(my_docs.shingle_sets)-1])
            jaccard_similarity=float(float(len(intersection))/float(len(union)))
            true_value_list.append(jaccard_similarity)
        return true_value_list
if __name__ == '__main__':
    unittest.main()
