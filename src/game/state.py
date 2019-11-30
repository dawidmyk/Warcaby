from game.move import CheckerMove
from game.type import CheckerType
from helpers.stringBuilder import StringBuilder


class CheckersState:
    SizeX = 8
    SizeY = 8

    def __init__(self, move=None):
        # alokacja pustej planszy
        self._board = [[None for x in range(self.SizeX)] for y in range(self.SizeY)]
        self._availableMoves = None
        self._sumSalary = 0

        if move == None:
            self._next = CheckerType.whiteNormal()
            self._initStartingBoard()
        else:
            self._insertDataFrom(move)

    def _initStartingBoard(self):
        fillRows = 3

        def fillRow(x, type):
            offset = x % 2
            for y in range(0 + offset, self.SizeX + offset, 2):
                self._setPawn(x, y, type)

        for x in range(0, fillRows):
            fillRow(x, CheckerType.blackNormal())

        for x in range(self.SizeX - fillRows, self.SizeX):
            fillRow(x, CheckerType.whiteNormal())

    def _insertDataFrom(self, move):
        lastState = move.getState()

        if move.hasBeat():
            if lastState.isWhiteMove():
                self._next = CheckerType.whiteNormal()
            if lastState.isBlackMove():
                self._next = CheckerType.blackNormal()
        else:
            if lastState.isWhiteMove():
                self._next = CheckerType.blackNormal()
            if lastState.isBlackMove():
                self._next = CheckerType.whiteNormal()

        # przepisanie planszy
        for x in range(self.SizeX):
            for y in range(self.SizeY):
                self._board[x][y] = lastState._board[x][y]

        # przestawianie pionka
        pawn2move = lastState.getPawnType(move.getFromX(), move.getFromY())
        self._setPawn(move.getFromX(), move.getFromY(), None)
        if move.hasPromotion():
            pawn2move = CheckerType.upgrade(pawn2move)
        self._setPawn(move.getToX(), move.getToY(), pawn2move)
        if move.hasBeat():
            self._setPawn(move.getBeatX(), move.getBeatY(), None)

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
        for x in range(self.SizeX):
            rowSpacer1 = rowSpacer1 + hLine + str(x + 1) + hLine + cross
        rowSpacer2 = cross + (hLine * 3 + cross) * self.SizeX

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
        self._availableMoves = []
        for x in range(self.SizeX):
            for y in range(self.SizeY):
                pawn = self._board[x][y]

                def moveNormalForward(dx, dy):
                    x2, y2 = x + dx, y + dy

                    # jeżeli pozycje nie jest na planysz to koniec
                    if not self.isPositionValid(x2, y2):
                        return

                    if self.isFieldEmpty(x2, y2):
                        # czyli nie niema na tej pozycji
                        self._availableMoves.append(
                            CheckerMove(self, x, y, x2, y2))
                        return

                    pawn2 = self.getPawnType(x2, y2)

                    # w przypadku kiedy jest z tej samej drużyny to nie możemy się ruszyć
                    if CheckerType.isSameTeam(pawn, pawn2):
                        return

                    # czyli nie jest z tej samej drużyny, więc sprawdzamy czy miejsce za nim jest wolne
                    x3, y3 = x2 + dx, y2 + dy
                    if not self.isPositionValid(x3, y3):
                        return
                    if self.isFieldEmpty(x3, y3):
                        self._availableMoves.append(
                            CheckerMove(self, x, y, x3, y3))

                def moveNormalBackward(dx, dy):
                    x2, y2 = x + dx, y + dy

                    # jeżeli pozycje nie jest na planysz to koniec
                    if not self.isPositionValid(x2, y2):
                        return

                    if self.isFieldEmpty(x2, y2):
                        return

                    pawn2 = self.getPawnType(x2, y2)

                    # w przypadku kiedy jest z tej samej drużyny to nie możemy się ruszyć
                    if CheckerType.isSameTeam(pawn, pawn2):
                        return

                    # czyli nie jest z tej samej drużyny, więc sprawdzamy czy miejsce za nim jest wolne
                    x3, y3 = x2 + dx, y2 + dy
                    if not self.isPositionValid(x3, y3):
                        return
                    if self.isFieldEmpty(x3, y3):
                        self._availableMoves.append(
                            CheckerMove(self, x, y, x3, y3))

                def moveSpecial(dx, dy):
                    x2 = x + dx
                    y2 = y + dy
                    wasPawn = False

                    while self.isPositionValid(x2, y2):

                        if self.isFieldEmpty(x2, y2):
                            # czyli nie niema na tej pozycji
                            self._availableMoves.append(
                                CheckerMove(self, x, y, x2, y2))
                        else:
                            pawn2 = self.getPawnType(x2, y2)

                            if CheckerType.isSameTeam(pawn, pawn2):
                                return

                            if wasPawn:
                                return

                            wasPawn = True

                        x2 = x2 + dx
                        y2 = y2 + dy

                if self.isBlackMove():

                    if pawn == CheckerType.blackNormal():
                        ## czarne idą w dół(+)
                        moveNormalForward(+1, +1)
                        moveNormalForward(+1, -1)
                        moveNormalBackward(-1, +1)
                        moveNormalBackward(-1, -1)

                    if pawn == CheckerType.blackSpecial():
                        moveSpecial(+1, +1)
                        moveSpecial(+1, -1)
                        moveSpecial(-1, +1)
                        moveSpecial(-1, -1)

                if self.isWhiteMove():

                    if pawn == CheckerType.whiteNormal():
                        ## czarne idą w góre(-)
                        moveNormalForward(-1, +1)
                        moveNormalForward(-1, -1)
                        moveNormalBackward(+1, +1)
                        moveNormalBackward(+1, -1)

                    if pawn == CheckerType.whiteSpecial():
                        moveSpecial(+1, +1)
                        moveSpecial(+1, -1)
                        moveSpecial(-1, +1)
                        moveSpecial(-1, -1)

    def getAvailableMoves(self):
        if self._availableMoves is None:
            self._generateAvailableMoves()

        return self._availableMoves

    def isWhiteMove(self):
        return CheckerType.isWhite(self._next)

    def isBlackMove(self):
        return CheckerType.isBlack(self._next)

    def _setPawn(self, x, y, pawn):
        self._board[x][y] = pawn

    def isPositionValid(self, x, y):
        return 0 <= x < self.SizeX and 0 <= y < self.SizeY

    def getPawnType(self, x, y):
        return self._board[x][y]

    def isFieldEmpty(self, x, y):
        return not CheckerType.isValid(self.getPawnType(x, y))

    def isEnd(self):
        wasBlack = True
        wasWhite = True

        for row in self._board:
            for pawn in row:
                if CheckerType.isBlack(pawn):
                    wasBlack = True
                if CheckerType.isWhite(pawn):
                    wasWhite = True

        return wasWhite != wasBlack

    def endType(self):
        pass

    def sumSalary(self):
        return self._sumSalary
