class ListOrder(list):
    highest_used_index = 0
    def __init__(self):
        super(ListOrder, self).__init__()
    def append(self, element):
        super(ListOrder, self).append(element)
        if not self.highest_used_index == 0:
            self.highest_used_index += 1
    def used_indices(self, index):
        if index>self.highest_used_index:
            self.highest_used_index=index
