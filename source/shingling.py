class Shingling:
    parent_document_base=None
    def __init__(self, parent_document_base):
        self.parent_document_base=parent_document_base
    def read_file(self, file_path):
        file=open(file_path, 'r')
        res=file.read()
        file.close()
        return res

    def shingle_all(self, file_path, shingle_size):
        document=self.read_file(file_path)
        counter=0
        shingles=set()
        while counter+shingle_size<len(document):
            shingles.add(document[counter:counter+shingle_size])
            counter=counter+1
        self.update_parent(shingles, file_path)
        #return shingles

    def update_parent(self, shingles, file_path):
        while True:
            try:
                lock=self.parent_document_base.lock.acquire()
                if lock:
                    self.parent_document_base.add_shingles(shingles)
                    self.parent_document_base.documents_completion_order.append(file_path)
            finally:
                self.parent_document_base.lock.release()
                break
