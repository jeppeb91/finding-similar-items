import document_base
import os
import sys
def main():
    SHINGLE_SIZE = 5
    NUMBER_OF_PERMUTATIONS = 100
    TRESHOLD=0.05
    print "Enter path to home folder of the documents"
    my_path_to_dir=sys.stdin.readline()
    my_path_to_dir=my_path_to_dir.strip('\n')
    print "enter path to your document"
    file_path=sys.stdin.readline()
    file_path=file_path.strip('\n')
    print file_path
    my_docs=document_base.DocumentBase(my_path_to_dir, SHINGLE_SIZE, NUMBER_OF_PERMUTATIONS, TRESHOLD)
    result_set=my_docs.lsh(file_path)
    print result_set
if __name__ == '__main__':
    main()