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

    raise Exception("Doszliśmy do miejsca w któ©ym znaleść się nie powinniśmy")
