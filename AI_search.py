import Board as bd
import const
import numpy as np
import sqlite3


class history_table:
    """
    Here recodes all history moves and its score
    """
    def __init__(self):
        self.table = np.zeros((2, 90, 90))

    def get_history_score(self, who, step):
        if self.table[who, step.from_x * 9 + step.from_y, step.to_x * 9 + step.to_y]:
            return self.table[who, step.from_x * 9 + step.from_y, step.to_x * 9 + step.to_y]
        else:
            return 0

    def add_history_score(self, who, step, depth):
        self.table[who, step.from_x * 9 + step.from_y, step.to_x * 9 + step.to_y] += 2 << depth


class relation:
    """
    store pieces relation
    """
    def __init__(self):
        self.chess_type = 0
        self.num_attack = 0
        self.num_guard = 0
        self.num_attacked = 0
        self.num_guarded = 0
        self.attack = [0, 0, 0, 0, 0, 0]
        self.attacked = [0, 0, 0, 0, 0, 0]
        self.guard = [0, 0, 0, 0, 0, 0]
        self.guarded = [0, 0, 0, 0, 0, 0]


class ai_search:
    def __init__(self):
        self.lastboard = None
        self.board = bd.chess_board()
        self.max_depth = const.max_depth
        self.history_table = history_table()
        self.best_move = bd.step()
        self.cnt = 0

    def last_step(self):
        """
        store last step, will be called if undo move
        :return:
        """
        self.board = self.lastboard

    def set_difficulty(self, difficulty):
        """
        Initial difficulty, 1 for default
        :param difficulty:
        :return:
        """
        if difficulty == 1:
            self.max_depth = 3
        elif difficulty == 2:
            self.max_depth = 4
        elif difficulty == 3:
            self.max_depth = 6
        else:
            self.max_depth = 2

    def alpha_beta(self, depth, alpha, beta):
        """
        Do Alpha-beta puring
        :param depth: Search depth
        :param alpha:
        :param beta:
        :return:
        """
        who = (self.max_depth - depth) % 2
        if self.is_game_over(who):
            return const.min_val
        if depth == 1:
            return self.evaluate(who)

        move_list = self.board.generate_move(who)
        for move in move_list:
            move.score = self.history_table.get_history_score(who, move)
        move_list.sort(key=lambda x: x.score, reverse=True)

        best_move = None
        for move in move_list:
            temp = self.move_to(move)
            # Swap alpha and beta, for next player is opposite
            score = -self.alpha_beta(depth - 1, -beta, -alpha)
            self.undo_move(move, temp)
            if score > alpha:
                alpha = score
                if depth == self.max_depth:
                    self.best_move = move

                best_move = move
            if alpha >= beta:
                break

        if best_move:
            self.history_table.add_history_score(who, best_move, depth)
        return alpha

    def evaluate(self, who):
        """
        :param who: current player, people or AI
        :return:
        """
        relation_list = self.init_relation_list()
        base_val = [0, 0]
        pos_val = [0, 0]
        mobile_val = [0, 0]
        relation_val = [0, 0]
        for x in range(9):
            for y in range(10):
                now_chess = self.board.board[x][y]
                type = now_chess.chess_type
                if type == 0:
                    continue
                # now = 0 if who else 1
                now = now_chess.belong
                pos = x * 9 + y
                temp_move_list = self.board.get_chess_move(x, y, now, True)
                # base value, how much for one
                base_val[now] += const.base_val[type]
                # how much for its postion
                if now == 0:  # if Maximizer
                    pos_val[now] += const.pos_val[type][pos]
                else:
                    pos_val[now] += const.pos_val[type][89 - pos]
                # Relations & how much for it can move
                for item in temp_move_list:

                    # print(item)
                    temp_chess = self.board.board[item.to_x][item.to_y]

                    if temp_chess.chess_type == const.empty:

                        mobile_val[now] += const.mobile_val[type]

                        continue
                    elif temp_chess.belong != now:  # if its opposite

                        if temp_chess.chess_type == const.king:  # if checkmate then win
                            if temp_chess.belong != who:

                                return const.max_val
                            else:
                                relation_val[1 - now] -= 20  # if be checked, cost
                                continue
                        # Attack-relation
                        relation_list[x][y].attack[relation_list[x][y].num_attack] = temp_chess.chess_type
                        relation_list[x][y].num_attack += 1
                        relation_list[item.to_x][item.to_y].chess_type = temp_chess.chess_type

                        relation_list[item.to_x][item.to_y].attacked[
                            relation_list[item.to_x][item.to_y].num_attacked] = type
                        relation_list[item.to_x][item.to_y].num_attacked += 1
                    elif temp_chess.belong == now:

                        if temp_chess.chess_type == const.king:
                            continue

                        relation_list[x][y].guard[relation_list[x][y].num_guard] = temp_chess
                        relation_list[x][y].num_guard += 1
                        relation_list[item.to_x][item.to_y].chess_type = temp_chess.chess_type
                        relation_list[item.to_x][item.to_y].guarded[
                            relation_list[item.to_x][item.to_y].num_guarded] = type
                        relation_list[item.to_x][item.to_y].num_guarded += 1

        for x in range(9):
            for y in range(10):
                # iter list, build relation
                num_attacked = relation_list[x][y].num_attacked
                num_guarded = relation_list[x][y].num_guarded
                now_chess = self.board.board[x][y]
                type = now_chess.chess_type
                now = now_chess.belong
                unit_val = const.base_val[now_chess.chess_type] >> 3
                sum_attack = 0
                sum_guard = 0
                min_attack = 999
                max_attack = 0
                max_guard = 0
                flag = 999
                if type == const.empty:
                    continue
                # calculate attackers
                for i in range(num_attacked):
                    temp = const.base_val[relation_list[x][y].attacked[i]]
                    flag = min(flag, min(temp, const.base_val[type]))
                    min_attack = min(min_attack, temp)
                    max_attack = max(max_attack, temp)
                    sum_attack += temp
                # calculate defenders
                for i in range(num_guarded):
                    temp = const.base_val[relation_list[x][y].guarded[i]]
                    max_guard = max(max_guard, temp)
                    sum_guard += temp
                if num_attacked == 0:
                    relation_val[now] += 5 * relation_list[x][y].num_guarded
                else:
                    muti_val = 5 if who != now else 1
                    if num_guarded == 0:  # ungraded piece
                        relation_val[now] -= muti_val * unit_val
                    else:
                        if flag != 999:  # worth a try
                            relation_val[now] -= muti_val * unit_val
                            relation_val[1 - now] -= muti_val * (flag >> 3)
                        # double relpace 1, still worth
                        elif num_guarded == 1 and num_attacked > 1 and min_attack < const.base_val[type] + sum_guard:
                            relation_val[now] -= muti_val * unit_val
                            relation_val[now] -= muti_val * (sum_guard >> 3)
                            relation_val[1 - now] -= muti_val * (flag >> 3)
                        # 3 for 2
                        elif num_guarded == 2 and num_attacked == 3 and sum_attack - max_attack < const.base_val[
                            type] + sum_guard:
                            relation_val[now] -= muti_val * unit_val
                            relation_val[now] -= muti_val * (sum_guard >> 3)
                            relation_val[1 - now] -= muti_val * ((sum_attack - max_attack) >> 3)
                        # n for n
                        elif num_guarded == num_attacked and sum_attack < const.base_val[
                            now_chess.chess_type] + sum_guard - max_guard:
                            relation_val[now] -= muti_val * unit_val
                            relation_val[now] -= muti_val * ((sum_guard - max_guard) >> 3)
                            relation_val[1 - now] -= sum_attack >> 3

        my_max_val = base_val[0] + pos_val[0] + mobile_val[0] + relation_val[0]
        my_min_val = base_val[1] + pos_val[1] + mobile_val[1] + relation_val[1]
        if who == 0:
            return my_max_val - my_min_val
        else:
            return my_min_val - my_max_val

    def init_relation_list(self):
        res_list = []
        for i in range(9):
            res_list.append([])
            for j in range(10):
                res_list[i].append(relation())
        return res_list



    def is_game_over(self, who):
        """
        :param who: player
        :return: win or loss
        """
        for i in range(9):
            for j in range(10):
                if self.board.board[i][j].chess_type == const.king:
                    if self.board.board[i][j].belong == who:
                        return False
        return True

    def move_to(self, step):
        """
        :param step: given step
        :param flag:
        :return:
        """
        belong = self.board.board[step.to_x][step.to_y].belong
        chess_type = self.board.board[step.to_x][step.to_y].chess_type
        temp = bd.chess(belong, chess_type)

        self.board.board[step.to_x][step.to_y].chess_type = self.board.board[step.from_x][step.from_y].chess_type

        self.board.board[step.to_x][step.to_y].belong = self.board.board[step.from_x][step.from_y].belong
        self.board.board[step.from_x][step.from_y].chess_type = const.empty
        self.board.board[step.from_x][step.from_y].belong = -1

        return temp

    def undo_move(self, step, chess):
        """
        undo move
        :param step: last walk
        :param chess:
        :return:
        """
        self.board.board[step.from_x][step.from_y].belong = self.board.board[step.to_x][step.to_y].belong
        self.board.board[step.from_x][step.from_y].chess_type = self.board.board[step.to_x][step.to_y].chess_type
        self.board.board[step.to_x][step.to_y].belong = chess.belong
        self.board.board[step.to_x][step.to_y].chess_type = chess.chess_type
