class CheckerMove:
    def __init__(self, state, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._state = state

    def getFromX(self):
        return self._x1

    def getFromY(self):
        return self._y1

    def getToX(self):
        return self._x2

    def getToY(self):
        return self._y2

    def __str__(self):
        return f"{str(self._x1 + 1)},{str(self._y1 + 1)} => {str(self._x2 + 1)},{str(self._y2 + 1)}"

    def __repr__(self):
        return f"CheckerMove({self.__str__()})"
