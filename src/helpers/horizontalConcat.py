import os


def horizontalConcat(first, second, spacer):
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
