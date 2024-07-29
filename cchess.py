import pygame
import time
import const
import pieces
import computer
import AI_search as search


class Button:
    def __init__(self, screen, msg, left, top):
        """
        :param screen: CChess GUI
        :param msg: text show in button
        :param left:
        :param top:
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = 150, 50
        self.button_color = (72, 61, 139)
        self.text_color = (255, 255, 255)

        # Setting font size
        pygame.font.init()
        self.font = pygame.font.SysFont('Courier', 20)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.left = left
        self.top = top

        self.deal_msg(msg)

    def deal_msg(self, msg):
        """
        :param msg: Text going to be rendered
        :return:
        """
        # Render text to img
        self.msg_img = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center

    def draw_button(self):
        self.screen.blit(self.msg_img, (self.left, self.top))

    def is_click(self):
        """
        Listening to mouse click, get pos
        :return:
        """
        point_x, point_y = pygame.mouse.get_pos()
        x = self.left
        y = self.top
        w, h = self.msg_img.get_size()

        in_x = x < point_x < x + w
        in_y = y < point_y < y + h
        return in_x and in_y


class MainGame:
    history = []

    # Store 20 last walks
    operation_logs = []
    max_logs = 20

    # Set board grid
    window = None
    Start_X = const.Start_X
    Start_Y = const.Start_Y
    Line_Span = const.Line_Span
    Max_X = Start_X + 8 * Line_Span
    Max_Y = Start_Y + 9 * Line_Span
    from_x = 0
    from_y = 0
    to_x = 0
    to_y = 0
    clickx = -1
    clicky = -1

    # Set computer player
    ai_search = search.ai_search()
    player1Color = const.player1Color
    player2Color = const.player2Color
    Putdownflag = player1Color
    piecesSelected = None

    # Initialize buttons with None type
    button_go = None
    button_undo = None
    button_easy = None
    button_medium = None
    button_hard = None
    difficulty = 1
    piecesList = []
    game_message = ""
    game_over = False
    possible_moves = []

    def start_game(self):
        """
        Initialize game, contains GUI and pieces statues
        :return:
        """
        MainGame.window = pygame.display.set_mode([const.SCREEN_WIDTH, const.SCREEN_HEIGHT])
        pygame.display.set_caption("CChess")

        MainGame.button_go = Button(MainGame.window, "Restart", const.SCREEN_WIDTH - 100, 300)
        MainGame.button_undo = Button(MainGame.window, "Cancel", const.SCREEN_WIDTH - 100, 250)
        MainGame.button_easy = Button(MainGame.window, "Level 1", const.SCREEN_WIDTH - 100, 100)
        MainGame.button_medium = Button(MainGame.window, "Level 2", const.SCREEN_WIDTH - 100, 150)
        MainGame.button_hard = Button(MainGame.window, "Level 3", const.SCREEN_WIDTH - 100, 200)

        self.piecesInit()

        while True:
            time.sleep(0.1)
            self.show_all()
            self.Computerplay()
            self.getEvent()

    def show_all(self):
        """
        Print all pieces on Board
        :return:
        """
        background_img = pygame.image.load(const.bg).convert()
        scale = 1.08
        MainGame.background_image = pygame.transform.scale(background_img,
                                                           (const.CHECKBOARD_WIDTH * scale,
                                                            const.CHECKBOARD_HEIGHT * scale))
        MainGame.window.fill(const.BG_COLOR)
        MainGame.window.blit(MainGame.background_image,
                             (const.SCREEN_WIDTH * 0.005, const.SCREEN_HEIGHT * 0.01))
        MainGame.button_go.draw_button()
        MainGame.button_undo.draw_button()
        MainGame.button_easy.draw_button()
        MainGame.button_medium.draw_button()
        MainGame.button_hard.draw_button()
        self.display_logs()
        self.piecesDisplay()
        self.VictoryOrDefeat()
        self.display_message()
        self.draw_possible_moves()
        pygame.display.update()
        pygame.display.flip()

    def piecesInit(self):
        """
        Set pieces in position
        :return:
        """
        MainGame.piecesList.clear()
        MainGame.piecesList.append(pieces.Chariot(MainGame.player2Color, 0, 0))
        MainGame.piecesList.append(pieces.Chariot(MainGame.player2Color, 8, 0))
        MainGame.piecesList.append(pieces.Elephant(MainGame.player2Color, 2, 0))
        MainGame.piecesList.append(pieces.Elephant(MainGame.player2Color, 6, 0))
        MainGame.piecesList.append(pieces.King(MainGame.player2Color, 4, 0))
        MainGame.piecesList.append(pieces.Horse(MainGame.player2Color, 1, 0))
        MainGame.piecesList.append(pieces.Horse(MainGame.player2Color, 7, 0))
        MainGame.piecesList.append(pieces.Cannons(MainGame.player2Color, 1, 2))
        MainGame.piecesList.append(pieces.Cannons(MainGame.player2Color, 7, 2))
        MainGame.piecesList.append(pieces.Advisor(MainGame.player2Color, 3, 0))
        MainGame.piecesList.append(pieces.Advisor(MainGame.player2Color, 5, 0))
        MainGame.piecesList.append(pieces.Pawns(MainGame.player2Color, 0, 3))
        MainGame.piecesList.append(pieces.Pawns(MainGame.player2Color, 2, 3))
        MainGame.piecesList.append(pieces.Pawns(MainGame.player2Color, 4, 3))
        MainGame.piecesList.append(pieces.Pawns(MainGame.player2Color, 6, 3))
        MainGame.piecesList.append(pieces.Pawns(MainGame.player2Color, 8, 3))

        MainGame.piecesList.append(pieces.Chariot(MainGame.player1Color, 0, 9))
        MainGame.piecesList.append(pieces.Chariot(MainGame.player1Color, 8, 9))
        MainGame.piecesList.append(pieces.Elephant(MainGame.player1Color, 2, 9))
        MainGame.piecesList.append(pieces.Elephant(MainGame.player1Color, 6, 9))
        MainGame.piecesList.append(pieces.King(MainGame.player1Color, 4, 9))
        MainGame.piecesList.append(pieces.Horse(MainGame.player1Color, 1, 9))
        MainGame.piecesList.append(pieces.Horse(MainGame.player1Color, 7, 9))
        MainGame.piecesList.append(pieces.Cannons(MainGame.player1Color, 1, 7))
        MainGame.piecesList.append(pieces.Cannons(MainGame.player1Color, 7, 7))
        MainGame.piecesList.append(pieces.Advisor(MainGame.player1Color, 3, 9))
        MainGame.piecesList.append(pieces.Advisor(MainGame.player1Color, 5, 9))
        MainGame.piecesList.append(pieces.Pawns(MainGame.player1Color, 0, 6))
        MainGame.piecesList.append(pieces.Pawns(MainGame.player1Color, 2, 6))
        MainGame.piecesList.append(pieces.Pawns(MainGame.player1Color, 4, 6))
        MainGame.piecesList.append(pieces.Pawns(MainGame.player1Color, 6, 6))
        MainGame.piecesList.append(pieces.Pawns(MainGame.player1Color, 8, 6))
        self.operation_logs.clear()
        self.game_over = False

    def piecesDisplay(self):
        for item in MainGame.piecesList:
            item.displaypieces(MainGame.window)

    def getEvent(self):
        """
        Get event from PyGame
        :return:
        """
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                self.endGame()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                mouse_x = pos[0]
                mouse_y = pos[1]
                # Align click to grid
                if (MainGame.Start_X - MainGame.Line_Span / 2 < mouse_x < MainGame.Max_X + MainGame.Line_Span / 2) and (
                        MainGame.Start_Y - MainGame.Line_Span / 2 < mouse_y < MainGame.Max_Y + MainGame.Line_Span / 2):
                    if MainGame.Putdownflag != MainGame.player1Color:
                        return

                    click_x = round((mouse_x - MainGame.Start_X) / MainGame.Line_Span)
                    click_y = round((mouse_y - MainGame.Start_Y) / MainGame.Line_Span)
                    click_mod_x = (mouse_x - MainGame.Start_X) % MainGame.Line_Span
                    click_mod_y = (mouse_y - MainGame.Start_Y) % MainGame.Line_Span
                    if abs(click_mod_x - MainGame.Line_Span / 2) >= 5 and abs(
                            click_mod_y - MainGame.Line_Span / 2) >= 5:
                        self.from_x = MainGame.clickx
                        self.from_y = MainGame.clicky
                        self.to_x = click_x
                        self.to_y = click_y
                        MainGame.clickx = click_x
                        MainGame.clicky = click_y
                        # Check whether checked
                        self.check_check(MainGame.player1Color)
                        self.PutdownPieces(MainGame.player1Color, click_x, click_y)

                        return True

                if MainGame.button_undo.is_click():
                    self.undoMove()

                if MainGame.button_go.is_click():
                    # Signal control
                    self.game_over = False
                    MainGame.Putdownflag = const.player1Color
                    # Reset board state
                    self.piecesInit()
                    self.ai_search = search.ai_search()

                if MainGame.button_easy.is_click():
                    self.set_message("Set difficulty: level 1")
                    MainGame.ai_search.set_difficulty(1)

                elif MainGame.button_medium.is_click():
                    self.set_message("Set difficulty: level 2")
                    MainGame.ai_search.set_difficulty(2)

                elif MainGame.button_hard.is_click():
                    self.set_message("Set difficulty: level 3")
                    MainGame.ai_search.set_difficulty(3)

    def set_message(self, message):
        self.game_message = message

    def display_message(self):
        if self.game_message:
            font = pygame.font.SysFont('Courier', 20)
            message_surface = font.render(self.game_message, True, const.RED)
            MainGame.window.blit(message_surface, (const.SCREEN_WIDTH - 300, 600))

    def undoMove(self):
        """
        Cancel current move and go backward
        :return:
        """
        MainGame.piecesList.clear()
        for pie in MainGame.history:
            MainGame.piecesList.append(pie.clone())
        self.ai_search.last_step()

    def PutdownPieces(self, t, x, y):
        MainGame.history.clear()
        for pie in MainGame.piecesList:
            MainGame.history.append(pie.clone())

        selectfilter = list(
            filter(lambda cm: cm.x == x and cm.y == y and cm.player == MainGame.player1Color, MainGame.piecesList))
        if len(selectfilter):
            MainGame.piecesSelected = selectfilter[0]
            self.highlight_moves(MainGame.piecesSelected)
            return

        if MainGame.piecesSelected:
            arr = pieces.listPiecestoArr(MainGame.piecesList)
            if MainGame.piecesSelected.canmove(arr, x, y):
                self.PiecesMove(MainGame.piecesSelected, x, y)
                MainGame.Putdownflag = MainGame.player2Color
            else:
                self.log_operation(f"{str(type(MainGame.piecesSelected)).split('.')[1][:-2]} can't move to {x},{y}",
                                   const.RED)
                self.log_operation(f"This move is illegal!", const.RED)
        else:
            fi = filter(lambda p: p.x == x and p.y == y, MainGame.piecesList)
            listfi = list(fi)
            if len(listfi) != 0:
                MainGame.piecesSelected = listfi[0]
                self.highlight_moves(MainGame.piecesSelected)

    def PiecesMove(self, pieces, x, y):
        capture = None
        for item in MainGame.piecesList:
            if item.x == x and item.y == y:
                MainGame.piecesList.remove(item)
                capture = str(type(item)).split('.')[1][:-2]
        pieces.x = x
        pieces.y = y
        if pieces.player == 1:
            color = const.RED
        else:
            color = const.BLACK
        if capture:
            self.log_operation(f"{str(type(pieces)).split('.')[1][:-2]} move to {str(x)},{str(y)}",
                               color)
            self.log_operation(f"Capture {capture}", color)
        else:
            self.log_operation(f"{str(type(pieces)).split('.')[1][:-2]} move to {str(x)},{str(y)}", color)

        if self.check_check(MainGame.player2Color):
            self.log_operation("You need AI to respond!", const.RED)
        if self.check_check(MainGame.player1Color):
            self.log_operation("AI wants You to respond!", const.BLACK)
        return True

    def Computerplay(self):
        if MainGame.Putdownflag == MainGame.player2Color:
            # self.ai_search.alpha_beta(self.ai_search.max_depth, const.min_val, const.max_val)
            computermove = computer.getPlayInfo(MainGame.piecesList, self.from_x, self.from_y, self.to_x, self.to_y,
                                                self.ai_search, max_depth=self.ai_search.max_depth)
            if computermove is None:
                return
            piecemove = None
            for item in MainGame.piecesList:
                if item.x == computermove[0] and item.y == computermove[1]:
                    piecemove = item
            self.PiecesMove(piecemove, computermove[2], computermove[3])
            MainGame.Putdownflag = MainGame.player1Color

    def log_operation(self, message, color):
        MainGame.operation_logs.append((message, color))
        if len(MainGame.operation_logs) > MainGame.max_logs:
            MainGame.operation_logs.pop(0)

    def display_logs(self):
        pygame.font.init()
        log_font = pygame.font.SysFont('Courier', 14)
        log_y = const.SCREEN_HEIGHT - (MainGame.max_logs * 30)
        for log, color in MainGame.operation_logs:
            log_surface = log_font.render(log, True, color)
            MainGame.window.blit(log_surface, (const.SCREEN_WIDTH - 300, log_y))
            log_y += 18

    def VictoryOrDefeat(self):
        if self.game_over:
            return

        result = [MainGame.player1Color, MainGame.player2Color]
        for item in MainGame.piecesList:
            if isinstance(item, pieces.King):
                if item.player == MainGame.player1Color:
                    result.remove(MainGame.player1Color)
                if item.player == MainGame.player2Color:
                    result.remove(MainGame.player2Color)

        if len(result) == 0:
            return
        if result[0] == MainGame.player1Color:
            self.set_message("Lost in last game")
            self.log_operation("Failed", const.TEXT_COLOR)
        else:
            self.set_message("Won last game")
            self.log_operation("Victory", const.TEXT_COLOR)

        MainGame.Putdownflag = const.overColor
        self.game_over = True

    def highlight_moves(self, piece):
        arr = pieces.listPiecestoArr(MainGame.piecesList)
        self.possible_moves = [(x, y) for x in range(9) for y in range(10) if piece.canmove(arr, x, y)]

    def draw_possible_moves(self):
        for (x, y) in self.possible_moves:
            center_x = const.Start_X + x * const.Line_Span
            center_y = const.Start_Y + y * const.Line_Span
            pygame.draw.circle(MainGame.window, const.RED, (center_x, center_y), 5)

    def check_check(self, player):
        if player == 1:
            color = const.RED
        else:
            color = const.BLACK
        arr = pieces.listPiecestoArr(MainGame.piecesList)
        king = None
        for piece in MainGame.piecesList:
            if isinstance(piece, pieces.King) and piece.player == player:
                king = piece
                break

        if not king:
            return False

        for piece in MainGame.piecesList:
            if piece.player != player and piece.canmove(arr, king.x, king.y):
                if player == 1:
                    self.log_operation(f"Your king is captured", color)
                if player == 2:
                    self.log_operation(f"AI king is captured", color)

                return True
        return False

    def endGame(self):
        exit()


if __name__ == '__main__':
    MainGame().start_game()
