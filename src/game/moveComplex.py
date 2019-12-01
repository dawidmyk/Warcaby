from game.move import CheckerMove


class CheckerMoveComplex:
    """
    Klasa odpowiada za ruchy wielokrotne, składające się z dwóch innych ruchów
    """
    def __init__(self, first, second):
        self._first = first
        self._second = second

        if (  # zabezpieczenie przed dodanie dwóch ruchów, które nie powinny być łączone
                first.getToX() != second.getFromX() or
                first.getToY() != second.getFromY() or
                first.getPawnType() != second.getPawnType()
        ):
            raise Exception("cant combine these moves")

    def getStateFrom(self):
        return self._first.getStateFrom()

    def getStateTo(self):
        return self._second.getStateTo()

    def getFromX(self) -> int:
        return self._first.getFromX()

    def getFromY(self) -> int:
        return self._first.getFromY()

    def getToX(self) -> int:
        return self._second.getToX()

    def getToY(self) -> int:
        return self._second.getToY()

    def hasBeat(self):
        return self._first.hasBeat() or self._second.hasBeat()

    def getPawnType(self):
        return self._first.getPawnType()

    def executeOnBoard(self, board):
        self._first.executeOnBoard(board)
        self._second.executeOnBoard(board)

    def getMovePoints(self):
        first = self._first.getMovePoints()
        second = self._second.getMovePoints()
        del second[0]

        return first + second

    def __str__(self):
        points = self.getMovePoints()

        # wiem wygląda obrzydliwie, ale działa
        points = list(map(lambda point: ",".join(list(map(lambda x: str(x + 1), point))), points))

        return " -> ".join(points)

    def __repr__(self):
        return "CheckerMoveComplex(" + self.__str__() + ")"
