def getInt(text):
    """
    Pobiera liczbę całkowitą od użytkownika, jeżeli wejście będzie złe, to ponowi próbę
    :param text:
    :return:
    """
    try:
        return int(input(text))
    except:
        return -1
