import os
from game.move import CheckerMove
from game.type import CheckerType
from helpers.stringBuilder import StringBuilder


class CheckersState:
    _sizeX = 8
    _sizeY = 8

    def __init__(self, move = None):
        # alokacja pustej planszy
        self._board = [[None for x in range(self._sizeX)] for y in range(self._sizeY)]
        self._availableMoves = []

        if move == None:
            self._next = CheckerType.whiteNormal()
            self._initStartingBoard()
        else:
            self._insertDataFrom(move)

        self._generateAvailableMoves()

    def _initStartingBoard(self):
        fillRows = 3

        def fillRow(x, type):
            offset = x % 2
            for y in range(0 + offset, self._sizeX + offset, 2):
                self._setPawn(x, y, type)

        for x in range(0, fillRows):
            fillRow(x, CheckerType.blackNormal())

        for x in range(self._sizeX - fillRows, self._sizeX):
            fillRow(x, CheckerType.whiteNormal())

    def _insertDataFrom(self, move):
        lastState = move.getState()

        if lastState.isWhiteMove():
            self._next = CheckerType.blackNormal()
        if lastState.isBlackMove():
            self._next = CheckerType.whiteNormal()

        # przepisanie planszy
        for x in range(self._sizeX):
            for y in range(self._sizeY):
                self._board[x][y] = lastState._board[x][y]

        # przestawianie pionka
        pawn2move = lastState.getPawnType(move.getFromX(), move.getFromY())
        self._setPawn(move.getFromX(), move.getFromY(), None)
        self._setPawn(move.getToX(), move.getToY(), pawn2move)

        # i usuwanie jak bedzie potrzeba
        if move.hasRemove():
            self._setPawn(move.getRemoveX(), move.getRemoveY(), None)

    def boardString(self):
        # https://www.utf8-chartable.de/unicode-utf8-table.pl?start=9472&unicodeinhtml=dec
        vLine = '║'
        hLine = '═'
        cross = '╬'
        pawnNormalWhite = ' ▣ '
        pawnSpecialWhite = '<▣>'
        pawnNormalBlack = ' □ '
        pawnSpecialBlack = '<□>'
        emptyCell = '   '

        buffer = StringBuilder()

        rowSpacer1 = cross
        for x in range(self._sizeX):
            rowSpacer1 = rowSpacer1 + hLine + str(x + 1) + hLine + cross
        rowSpacer2 = cross + (hLine * 3 + cross) * self._sizeX

        buffer.append(rowSpacer1).newLine()
        y = 0
        for row in self._board:
            line = StringBuilder()
            line.append(y + 1)

            for cell in row:

                if cell == CheckerType.blackNormal():
                    line.append(pawnNormalBlack)
                elif cell == CheckerType.whiteNormal():
                    line.append(pawnNormalWhite)
                elif cell == CheckerType.blackSpecial():
                    line.append(pawnSpecialBlack)
                elif cell == CheckerType.whiteSpecial():
                    line.append(pawnSpecialWhite)
                else:
                    line.append(emptyCell)

                line.append(vLine)

            buffer.append(line).newLine()
            buffer.append(rowSpacer2).newLine()
            y = y + 1

        return str(buffer)

    def _generateAvailableMoves(self):
        for x in range(self._sizeX):
            for y in range(self._sizeY):
                pawn = self._board[x][y]

                def moveNormal(dx, dy):
                    x2, y2 = x + dx, y + dy

                    # jeżeli pozycje nie jest na planysz to koniec
                    if not self.isPositionValid(x2, y2):
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
                            CheckerMove(self, x, y, x3, y3, x2, y2))

                if self.isBlackMove():

                    if pawn == CheckerType.blackNormal():
                        ## czarne idą w dół(+)
                        moveNormal(+1, +1)
                        moveNormal(+1, -1)

                    if pawn == CheckerType.blackSpecial():
                        pass

                if self.isWhiteMove():

                    if pawn == CheckerType.whiteNormal():
                        ## czarne idą w góre(-)
                        moveNormal(-1, +1)
                        moveNormal(-1, -1)

                    if pawn == CheckerType.whiteSpecial():
                        pass

    def getAvailableMoves(self):
        return self._availableMoves

    def isWhiteMove(self):
        return CheckerType.isWhite(self._next)

    def isBlackMove(self):
        return CheckerType.isBlack(self._next)

    def _setPawn(self, x, y, pawn):
        self._board[x][y] = pawn

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
