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
        self._isContinuousBeating = False

        if move == None:
            self._next = CheckerType.whiteNormal()
            self._initStartingBoard()
        else:
            self._insertDataFromMove(move)

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

    def _insertDataFromMove(self, move):
        lastState = move.getStateFrom()

        # przepisanie planszy
        for x in range(self.SizeX):
            for y in range(self.SizeY):
                self._setPawn(x, y, lastState.getPawnType(x, y))

        # przestawianie pionka
        move.executeOnBoard(self._board)

        # ustalenie następnego gracza
        if move.hasBeat():

            if lastState.isWhiteMove():
                self._next = CheckerType.whiteNormal()
            if lastState.isBlackMove():
                self._next = CheckerType.blackNormal()

            # tu jest troche triki, ponieważ możemy kontynłować, tylko wtedy gdy zbijemy i zbijamy dalej
            # dlatego generujemy ruchy i sprawdzmy czy możemy bić dalej, ale tym konkretnym pionkiem
            self._generateAvailableMoves()

            def filerOurPawnMoves(newMove):
                return newMove.getFromX() == move.getToX() and \
                       newMove.getFromY() == move.getToY()

            moves = list(filter(filerOurPawnMoves, self._availableMoves))
            if len(moves) > 0 and moves[0].hasBeat():
                # jest możliwośc kontynuacji bicia tym pionem
                self._availableMoves = moves
                self._isContinuousBeating = True
            else:
                if lastState.isWhiteMove():
                    self._next = CheckerType.blackNormal()
                if lastState.isBlackMove():
                    self._next = CheckerType.whiteNormal()
                self._generateAvailableMoves()

        else:
            if lastState.isWhiteMove():
                self._next = CheckerType.blackNormal()
            if lastState.isBlackMove():
                self._next = CheckerType.whiteNormal()

        # rozwinięcie bić do ruchów złożonych
        def extendBeatMove(move):
            from game.moveComplex import CheckerMoveComplex

            # jeżeli brak bicia to zwróć bicie
            if not move.hasBeat():
                return [move]

            nextState = move.getStateTo()
            if nextState.isContinuousBeating():
                newMoves = []
                for nextMove in nextState.getAvailableMoves():
                    newMoves.append(CheckerMoveComplex(move, nextMove))

                return newMoves
            else:
                return [move]

        self._availableMoves = list(map(extendBeatMove, self.getAvailableMoves()))
        # wyprostowanie listy, ponieważ teraz mamy liste list
        # https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
        self._availableMoves = [item for sublist in self._availableMoves for item in sublist]

        # upgrade do damki
        if not self._isContinuousBeating and (
                (CheckerType.isWhite(move.getPawnType()) and move.getToX() == 0) or
                (CheckerType.isBlack(move.getPawnType()) and move.getToX() == CheckersState.SizeX - 1)):
            self._setPawn(move.getToX(), move.getToY(), CheckerType.upgrade(move.getPawnType()))

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
        from game.move import CheckerMove

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

        # wymuszenie bicia

        for move in self._availableMoves:
            if move.hasBeat():
                self._availableMoves = list(filter(lambda move: move.hasBeat(), self._availableMoves))
                break

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

    def isContinuousBeating(self):
        return self._isContinuousBeating

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
