import os
import random
import time

from game.state import CheckersState
from helpers.clearConsole import clearConsole
from helpers.gameHeader import gameHeader
from helpers.getInt import getInt

# stan początkowy
from helpers.horizontalConcat import horizontalConcat
from helpers.stringBuilder import StringBuilder

state = CheckersState()

logBuffer = StringBuilder()

while not state.isEnd():
    # clearConsole()
    gameHeader()

    availableMoves = state.getAvailableMoves()
    nextMove = None

    gameBuffer = state.boardString()
    movesBuffer = StringBuilder()

    if state.isWhiteMove():
        movesBuffer.append("Ruch gracza")
    if state.isBlackMove():
        movesBuffer.append("Ruch kompuera")

    movesBuffer.newLine().newLine().append("Dostępne ruchy: ").newLine()
    for i in range(len(availableMoves)):
        movesBuffer.append(i + 1).append(': ').append(availableMoves[i]).newLine()

    print(horizontalConcat(horizontalConcat(gameBuffer, str(movesBuffer), '  |  '), str(logBuffer), '  |  '))

    if state.isWhiteMove():
        while True:
            choice = getInt('Wybierz ruch: ') - 1
            if 0 <= choice < len(availableMoves):
                nextMove = availableMoves[choice]
                break

        logBuffer.append('Biały:  ')

    if state.isBlackMove():
        # komputer wybiera losowy ruch
        # i tu jest miejsce gdzie robisz magie
        print("Komputer myśli ...")
        time.sleep(3)

        # jakbyś chciał rozbudować stany to robisz to tak

        choice = random.randrange(0, len(availableMoves))
        nextMove = availableMoves[choice]

        logBuffer.append('Czarny: ')

    state = CheckersState(nextMove)
    logBuffer.append(nextMove).newLine()

endType = state.endType()
