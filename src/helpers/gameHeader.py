import math


def gameHeader():
    title = " Warcaby "

    authorsTitle = "Autorzy:"
    authors = ["Adam Jędrzejowski", "Dawid Mackiewicz"]

    width = 8 * 4 + 1

    print(authorsTitle, end='')
    for author in authors:
        print(' ' + author)
        print(' ' * len(authorsTitle), end='')

    print("")
    half = (width - len(title)) / 2
    char = '═'
    print(char * math.floor(half) + title + char * math.ceil(half))
    print("")
