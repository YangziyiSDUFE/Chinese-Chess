import pygame
import const


class Pieces:
    def __init__(self, player, x, y):
        """
        base class for every pieces
        :param player:
        :param x:
        :param y:
        """
        self.imagskey = self.getImagekey()

        self.image = const.pieces_images[self.imagskey]
        self.x = x
        self.y = y
        self.player = player
        self.rect = self.image.get_rect()
        self.rect.left = const.Start_X + x * const.Line_Span - self.image.get_rect().width / 2
        self.rect.top = const.Start_Y + y * const.Line_Span - self.image.get_rect().height / 2

    def displaypieces(self, screen):
        """
        display
        :param screen:
        :return:
        """
        self.rect.left = (const.Start_X + self.x * const.Line_Span - self.image.get_rect().width / 2)
        self.rect.top = const.Start_Y + self.y * const.Line_Span - self.image.get_rect().height / 2
        screen.blit(self.image, self.rect);

    def canmove(self, arr, moveto_x, moveto_y):
        """
        check if can move to (moveto_x, moveto_y)
        :param arr:
        :param moveto_x:
        :param moveto_y:
        :return:
        """
        pass

    def getImagekey(self):
        return None

    def getScoreWeight(self, listpieces):
        return None


class Chariot(Pieces):
    def __init__(self, player, x, y):
        self.player = player
        super().__init__(player, x, y)

    def getImagekey(self):
        if self.player == const.player1Color:
            return "r_chariot"
        else:
            return "b_chariot"

    def canmove(self, arr, moveto_x, moveto_y):
        """
        check if can move
        :param arr:
        :param moveto_x:
        :param moveto_y:
        :return:
        """
        if self.x == moveto_x and self.y == moveto_y:
            return False
        if arr[moveto_x][moveto_y] == self.player:
            return False
        if self.x == moveto_x:
            step = -1 if self.y > moveto_y else 1
            for i in range(self.y + step, moveto_y, step):
                if arr[self.x][i] != 0:
                    return False
            return True

        if self.y == moveto_y:
            step = -1 if self.x > moveto_x else 1
            for i in range(self.x + step, moveto_x, step):
                if arr[i][self.y] != 0:
                    return False
            return True

    def getScoreWeight(self, listpieces):
        score = 11
        return score

    def clone(self):
        new_piece = Chariot(self.player, self.x, self.y)
        return new_piece


class Horse(Pieces):
    def __init__(self, player, x, y):
        self.player = player
        super().__init__(player, x, y)

    def getImagekey(self):
        if self.player == const.player1Color:
            return "r_horse"
        else:
            return "b_horse"

    def canmove(self, arr, moveto_x, moveto_y):
        if self.x == moveto_x and self.y == moveto_y:
            return False
        if arr[moveto_x][moveto_y] == self.player:
            return False
        move_x = moveto_x - self.x
        move_y = moveto_y - self.y
        if abs(move_x) == 1 and abs(move_y) == 2:
            step = 1 if move_y > 0 else -1
            if arr[self.x][self.y + step] == 0:
                return True
        if abs(move_x) == 2 and abs(move_y) == 1:
            step = 1 if move_x > 0 else -1
            if arr[self.x + step][self.y] == 0:
                return True

    def getScoreWeight(self, listpieces):
        score = 5
        return score

    def clone(self):
        new_piece = Horse(self.player, self.x, self.y)
        return new_piece


class Elephant(Pieces):
    def __init__(self, player, x, y):
        self.player = player
        super().__init__(player, x, y)

    def getImagekey(self):
        if self.player == const.player1Color:
            return "r_elephant"
        else:
            return "b_elephant"

    def canmove(self, arr, moveto_x, moveto_y):
        if self.x == moveto_x and self.y == moveto_y:
            return False
        if arr[moveto_x][moveto_y] == self.player:
            return False
        if self.y <= 4 and moveto_y >= 5 or self.y >= 5 and moveto_y <= 4:
            return False
        move_x = moveto_x - self.x
        move_y = moveto_y - self.y
        if abs(move_x) == 2 and abs(move_y) == 2:
            step_x = 1 if move_x > 0 else -1
            step_y = 1 if move_y > 0 else -1
            if arr[self.x + step_x][self.y + step_y] == 0:
                return True

    def getScoreWeight(self, listpieces):
        score = 2
        return score

    def clone(self):
        new_piece = Elephant(self.player, self.x, self.y)
        return new_piece


class Advisor(Pieces):

    def __init__(self, player, x, y):
        self.player = player
        super().__init__(player, x, y)

    def getImagekey(self):
        if self.player == const.player1Color:
            return "r_advisor"
        else:
            return "b_advisor"

    def canmove(self, arr, moveto_x, moveto_y):
        if self.x == moveto_x and self.y == moveto_y:
            return False
        if arr[moveto_x][moveto_y] == self.player:
            return False
        if moveto_x < 3 or moveto_x > 5:
            return False
        if 2 < moveto_y < 7:
            return False
        move_x = moveto_x - self.x
        move_y = moveto_y - self.y
        if abs(move_x) == 1 and abs(move_y) == 1:
            return True

    def getScoreWeight(self, listpieces):
        score = 2
        return score

    def clone(self):
        new_piece = Advisor(self.player, self.x, self.y)
        return new_piece


class King(Pieces):
    def __init__(self, player, x, y):
        self.player = player
        super().__init__(player, x, y)

    def getImagekey(self):
        if self.player == const.player1Color:
            return "r_king"
        else:
            return "b_king"

    def canmove(self, arr, moveto_x, moveto_y):
        if self.x == moveto_x and self.y == moveto_y:
            return False
        if arr[moveto_x][moveto_y] == self.player:
            return False
        if moveto_x < 3 or moveto_x > 5:
            return False
        if moveto_y > 2 and moveto_y < 7:
            return False
        move_x = moveto_x - self.x
        move_y = moveto_y - self.y
        if abs(move_x) + abs(move_y) == 1:
            return True

    def getScoreWeight(self, listpieces):
        score = 150
        return score

    def clone(self):
        new_piece = King(self.player, self.x, self.y)
        return new_piece


class Cannons(Pieces):
    def __init__(self, player, x, y):
        self.player = player
        super().__init__(player, x, y)

    def getImagekey(self):
        if self.player == const.player1Color:
            return "r_cannon"
        else:
            return "b_cannon"

    def canmove(self, arr, moveto_x, moveto_y):
        if self.x == moveto_x and self.y == moveto_y:
            return False
        if arr[moveto_x][moveto_y] == self.player:
            return False
        overflag = False
        if self.x == moveto_x:
            step = -1 if self.y > moveto_y else 1
            for i in range(self.y + step, moveto_y, step):
                if arr[self.x][i] != 0:
                    if overflag:
                        return False
                    else:
                        overflag = True

            if overflag and arr[moveto_x][moveto_y] == 0:
                return False
            if not overflag and arr[self.x][moveto_y] != 0:
                return False

            return True

        if self.y == moveto_y:
            step = -1 if self.x > moveto_x else 1
            for i in range(self.x + step, moveto_x, step):
                if arr[i][self.y] != 0:
                    if overflag:
                        return False
                    else:
                        overflag = True

            if overflag and arr[moveto_x][moveto_y] == 0:
                return False
            if not overflag and arr[moveto_x][self.y] != 0:
                return False
            return True

    def getScoreWeight(self, listpieces):
        score = 6
        return score

    def clone(self):
        new_piece = Cannons(self.player, self.x, self.y)
        return new_piece


class Pawns(Pieces):
    def __init__(self, player, x, y):
        self.player = player
        super().__init__(player, x, y)

    def getImagekey(self):
        if self.player == const.player1Color:
            return "r_pawn"
        else:
            return "b_pawn"

    def canmove(self, arr, moveto_x, moveto_y):
        if self.x == moveto_x and self.y == moveto_y:
            return False
        if arr[moveto_x][moveto_y] == self.player:
            return False
        move_x = moveto_x - self.x
        move_y = moveto_y - self.y

        if self.player == const.player1Color:
            if self.y > 4 and move_x != 0:
                return False
            if move_y > 0:
                return False
        elif self.player == const.player2Color:
            if self.y <= 4 and move_x != 0:
                return False
            if move_y < 0:
                return False

        if abs(move_x) + abs(move_y) == 1:
            return True

    def getScoreWeight(self, listpieces):
        score = 2
        return score

    def clone(self):
        new_piece = Pawns(self.player, self.x, self.y)
        return new_piece


def listPiecestoArr(piecesList):
    arr = [[0 for i in range(10)] for j in range(9)]
    for i in range(0, 9):
        for j in range(0, 10):
            if len(list(filter(lambda cm: cm.x == i and cm.y == j and cm.player == const.player1Color,
                               piecesList))):
                arr[i][j] = const.player1Color
            elif len(list(filter(lambda cm: cm.x == i and cm.y == j and cm.player == const.player2Color,
                                 piecesList))):
                arr[i][j] = const.player2Color

    return arr
