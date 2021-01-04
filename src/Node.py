class Node:

    def __init__(self, key=-1, pos=None, tag=-1, weight=-1, info=" "):
        self.key = key
        self.pos = pos
        self.tag = tag
        self.weight = weight
        self.info = info

    def copy(self, other):
        self.key = other.key
        self.pos = other.pos
        self.tag = other.tag
        self.weight = other.weight
        self.info = other.info

    def set_weight(self, weight: float):
        self.weight = weight

    def get_weight(self):
        return self.weight

    def set_tag(self, tag: float):
        self.tag = tag

    def get_tag(self):
        return self.tag

    def set_info(self, info: str):
        self.info = info

    def get_info(self):
        return self.info

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Node):
            return self.key == other.key and self.weight == other.weight and self.pos == other.pos and \
                   self.info == other.info and self.tag == other.tag
        return False

    def compare_to(self, other):
        if isinstance(other, Node):
            if self.weight > other.weight:
                return 1
            elif self.weight == other.weight:
                return 0
            else:
                return -1

    def __str__(self):
        return 'Key: {self.key}, Tag: {self.tag}, Weight: {self.weight}, Pos: {self.pos}, Info: {self.info}'.format(
            self=self)

