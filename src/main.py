import os
import random

from game.state import CheckersState
from helpers.clearConsole import clearConsole
from helpers.gameHeader import gameHeader
from helpers.getInt import getInt

# stan początkowy
from helpers.horizontalConcat import horizontalConcat
from helpers.stringBuilder import StringBuilder

state = CheckersState()

logBuffer = StringBuilder()

while not state.isWon():
    clearConsole()
    gameHeader()

    availableMoves = state.getAvailableMoves()
    nextMove = None

    # Ruch gracza
    if state.isWhiteMove():
        gameBuffer = state.boardString()
        movesBuffer = StringBuilder()

        movesBuffer.append("Dostępne ruchy: ").newLine()
        for i in range(len(availableMoves)):
            movesBuffer.append(i + 1).append(': ').append(availableMoves[i]).newLine()

        print(horizontalConcat(horizontalConcat(gameBuffer, str(movesBuffer), '  |  '), str(logBuffer), '  |  '))

        while True:
            choice = getInt('Wybierz ruch: ') - 1
            if 0 <= choice < len(availableMoves):
                nextMove = availableMoves[choice]
                break

        logBuffer.append('Biały:  ')

    # Ruch komputera
    if state.isBlackMove():
        # komputer wybiera losowy ruch
        # i tu jest miejsce gdzie robisz magie
        choice = random.randrange(0, len(availableMoves))
        nextMove = availableMoves[choice]

        logBuffer.append('Czarny: ')

    state = CheckersState(nextMove)

    # log gry

    logBuffer.append(nextMove).newLine()
