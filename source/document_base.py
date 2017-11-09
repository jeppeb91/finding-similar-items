import os
import sys
import shingling, min_hashing, hashing
import threading
import math
class DocumentBase:
    documents=[]
    documents_completion_order=[]
    shingle_sets=[]
    number_of_permutations=0
    shingle_size=0
    lock=None
    treshold=0.05
    def __init__(self, path_to_directory, shing_size, number_of_perms, treshold):
        self.shingle_size=shing_size
        self.number_of_permutations=number_of_perms
        self.treshold=treshold
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
    def lsh(self, path_to_document):
        shing=shingling.Shingling(self)
        min_hasher=min_hashing.MinHashing(self.number_of_permutations)
        my_shingles=shing.shingle_all(path_to_document, self.shingle_size)
        bool_matrix=min_hasher.make_boolean_matrix(self.shingle_sets)
        sign_matrix=min_hasher.find_signature_matrix(bool_matrix, self.number_of_permutations)
        hasher=hashing.Hasher(sign_matrix, int(math.sqrt(self.number_of_permutations))/2)
        hasher.hash_matrix()
        candidates=self.find_candidates(hasher.buckets, hasher)
        filtered_candidates=self.compare_candidates(candidates)
        return self.get_resulting_files(filtered_candidates, candidates)
    def get_resulting_files(self, filtered_candidates, candidates):
        result=[]
        for i in range(len(filtered_candidates)):
            if filtered_candidates[i]>=0:
                similar_item=(self.documents_completion_order[candidates[i]], filtered_candidates[i])
                result.append(similar_item)
        return result
    def find_candidates(self, buckets, hasher):
        candidate_set=set()
        for bucket in hasher.buckets_of_my_document:
            current=hasher.buckets.get(bucket)
            members= current.members
            for member in members:
                candidate_set.add(member)
        return list(candidate_set)
    def compare_candidates(self, candidates):
        my_document_index=len(self.shingle_sets)-1
        my_shingles=self.shingle_sets[my_document_index]
        result=[]
        candidates.remove(my_document_index)
        for i in range(len(candidates)):
            result.append(self.jaccard_similarity(my_shingles, self.shingle_sets[candidates[i]]))
        for i in range(len(result)):
            if result[i]<self.treshold:
                result[i]=-1
        return result
    def jaccard_similarity(self, x, y):
        intersection=x.intersection(y)
        union=x.union(y)
        jaccard_similarity=float(float(len(intersection))/float(len(union)))
        return jaccard_similarity