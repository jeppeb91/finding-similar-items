import unittest
import sys
import os
from os.path import dirname, abspath
parent_dir=dirname(dirname(abspath(__file__)))
sys.path.append(parent_dir)

from source import shingling, min_hashing, document_base, hashing
class TestSimilarity(unittest.TestCase):
    file_path=os.path.join(parent_dir, "source\\resources\\dataset-CalheirosMoroRita-2017.csv")
    file_path2=os.path.join(parent_dir, "source\\min_hashing.py")
    #shing=shingling.Shingling()
    #min_hasher=min_hashing.MinHashing()
    SHINGLE_SIZE=2
    NUMBER_OF_PERMUTATIONS=100

    def test_compare(self):
        my_path_to_dir=os.path.join(parent_dir, "source", "resources")
        my_docs=document_base.DocumentBase(my_path_to_dir, self.SHINGLE_SIZE, self.NUMBER_OF_PERMUTATIONS)
        result_set=my_docs.lsh(self.file_path)
        count=0
        print result_set
if __name__ == '__main__':
    unittest.main()
