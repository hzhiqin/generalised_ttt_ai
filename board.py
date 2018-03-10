"""
representing any random n by n tic tac toe game board
recording all position on the board
"""
import numpy
import sys
import math
import random


class Board:
    """representing a state of the board"""

    MAX = sys.maxsize
    MIN = - sys.maxsize
    WIN = MAX
    LOSE = MIN
    DRAW = 0.2017
    IN_PROGRESS = 1

    def __init__(self, side_num, win_len, search_depth):
        #   link how many pieces to win
        self.win_len = win_len
        self.side_num = side_num
        #   indicate how many moves have taken
        self.last_move = []

        #   a list to store the situation of all the pits
        #   0- no piece, +1- player 1's piece, -1- player 2's piece
        self.panel = numpy.zeros((side_num, side_num), dtype=int)
        #   indicate search depth
        self.search_depth = search_depth
        #   evaluation criteria - format score
        self.criteria_1 = []
        self.criteria_2 = []
        for i in range(1, win_len):
            self.criteria_1.append(10 ** i)
        self.criteria_1.append(sys.maxsize)
        self.criteria_2.append(0)
        for i in range(2, win_len):
            self.criteria_2.append(10 ** (i - 1))
        self.criteria_2.append(sys.maxsize)
        self.current_score = 0
        self.empty = side_num ** 2

    def get_position(self, x, y):
        """check the state of required location on board"""
        if self.panel[x][y] == 0:
            return 0
        elif self.panel[x][y] == 1:
            return 1
        elif self.panel[x][y] == -1:
            return -1
        else:
            pass

    def get_row(self, x):
        """return the row of given coordinate"""
        return self.panel[x].tolist()

    def get_col(self, y):
        """:return the column of given coordinate"""
        return self.panel[:, y].tolist()

    def get_dia(self, x, y):
        """return the diagonal of given coordinate"""
        point_x = x
        point_y = y
        while point_x > 0:
            point_x = point_x - 1
            point_y = point_y - 1
        return self.panel.diagonal(point_x).copy().tolist()

    def get_anti_dia(self, x, y):
        """:return the anti-diagonal of given coordinate"""
        point_x = x
        point_y = y
        transpose = numpy.fliplr(self.panel)
        while point_x < self.side_num - 1:
            point_x = point_x + 1
            point_y = point_y - 1
        return transpose.diagonal(-point_y).copy().tolist()

    def set_piece(self, x, y, player):
        """put one player's piece in location x, y
           player is -1 or +1
        """
        self.panel[x][y] = player
        self.last_move = [x, y]
        self.empty = self.empty - 1

    def _count_list_score(self, line, player):
        """count score in one line"""
        index_list = []
        count_list = []
        count = 0
        line_score = 0
        if player == 1:
            for i in range(0, len(line)):
                if line[i] == 1:
                    count = count + 1
                    if i + 1 != len(line):
                        if line[i + 1] != 1:
                            count_list.append(count)
                            index_list.append(i)
                            count = 0
                    else:
                        count_list.append(count)
                        index_list.append(i)
                        count = 0

            for i in range(len(index_list)):
                if index_list[i] + 1 == len(line) and index_list[i] - count_list[i] < 0:
                    continue
                if index_list[i] + 1 == len(line) or line[index_list[i] + 1] == -1:
                    if index_list[i] - self.win_len + 1 < 0:
                        continue
                    if line[index_list[i] - count_list[i]] == 0:
                        line_score = line_score + self.criteria_2[count_list[i] - 1]
                        continue
                    else:
                        continue
                if index_list[i] - count_list[i] < 0 or line[index_list[i] - count_list[i]] == -1:
                    if index_list[i] - count_list[i] + 1 + self.win_len > len(line):
                        continue
                    if line[index_list[i] + 1] == 0:
                        line_score = line_score + self.criteria_2[count_list[i] - 1]
                        continue
                    else:
                        continue
                if line[index_list[i] + 1] == 0 and line[index_list[i] - count_list[i]] == 0:
                    line_score = line_score + self.criteria_1[count_list[i] - 1]
                    continue
                else:
                    pass
        elif player == -1:
            for i in range(0, len(line)):
                if line[i] == -1:
                    count = count + 1
                    if i + 1 != len(line):
                        if line[i + 1] != -1:
                            count_list.append(count)
                            index_list.append(i)
                            count = 0
                    else:
                        count_list.append(count)
                        index_list.append(i)
                        count = 0

            for i in range(len(index_list)):
                if index_list[i] + 1 == len(line) and index_list[i] - count_list[i] < 0:
                    continue
                if index_list[i] + 1 == len(line) or line[index_list[i] + 1] == 1:
                    if index_list[i] - self.win_len + 1 < 0:
                        continue
                    if line[index_list[i] - count_list[i]] == 0:
                        line_score = line_score + self.criteria_2[count_list[i] - 1]
                        continue
                    else:
                        continue
                if index_list[i] - count_list[i] < 0 or line[index_list[i] - count_list[i]] == 1:
                    if index_list[i] - count_list[i] + 1 + self.win_len > len(line):
                        continue
                    if line[index_list[i] + 1] == 0:
                        line_score = line_score + self.criteria_2[count_list[i] - 1]
                        continue
                    else:
                        continue
                if line[index_list[i] + 1] == 0 and line[index_list[i] - count_list[i]] == 0:
                    line_score = line_score + self.criteria_1[count_list[i] - 1]
                    continue
                else:
                    pass
        return line_score

    def count_position_score(self, x, y, player):
        """count score for one player in one position"""
        row = self._count_list_score(self.get_row(x), player)
        col = self._count_list_score(self.get_col(y), player)
        dia = self._count_list_score(self.get_dia(x, y), player)
        anti_dia = self._count_list_score(self.get_anti_dia(x, y), player)
        score = row + col + dia + anti_dia
        return score

    def try_state(self, board, x, y):
        """find the game state"""
        is_full = True

        #   is game board full?
        for i in range(0, len(board)):
            for j in range(0, len(board[0])):
                if board[i][j] == 0:
                    is_full = False
                    break

        # print("count_position_score:", self.count_position_score)

        #   is win/lose/draw?
        if self.count_position_score(x, y, 1) == self.MAX:
            return self.WIN
        if self.count_position_score(x, y, -1) == self.MAX:
            return self.LOSE
        if self.count_position_score(x, y, 1) != self.MAX and self.count_position_score(x, y,
                                                                                        -1) != self.MAX and is_full:
            return self.DRAW

        #   evaluate current score
        result = self.count_position_score(x, y, 1) - self.count_position_score(x, y, -1)
        return result

    def minimax_x(self, board, search_depth, x, y):
        points = gen(board, search_depth)

        best_points = []

        best_value = self.MIN

        for i in range(0, len(points)):
            p = points[i]

            if board[p[0]][p[1]] == 0:
                board[p[0]][p[1]] = 1
                value = self.max_minimax(board, search_depth - 1, best_value if best_value > self.MIN else self.MIN,
                                         self.MAX, x, y)

                if value == best_value:
                    best_points.append(p)
                if value > best_value:
                    best_value = value
                    del best_points[:]
                    best_points.append(p)
                board[p[0]][p[1]] = 0

        result = best_points[math.floor(len(best_points) * random.uniform(0, 1))]
        return result

    def max_minimax(self, board, search_depth, alpha, beta, x, y):
        eval_value = self.try_state(board, x, y)
        is_game_over = False
        is_game_over = (eval_value == self.WIN or eval_value == self.LOSE or eval_value == self.DRAW)

        if search_depth <= 0 or is_game_over:
            return eval_value

        """set LOSE evaluation to MIN"""
        best_value = self.MIN
        points = gen(board, search_depth)

        for i in range(0, len(points)):
            p = points[i]
            if board[p[0]][p[1]] == 0:
                board[p[0]][p[1]] = 1
                best_value = self.min_minimax(board, search_depth - 1, alpha, best_value if best_value > beta else beta,
                                              x,
                                              y)
                board[p[0]][p[1]] = 0
        return eval_value

    def min_minimax(self, board, search_depth, alpha, beta, x, y):
        eval_value = self.try_state(board, x, y)
        is_game_over = False
        is_game_over = (eval_value == self.WIN or eval_value == self.LOSE or eval_value == self.DRAW)

        if search_depth <= 0 or is_game_over:
            return eval_value

        """set WIN evaluation to MAX"""
        best_value = self.MAX
        points = gen(board, search_depth)

        for i in range(0, len(points)):
            p = points[i]
            if board[p[0]][p[1]] == 0:
                board[p[0]][p[1]] = -1
                best_value = self.max_minimax(board, search_depth - 1, alpha, best_value if best_value > beta else beta,
                                              x,
                                              y)
                board[p[0]][p[1]] = 0
        return eval_value


def game_state(board, x, y):
    """find the game state"""
    if board.empty != 0:
        is_full = False
    else:
        is_full = True

    # print("count_position_score:", self.count_position_score)

    #   is win/lose/draw?
    if board.count_position_score(x, y, 1) > board.MAX:
        return board.WIN
    if board.count_position_score(x, y, -1) > board.MAX:
        return board.LOSE
    if board.count_position_score(x, y, 1) < board.MAX and board.count_position_score(x, y,
                                                                                      -1) < board.MAX and is_full:
        return board.DRAW

    #   evaluate current score
    board.current_score = board.count_position_score(x, y, 1) - board.count_position_score(x, y, -1)
    return board.current_score


def has_neighbor(board, point, distance, count):
    """check if this point has pieces within the distance"""
    start_x = point[0] - distance
    end_x = point[0] + distance
    start_y = point[1] - distance
    end_y = point[1] + distance
    for i in range(start_x, end_x):
        if i < 0 or i >= len(board):
            continue
        for j in range(start_y, end_y):
            if j < 0 or j >= len(board):
                continue
            if i == point[0] and j == point[1]:
                continue
            if (board[i][j]) != 0:
                count = count - 1
                if count <= 0:
                    return True
    return False


def gen(board, search_depth):
    """generate all the neighbors into neighbors[]"""
    neighbors = []
    next_neighbors = []

    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == 0:
                if has_neighbor(board, [i, j], 1, 1):
                    neighbors.append([i, j])
                elif search_depth >= 2 and has_neighbor(board, [i, j], 2, 2):
                    next_neighbors.append([i, j])
    neighbors.extend(next_neighbors)
    return neighbors
