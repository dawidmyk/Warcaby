from src.game.state import CheckersState
from src.helpers.clearConsole import clearConsole
from src.helpers.gameHeader import gameHeader
from src.helpers.getInt import getInt

# stan początkowy

state = CheckersState()

while not state.isWon():
    clearConsole()
    gameHeader()


    state.printBoard()

    print("")

    print("Dostępne ruchy:")
    availableMoves = state.getAvailableMoves()
    for i in range(len(availableMoves)):
        print(f' {str(i + 1)}: ' + str(availableMoves[i]))

    print("")

    while True:
        choice = getInt('Wybierz ruch:') - 1
        if choice < 0:
            continue

        break
