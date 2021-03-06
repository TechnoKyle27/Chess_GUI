# -*- coding: utf-8 -*-

from termcolor import cprint
import os
from pieces import *
from board import Board
from GUI import *

class Game:
    columnKey = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    rowKey = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}

    def __init__(self):
        self.boardy = Board()
        self.run = True
        self.turn = 0

    def translate(self, a1notation):
        try:
            x = self.columnKey[a1notation[0].lower()]
            y = self.rowKey[a1notation[1]]
            return x, y
        except BaseException:
            raise MoveException(a1notation)

    def isMoveValid(self, start, end):
        if start == end:
            raise MoveException(
                None, "The move you entered makes it so your piece does not move.")
        piece = self.boardy.board[start[1]][start[0]]
        piece.isMoveValid(self.boardy.board, start, end)

    # General game rules
    def movePiece(self, start, end):
        self.isMoveValid(start, end)
        (sx, sy) = start
        (ex, ey) = end
        self.boardy.movePiece(start, end)
        # when pawn makes it to other side and becomes queen
        if isinstance(self.boardy.board[ey][ex], Pawn):
            if (ey == 7 and self.boardy.board[ey][ex].side == -1) or (
                    ey == 0 and self.boardy.board[ey][ex].side == 1):
                self.boardy.board[ey][ex] = Queen(
                    self.boardy.board[ey][ex].side)

    def main_gui(self):
        place_board(self.boardy)
        pygame.display.update()
        error = ""
        clicks = 0
        while self.run:
            if error != "":
                cprint("Invalid move! " + error, "red")
                print("")
                error = ""

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONUP:
                    if clicks == 0:
                        start = pygame.mouse.get_pos()
                        sx = start[0]//111
                        sy = start[1]//111
                        if not isinstance(self.boardy.board[sy][sx], EmptySpace):
                            clicks += 1
                            draw_cursor(sx, sy)
                            pygame.display.update()
                    else:
                        end = pygame.mouse.get_pos()
                        ex = end[0] // 111
                        ey = end[1] // 111
                        clicks = 0
                        try:
                            if (self.boardy.board[sy][sx].side == 1 and self.turn % 2 == 0) or (self.boardy.board[sy][sx].side == -1 and self.turn % 2 == 1):
                                self.movePiece((sx, sy), (ex, ey))
                                self.turn += 1
                                if self.boardy.checkWin():
                                    # print(self.boardy.checkWin())
                                    show_text(self.boardy.checkWin())
                                    pygame.display.update()
                                    break
                        except MoveException as e:
                            error = "Your move goes against chess rules. " + e.message
                        place_board(self.boardy)
                        pygame.display.update()
        pygame.quit()
    def main(self):
        error = ""

        while self.run:
            os.system("clear")
            if error != "":
                cprint("Invalid move! " + error, "red")
                print("")
                error = ""

            # print("")
            self.boardy.printBoard()

            start = input("\nAt what X and Y is the piece you want to move?: ")
            # game.get_piece(start)

            destination = input(
                "At what X and Y do you want the piece to be?: ")

            try:
                (sx, sy) = self.translate(start)
                (ex, ey) = self.translate(destination)
            except Exception as e:
                error = "Invalid input notation."
                error = str(e)
                # os.system("clear")
                continue

            try:
                self.movePiece((sx, sy), (ex, ey))
            except MoveException as e:
                error = "Your move goes against chess rules. " + e.message
            # os.system("clear")
        pygame.quit()


if __name__ == "__main__":
    gamey = Game()
    gamey.main_gui()
    # import unittest
    # from test import *
    # unittest.main()
