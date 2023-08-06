import cx_engine

class Position:
    def __init__(self, x, y, z):
        self.__position = cx_engine.Position(x, y, z)

    @property
    def x(self):
        return self.__position.x

    @x.setter
    def x(self, value):
        self.__position.x = value

    @property
    def y(self):
        return self.__position.y

    @y.setter
    def y(self, value):
        self.__position.y = value

    @property
    def z(self):
        return self.__position.z

    @z.setter
    def z(self, value):
        self.__position.z = value

    def __repr__(self):
        return self.__position.__repr__()


class PositionEngine:
    def __init__(self, nb_anchors):
        self.__position_engine = cx_engine.PositionEngine(nb_anchors)

    def get_anchor_positions(self):
        return self.__position_engine.get_anchor_positions()

    def set_anchor_positions(self, anchor_positions):
        self.__position_engine.set_anchor_positions(anchor_positions)

    def compute_tag_position(self, measurements, initial_position):
        return self.__position_engine.compute_tag_position(measurements, initial_position)

    def get_sse(self):
        return self.__position_engine.get_sse()


import cx_debug_engine

class DebugPostionEngine(cx_debug_engine.DebugPostionEngine):
    def __init__(self, nb_anchors):
        super().__init__(nb_anchors)
