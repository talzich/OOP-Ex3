class Node:

    # Constructor
    def __init__(self, key=-1, pos=None, tag=-1, weight=-1, info=None):
        self.__key = key
        self.__pos = pos
        self.__tag = tag
        self.__weight = weight
        self.__info = info
        self.__in = dict()
        self.__out = dict()

    # Copy constructor
    def copy(self, other):
        self.__key = other.__key
        self.__pos = other.__pos
        self.__tag = other.__tag
        self.__weight = other.__weight
        self.__info = other.__info

    # **********SETTERS & Getters********** #
    def get_key(self):
        return self.__key

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

    def get_pos(self):
        return self.__pos

    def set_pos(self, pos: tuple):
        if not isinstance(pos, tuple):
            raise TypeError("Position must be of type tuple")
        self.__pos = pos

    def get_out(self):
        if self.__out is not None:
            return self.__out
        else:
            return None

    def get_in(self):
        if self.__in is not None:
            return self.__in

    # **********SETTERS & Getters********** #

    # Utility - To be used when calling DiGraph's add_edge
    def add_out(self, key, edge):
        self.__out[key] = edge

    def add_in(self, key, edge):
        self.__in[key] = edge

    # Utility - To be used when calling DiGraph's remove_edge
    def remove_out(self, key):
        self.__out.pop(key)

    def remove_in(self, key):
        self.__in.pop(key)

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

    def __repr__(self):
        return f'Key: {self.__key}, Tag: {self.__tag}, Weight: {self.__weight}, Pos: {self.__pos}, Info: {self.__info}'

    def to_json(self):
        my_x = str(self.__pos[0])
        my_y = str(self.__pos[1])
        my_pos = my_x + "," + my_y
        my_dict = {"pos": my_pos, "id": self.__key}
        return my_dict
