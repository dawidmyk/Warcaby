import os


class StringBuilder:
    def __init__(self):
        self._body = ''

    def clear(self):
        """

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

        :return StringBuilder:
        """
        return self.append(os.linesep)

    def __str__(self):
        return self._body

    def __repr__(self):
        return self.__str__()