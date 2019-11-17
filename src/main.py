import os
import random

from src.game.state import CheckersState
from src.helpers.clearConsole import clearConsole
from src.helpers.gameHeader import gameHeader
from src.helpers.getInt import getInt

# stan początkowy
from src.helpers.horizontalConcat import horizontalConcat

state = CheckersState()

logBuffer = ''

while not state.isWon():
    # clearConsole()
    gameHeader()

    availableMoves = state.getAvailableMoves()
    nextMove = None

    # Ruch gracza
    if state.isWhiteMove():
        gameBuffer = str(state)
        movesBuffer = ''

        movesBuffer = movesBuffer + "Dostępne ruchy: " + os.linesep
        for i in range(len(availableMoves)):
            movesBuffer = movesBuffer + str(i + 1) + ': ' + str(availableMoves[i]) + os.linesep

        print(horizontalConcat(gameBuffer, movesBuffer, '  |  '))

        while True:
            choice = getInt('Wybierz ruch:') - 1
            if 0 <= choice < len(availableMoves):
                nextMove = availableMoves[choice]
                break

    # Ruch komputera
    if state.isBlackMove():
        # komputer wybiera losowy ruch
        # i tu jest miejsce gdzie robisz magie
        choice = random.randrange(0, len(availableMoves))
        nextMove = availableMoves[choice]

    state = CheckersState(nextMove)
