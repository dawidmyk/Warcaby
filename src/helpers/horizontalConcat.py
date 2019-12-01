import os


def horizontalConcat(first, second, spacer):
    """
    Tworzy kolumny tekstowe, łączy dwa wielo-linijkowe teksty w jeden wspólny, mniej więcej tak: "A|B"
    :param first:
    :param second:
    :param spacer:
    :return:
    """
    buffer = ''

    first = first.splitlines()
    firstLen = len(first)
    maxFirst = 0
    for line in first:
        maxFirst = max(len(line), maxFirst)

    second = second.splitlines()
    secondLen = len(second)
    maxSecond = 0
    for line in second:
        maxSecond = max(len(line), maxSecond)

    length = max(firstLen, secondLen)

    for i in range(length):
        left = ''
        right = ''

        if i < firstLen:
            left = first[i]
        if i < secondLen:
            right = second[i]

        left = left + ' ' * (maxFirst - len(left))
        right = right + ' ' * (maxSecond - len(right))

        buffer = buffer + left + spacer + right + os.linesep

    return buffer
