class CheckerType:

    @staticmethod
    def blackNormal():
        return 'b'

    @staticmethod
    def whiteNormal():
        return 'w'

    @staticmethod
    def blackSpecial():
        return 'B'

    @staticmethod
    def whiteSpecial():
        return 'W'

    @staticmethod
    def isBlack(pawn):
        return pawn == CheckerType.blackNormal() or pawn == CheckerType.blackSpecial()

    @staticmethod
    def isWhite(pawn):
        return pawn == CheckerType.whiteNormal() or pawn == CheckerType.whiteSpecial()

    @staticmethod
    def isValid(pawn):
        return CheckerType.isBlack(pawn) or CheckerType.isWhite(pawn)

    @staticmethod
    def isSameTeam(pawn1, pawn2):
        return (CheckerType.isBlack(pawn1) and CheckerType.isBlack(pawn2)) or \
               (CheckerType.isWhite(pawn1) and CheckerType.isWhite(pawn2))

    @staticmethod
    def upgrade(pawn):
        if pawn == CheckerType.whiteNormal():
            return CheckerType.whiteSpecial()
        if pawn == CheckerType.blackNormal():
            return CheckerType.blackSpecial()
        return pawn
