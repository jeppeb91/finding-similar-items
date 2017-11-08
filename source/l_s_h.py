class Bucket:
    members=None
    def __init__(self):
        self.members=set()
    def add(self, item):
        self.members.add(item)
    def get_members(self):
        return self.members