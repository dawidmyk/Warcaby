import time
import random


def ai_magic_stuff(moves):
    startTime = int(round(time.time() * 1000))

    try:
        nextMove = move_min_max(moves, 5)
    except:
        # w przpadku błędu algorytmu, które się nie zdażają, wybiera losowy ruch
        choice = random.randrange(0, len(moves))
        nextMove = moves[choice]

    # magia zawsze trwa 3 sekundy(lub dłużej)
    endTime = int(round(time.time() * 1000))
    algTime = (endTime - startTime) / 1000
    if algTime < 3:
        time.sleep(3 - algTime)

    return nextMove


def move_min_max(moves, deep):
    # moves = state.getAvailableMoves()
    nextStates = list(map(lambda move: move.getStateTo(), moves))
    salaries = list(map(lambda state: min_max(state, deep - 1), nextStates))

    maxSalary = max(salaries)
    i = salaries.index(maxSalary)

    return moves[i]


def min_max(state, deep):
    if state.isEnd() or deep <= 0:
        return state.getSalary()

    moves = state.getAvailableMoves()
    nextStates = list(map(lambda move: move.getStateTo(), moves))
    nextSalaries = list(map(lambda state: min_max(state, deep - 1), nextStates))

    if state.isWhiteMove():  # maksymalizacja
        return max(nextSalaries)

    if state.isBlackMove():  # minimalizacja
        return min(nextSalaries)

    raise Exception("Doszliśmy do miejsca w którym znaleść się nie powinniśmy")
