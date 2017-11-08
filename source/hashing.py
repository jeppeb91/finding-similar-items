import l_s_h
import copy, threading
class Hasher:
    matrix=None
    buckets={}
    band_length=0
    highest_column_index=0
    highest_row_index=0
    prime=31
    lock=None
    def __init__(self, matrix, band_length):
        self.matrix=matrix
        self.band_length=band_length
        self.highest_column_index=len(self.matrix)
        self.lock=threading.Lock()
    def hash_matrix(self):
        self.highest_row_index=len(self.matrix[0])
        for i in range(self.highest_row_index):
            thread=threading.Thread(target=self.hash_row(i, self))
            thread.start()
            #self.hash_row(i, self)
    def hash_row(self, row_index, parent):
        bands = self.split_row_to_bands(row_index)
        for i in range(len(bands)):
            hash_value = self.hash_band(bands[i])
            self.update_buckets(hash_value, row_index, parent)
    def update_buckets(self, hash_value, row_index, parent):
        while True:
            try:
                lock=parent.lock.acquire()
                if lock:
                    current = self.buckets.get(hash_value)
                    if current is None:
                        current = l_s_h.Bucket()
                    current.add(row_index)
                    temp={hash_value:current}
                    self.buckets.update(temp)
                else:
                    print "locked"
            finally:
                parent.lock.release()
                break
    def hash_band(self, band):
        sum=0
        for i in range (len(band)):
            sum+=band[i]
        return sum
    def split_row_to_bands(self, row_index):
        bands=[]
        current_amount=0
        current_elements=[]
        for i in range(self.highest_column_index):
            current_elements.append(self.matrix[i][row_index])
            current_amount+=1
            if current_amount == self.band_length:
                current_amount = 0
                bands.append(current_elements)
                current_elements=[]
        if not current_elements == []:
            bands.append(current_elements)
        print bands
        return bands