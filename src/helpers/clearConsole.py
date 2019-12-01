import os


def clearConsole():
    """
    Czyszczenie konsoli
    :return:
    """
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
