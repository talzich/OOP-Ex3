class Edge:

    def __init__(self, src=-1, dest=-1, weight=-1.0, tag=-1, info=None):
        self.__src = src
        self.__dest = dest
        self.__weight = weight
        self.__tag = tag
        self.__info = info

    def get_src(self):
        return self.__src

    def get_dest(self):
        return self.__dest

    def get_weight(self):
        return self.__weight

    def get_info(self):
        return self.__info

    def set_src(self, src):
        self.__src = src

    def set_dest(self, dest):
        self.__dest = dest

    def set_weight(self, weight):
        self.__weight = weight

    def set_info(self, info):
        self.__info = info

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Edge):
            return self.__src == other.__src and self.__dest == other.__dest and self.__weight == other.__weight and \
                   self.__tag == other.__tag and self.__info == other.__info
        return False

    def __str__(self):
        return f'Src: {self.__src}, Dest: {self.__dest}, Weight: {self.__weight}, Tag: {self.__tag}, Info: {self.__info}'

    def to_json(self):
        my_dict = {"src": self.__src, "dest": self.__dest, "weight": self.__weight, "tag": self.__tag, "info": self.__info}
        return my_dict


