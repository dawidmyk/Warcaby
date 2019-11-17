from src.game.move import CheckerMove
from src.game.type import CheckerType


class CheckersState:
    _sizeX = 8
    _sizeY = 8
    _next = None
    _availableMoves = []

    def __init__(self, move=None):
        # alokacja pustej planszy
        self._board = [[None for x in range(self._sizeX)] for y in range(self._sizeY)]

        self._board[3][4] = 'B'
        self._board[4][3] = 'w'
        self._board[6][7] = 'W'
        self._board[7][6] = 'b'

        self._generateAvailableMoves()

    def printBoard(self):
        # https://www.utf8-chartable.de/unicode-utf8-table.pl?start=9472&unicodeinhtml=dec
        vLine = '║'
        hLine = '═'
        cross = '╬'
        pawnNormalWhite = ' O '
        pawnSpecialWhite = '<O>'
        pawnNormalBlack = ' X '
        pawnSpecialBlack = '<X>'
        empty = '   '

        rowSpacer1 = cross
        for x in range(self._sizeX):
            rowSpacer1 = rowSpacer1 + hLine + str(x + 1) + hLine + cross
        rowSpacer2 = cross + (hLine * 3 + cross) * self._sizeX

        print(rowSpacer1)
        y = 0
        for row in self._board:
            line = str(y + 1)

            for cell in row:
                content = empty

                if cell == CheckerType.blackNormal():
                    content = pawnNormalBlack
                if cell == CheckerType.whiteNormal():
                    content = pawnNormalWhite
                if cell == CheckerType.blackSpecial():
                    content = pawnSpecialBlack
                if cell == CheckerType.whiteSpecial():
                    content = pawnSpecialWhite

                line = line + content + vLine

            print(line)
            print(rowSpacer2)
            y = y + 1

    def _generateAvailableMoves(self):
        for x in range(self._sizeX):
            for y in range(self._sizeY):
                pawn = self._board[x][y]

                def moveNormal(dx, dy):
                    x2, y2 = x + dx, y + dy

                    # jeżeli pozycje nie jest na planysz to koniec
                    if not self.isPositionValid(x2, x2):
                        return

                    pawn2 = self.getPawnType(x2, y2)

                    if self.isEmpty(x2, y2):
                        # czyli nie niema na tej pozycji
                        self._availableMoves.append(
                            CheckerMove(self, x, y, x2, y2))
                        return

                    # w przypadku kiedy jest z tej samej drużyny to nie możemy się ruszyć
                    if CheckerType.isSameTeam(pawn, pawn2):
                        return

                    # czyli nie jest z tej samej drużyny, więc sprawdzamy czy miejsce za nim jest wolne
                    x3, y3 = x2 + dx, y2 + dy
                    if not self.isPositionValid(x3, y3):
                        return
                    if self.isEmpty(x3, y3):
                        self._availableMoves.append(
                            CheckerMove(self, x, y, x3, y3))

                if pawn == CheckerType.blackNormal():
                    ## czarne idą w dół(+)
                    moveNormal(+1, +1)
                    moveNormal(+1, -1)

                if pawn == CheckerType.whiteNormal():
                    ## czarne idą w góre(-)
                    moveNormal(-1, +1)
                    moveNormal(-1, -1)

                if pawn == CheckerType.blackSpecial():
                    pass

                if pawn == CheckerType.whiteSpecial():
                    pass

    def getAvailableMoves(self):
        return self._availableMoves

    def movePawn(self, x1, y1, x2, y2):
        return self

    def isWhiteMove(self):
        return CheckerType.isWhite(self._next)

    def isBlackMove(self):
        return CheckerType.isBlack(self._next)

    def _setPawn(self, x, y, pawn):
        pass

    def isPositionValid(self, x, y):
        return 0 <= x < self._sizeX and 0 <= y < self._sizeY

    def getPawnType(self, x, y):
        return self._board[x][y]

    def isEmpty(self, x, y):
        return not CheckerType.isValid(self.getPawnType(x, y))

    def isWon(self):
        wasBlack = True
        wasWhite = True

        for row in self._board:
            for pawn in row:
                if CheckerType.isBlack(pawn):
                    wasBlack = True
                if CheckerType.isWhite(pawn):
                    wasWhite = True

        return wasWhite != wasBlack


