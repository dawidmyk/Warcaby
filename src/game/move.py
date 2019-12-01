import math
from game.type import CheckerType


class CheckerMove:
    """
    Funkcja reprezentuje proste
    """
    def __init__(self, state, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._state1 = state
        self._state2 = None
        self._pawn = state.getPawnType(x1, y1)

        # określenie czy zachodzi bicie pionka, poprzez iteracje po polach pomiędzy początkiem a końcem
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

    def getStateFrom(self):
        return self._state1

    def getStateTo(self):
        """
        Stan następny nie jest generowany dopóki o niego nie poprosimy
        :return:
        """
        if self._state2 is None:
            from game.state import CheckersState
            self._state2 = CheckersState(self)

        return self._state2

    def getFromX(self) -> int:
        return self._x1

    def getFromY(self) -> int:
        return self._y1

    def getToX(self) -> int:
        return self._x2

    def getToY(self) -> int:
        return self._y2

    def getPawnType(self):
        return self._pawn

    def hasBeat(self):
        return self._xBeat != -1 and self._yBeat != -1

    def executeOnBoard(self, board):
        """
        Przestawienie pionka na planszy i usunięcie pionka zbitego
        :param board:
        :return:
        """
        pawn2move = self._pawn
        board[self._x1][self._y1] = None
        board[self._x2][self._y2] = pawn2move
        if self.hasBeat():
            board[self._xBeat][self._yBeat] = None

    def getMovePoints(self):
        """
        Część ładnego rysowania przejść
        :return:
        """
        return [[self._x1, self._y1], [self._x2, self._y2]]

    def __str__(self):

        m = str(self._x1 + 1) + ',' + str(self._y1 + 1) + \
            ' -> ' + \
            str(self._x2 + 1) + ',' + str(self._y2 + 1)

        return m

    def __repr__(self):
        return "CheckerMove(" + self.__str__() + ")"
