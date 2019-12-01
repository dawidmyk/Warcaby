#!/usr/bin/python

from game.ai import ai_magic_stuff
from game.state import CheckersState
from helpers.clearConsole import clearConsole
from helpers.gameHeader import gameHeader
from helpers.getInt import getInt

from helpers.horizontalConcat import horizontalConcat
from helpers.stringBuilder import StringBuilder

# stan początkowy
state = CheckersState()

# zapis historia ruchów
logBuffer = StringBuilder()

while not state.isEnd():
    clearConsole()
    gameHeader()

    availableMoves = state.getAvailableMoves()
    nextMove = None

    # tworzenie interfejsu użytkownika

    gameBuffer = state.boardString()
    movesBuffer = StringBuilder()

    if state.isWhiteMove():
        movesBuffer.append("Ruch gracza")
    if state.isBlackMove():
        movesBuffer.append("Ruch komputera")

    movesBuffer.newLine().newLine().append("Dostępne ruchy: ").newLine()
    for i in range(len(availableMoves)):
        movesBuffer.append(i + 1).append(': ').append(availableMoves[i]).newLine()

    print(horizontalConcat(horizontalConcat(gameBuffer, str(movesBuffer), '  |  '), str(logBuffer), '  |  '))

    # wybór sposobu wykonania ruchu, albo gracz, albo komputer

    if state.isWhiteMove():
        while True:
            choice = getInt('Wybierz ruch: ') - 1
            if 0 <= choice < len(availableMoves):
                nextMove = availableMoves[choice]
                break

        logBuffer.append('Biały:  ')

    if state.isBlackMove():
        print("Komputer myśli ...")
        nextMove = ai_magic_stuff(availableMoves)

        logBuffer.append('Czarny: ')

    # wybranie stanu i dodanie go do historii
    state = CheckersState(nextMove)
    logBuffer.append(nextMove).newLine()

# screen zakończenia

endType = state.endType()
endScreen = StringBuilder()
endScreen.newLine().append("     ")
if endType == "blackWon":
    endScreen.append("Czarny wygrał")
elif endType == "whiteWon":
    endScreen.append("Biały wygrał")
else:
    endScreen.append("Taki stan nie powinien się trafić")
endScreen.newLine().newLine()
endScreen.print()