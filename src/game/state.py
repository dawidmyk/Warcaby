from game.type import CheckerType
from helpers.stringBuilder import StringBuilder


class CheckersState:
    """
    Klasa stanu gry
    """

    # Jak widać wielkość planszy można zmienić
    SizeX = 8
    SizeY = 8

    def __init__(self, move=None):
        # alokacja pustej planszy
        self._board = [[None for x in range(self.SizeX)] for y in range(self.SizeY)]

        # wartość none oznacza, że nie została przeprowadzona analiza możliwych ruchów
        self._availableMoves = None
        self._isContinuousBeating = False

        # tworzenie stanu początkowego lub następnego
        if move == None:
            self._next = CheckerType.whiteNormal()
            self._initStartingBoard()
        else:
            self._insertDataFromMove(move)

    def _initStartingBoard(self):
        """
        Naprzemienne wypełnienie początkowej planszy
        :return:
        """
        fillRows = 3

        def fillRow(x, type):
            offset = x % 2
            for y in range(0 + offset, self.SizeX + offset, 2):
                self._setPawn(x, y, type)

        for x in range(0, fillRows):  # wypełnienie czarnych
            fillRow(x, CheckerType.blackNormal())

        for x in range(self.SizeX - fillRows, self.SizeX):  # wypełnienie białych
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

            # tu jest trochę triki, ponieważ możemy kontynuować, tylko wtedy gdy zbijemy i zbijamy dalej
            # dlatego generujemy ruchy i sprawdzamy czy możemy bić dalej, ale tym konkretnym pionkiem

            if lastState.isWhiteMove():
                self._next = CheckerType.whiteNormal()
            if lastState.isBlackMove():
                self._next = CheckerType.blackNormal()
            self._generateAvailableMoves()

            # znajdujemy tylko ruchy naszego ruszonego pionka
            def filerOurPawnMoves(newMove):
                return newMove.getFromX() == move.getToX() and \
                       newMove.getFromY() == move.getToY()

            moves = list(filter(filerOurPawnMoves, self._availableMoves))

            if len(moves) > 0 and moves[0].hasBeat():
                # jest możliwość kontynuacji bicia tym pionem
                self._availableMoves = moves
                self._isContinuousBeating = True
            else:
                # jak jej niema
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
                # newMoves = [move]
                newMoves = []
                for nextMove in nextState.getAvailableMoves():
                    newMoves.append(CheckerMoveComplex(move, nextMove))

                return newMoves
            else:
                return [move]

        self._availableMoves = list(map(extendBeatMove, self.getAvailableMoves()))
        # wyprostowanie listy, ponieważ teraz mamy listę list
        # https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
        self._availableMoves = [item for sublist in self._availableMoves for item in sublist]

        # upgrade do damki
        # ponieważ w czasie bicia gdy przeskoczymy do końca, ale się nie zatrzymamy to nie stajemy się damką
        if not self._isContinuousBeating and (
                (CheckerType.isWhite(move.getPawnType()) and move.getToX() == 0) or
                (CheckerType.isBlack(move.getPawnType()) and move.getToX() == CheckersState.SizeX - 1)):
            self._setPawn(move.getToX(), move.getToY(), CheckerType.upgrade(move.getPawnType()))

    def boardString(self):
        """
        Funkcja odpowiada za generowanie ładnej planszy z pionkami
        :return:
        """

        # https://www.utf8-chartable.de/unicode-utf8-table.pl?start=9472&unicodeinhtml=dec
        vLine = '║'
        hLine = '═'
        cross = '╬'
        pawnNormalWhite = ' ▣ '
        pawnSpecialWhite = '<▣>'
        pawnNormalBlack = ' □ '
        pawnSpecialBlack = '<□>'
        emptyCell = '   '

        # zestaw alternatywny
        # vLine = '|'
        # hLine = '-'
        # cross = '+'
        # pawnNormalWhite = ' W '
        # pawnSpecialWhite = ' W*'
        # pawnNormalBlack = ' B '
        # pawnSpecialBlack = ' B*'
        # emptyCell = '   '

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

        # iteracja po całej planszy
        for x in range(self.SizeX):
            for y in range(self.SizeY):
                pawn = self.getPawnType(x, y)

                # w poniższych funkcjach dx i dy reprezentują kierunek ruchu pionka/damki

                def moveNormalForward(dx, dy):
                    """
                    Obsługa ruchu do przodu i bicia pionka
                    """
                    x2, y2 = x + dx, y + dy

                    # jeżeli pozycje nie jest na planszy to koniec
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
                    """
                    Obsługa ruchu bicia do tyłu pionka
                    """
                    x2, y2 = x + dx, y + dy

                    # jeżeli pozycje nie jest na planszy to koniec
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
                    """
                    Obsługa ruchu i bicia damki
                    """
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
                                # natrafiono na pionek tej samej drużyny
                                return

                            if wasPawn:
                                # był pionek, który nie był z tej samej drużyny
                                self._availableMoves.append(  # sprawdzić poprawność w długiej grze
                                    CheckerMove(self, x, y, x2, y2))
                                return

                            wasPawn = True

                        x2 = x2 + dx
                        y2 = y2 + dy

                if self.isBlackMove():

                    if pawn == CheckerType.blackNormal():
                        # czarne idą w dół(+)
                        moveNormalForward(+1, +1)
                        moveNormalForward(+1, -1)
                        moveNormalBackward(-1, +1)
                        moveNormalBackward(-1, -1)

                    if pawn == CheckerType.blackSpecial():
                        # a damki gdziekolwiek
                        moveSpecial(+1, +1)
                        moveSpecial(+1, -1)
                        moveSpecial(-1, +1)
                        moveSpecial(-1, -1)

                if self.isWhiteMove():

                    if pawn == CheckerType.whiteNormal():
                        # białe idą w górę(-)
                        moveNormalForward(-1, +1)
                        moveNormalForward(-1, -1)
                        moveNormalBackward(+1, +1)
                        moveNormalBackward(+1, -1)

                    if pawn == CheckerType.whiteSpecial():
                        # a damki gdziekolwiek
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

    def getSalary(self):
        specialFactor = 1.6

        blackNormalCount = 0
        blackSpecialCount = 0
        whiteNormalCount = 0
        whiteSpecialCount = 0
        others = 0

        for x in range(self.SizeX):
            for y in range(self.SizeY):
                pawn = self.getPawnType(x, y)

                if pawn == CheckerType.blackNormal():
                    blackNormalCount += 1

                if pawn == CheckerType.blackSpecial():
                    blackSpecialCount += 1

                if pawn == CheckerType.whiteNormal():
                    whiteNormalCount += 1

                if pawn == CheckerType.whiteSpecial():
                    whiteSpecialCount += 1

        if self.isEnd():
            endType = self.endType()
            if endType == "whiteWon":
                others += -1000
            if endType == "blackWon":
                others += +1000

        return (
                (blackNormalCount + blackSpecialCount * specialFactor) -
                (whiteNormalCount + whiteSpecialCount * specialFactor) +
                others
        )

    def isEnd(self):
        return self.endType() is not None

    def endType(self):
        """
        Określenie typu stanu terminalnego, bo są dwa
        :return:
        """

        wasBlack = True
        wasWhite = True

        for row in self._board:
            for pawn in row:
                if CheckerType.isBlack(pawn):
                    wasBlack = True
                if CheckerType.isWhite(pawn):
                    wasWhite = True

        if wasWhite != wasBlack:
            if wasWhite:
                return "whiteWon"
            return "blackWon"

        return None