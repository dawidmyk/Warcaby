import math

from game.type import CheckerType


class CheckerMove:
    def __init__(self, state, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._state = state
        self._pawn = state.getPawnType(x1, y1)

        # określenie bicia
        self._xBeat = -1
        self._yBeat = -1
        dx = 1
        if x2 < x1:
            dx = -1
        dy = 1
        if y2 < y1:
            dy = -1
        x = x1 + dx
        y = y1 + dy
        while x != x2 and y != y2:
            if CheckerType.isValid(state.getPawnType(x, y)):
                self._xBeat = x
                self._yBeat = y
                break
            else:
                x = x + dx
                y = y + dy
        print(self._xBeat, self._yBeat)

    def getState(self):
        return self._state

    def getFromX(self) -> int:
        return self._x1

    def getFromY(self) -> int:
        return self._y1

    def getToX(self) -> int:
        return self._x2

    def getToY(self) -> int:
        return self._y2

    def getBeatX(self):
        return self._xBeat

    def getBeatY(self):
        return self._yBeat

    def hasBeat(self):
        return self._xBeat != -1 and self._yBeat != -1

    def hasPromotion(self):
        from game.state import CheckersState
        return (CheckerType.isWhite(self._pawn) and self._x2 == 0) or \
               (CheckerType.isBlack(self._pawn) and self._x2 == CheckersState.SizeX - 1)

    def selfSalary(self):
        return 0

    def sumSalary(self):
        return 0

    def __str__(self):
        m = str(self._x1 + 1) + ',' + str(self._y1 + 1) + ' => ' + str(self._x2 + 1) + ',' + str(self._y2 + 1)

        if self.hasBeat():
            m = m + " B"
        else:
            m = m + "  "

        if self.hasPromotion():
            m = m + " P"
        else:
            m = m + "  "

        return m

    def __repr__(self):
        return "CheckerMove(" + self.__str__() + ")"
