class Node:

    def __init__(self, key=-1, pos=None, tag=-1, weight=-1, info=None):
        self.__key = key
        self.__pos = pos
        self.__tag = tag
        self.__weight = weight
        self.__info = info

    def copy(self, other):
        self.__key = other.__key
        self.__pos = other.__pos
        self.__tag = other.__tag
        self.__weight = other.__weight
        self.__info = other.__info

    def set_weight(self, weight: float):
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def set_tag(self, tag: float):
        self.__tag = tag

    def get_tag(self):
        return self.__tag

    def set_info(self, info: str):
        self.__info = info

    def get_info(self):
        return self.__info

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Node):
            return self.__key == other.__key and self.__weight == other.__weight and self.__pos == other.__pos and \
                   self.__info == other.__info and self.__tag == other.__tag
        return False

    def compare_to(self, other):
        if isinstance(other, Node):
            if self.__weight > other.__weight:
                return 1
            elif self.__weight == other.__weight:
                return 0
            else:
                return -1

    def __str__(self):
        return 'Key: {self.__key}, Tag: {self.__tag}, Weight: {self.__weight}, Pos: {self.__pos}, Info: {self.__info}'\
            .format(self=self)