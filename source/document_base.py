import os
import sys
import shingling, min_hashing
import threading
class DocumentBase:
    documents=[]
    shingle_sets=[]
    number_of_permutations=0
    shingle_size=0
    lock=None
    def __init__(self, path_to_directory, shing_size, number_of_perms):
        self.shingle_size=shing_size
        self.number_of_permutations=number_of_perms
        self.lock=threading.Lock()
        self.load_directory(path_to_directory)
        self.shingle_all_in_directory()
    def load_directory(self, document_directory):
        for (dirpath, dirnames, filenames) in os.walk(document_directory):
            for i in range(len(filenames)):
                filenames[i]=os.path.join(document_directory, filenames[i])
            self.documents.extend(filenames)
    def shingle_all_in_directory(self):
        shing=shingling.Shingling(self)
        for i in range(len(self.documents)):
            # self.shingle_sets.append(shing.shingle_all(self.documents[i], self.shingle_size))
            thread=threading.Thread(target=shing.shingle_all(self.documents[i], self.shingle_size))
            thread.start()
    def extend_and_compare(self, path_to_document):
        shing=shingling.Shingling(self)
        min_hasher=min_hashing.MinHashing(self.number_of_permutations)
        my_shingles=shing.shingle_all(path_to_document, self.shingle_size)
        return min_hasher.min_hash(self.shingle_sets)
    def add_shingles(self, shingles):
        self.shingle_sets.append(shingles)


