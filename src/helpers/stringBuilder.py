import os


class StringBuilder:
    """
    Klasa służy jako pomocnik do budowania długich sekwencji tekstu
    """
    def __init__(self):
        self._body = ''

    def clear(self):
        """
        Czyści buffor
        :return StringBuilder:
        """
        self._body = ''
        return self

    def append(self, text):
        """

        :param text:
        :return StringBuilder:
        """
        self._body = self._body + str(text)
        return self

    def newLine(self):
        """
        Dodaje zakończenie lini
        :return StringBuilder:
        """
        return self.append(os.linesep)

    def print(self):
        print(self)

    def __str__(self):
        return self._body

    def __repr__(self):
        return self.__str__()
