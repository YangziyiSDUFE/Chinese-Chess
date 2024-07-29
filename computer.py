import const
from pieces import listPiecestoArr
import Board as bd


def getPlayInfo(listpieces, from_x, from_y, to_x, to_y, mgInit,max_depth=4):
    """
    calculate best move
    :param listpieces: pieces
    :param from_x:
    :param from_y:
    :param to_x:
    :param to_y:
    :param mgInit: player move
    :param max_depth: decided by difficulty
    :return:
    """
    pieces = movedeep(listpieces, 1, const.player2Color, from_x, from_y, to_x, to_y, mgInit,max_depth=max_depth)
    return [pieces[0].x, pieces[0].y, pieces[1], pieces[2]]


def movedeep(listpieces, deepstep, player, x1, y1, x2, y2, mgInit,max_depth=4):
    """
    do alpha-beta for a current step
    :return:
    """
    s = bd.step(8 - x1, y1, 8 - x2, y2)
    # print('ren')
    # print(s)
    mgInit.lastboard = mgInit.board.copy()
    mgInit.move_to(s)

    #gen best
    mgInit.alpha_beta(max_depth, const.min_val, const.max_val)
    t = mgInit.best_move

    mgInit.move_to(t)

    listMoveEnabel = []
    for i in range(0, 9):
        for j in range(0, 10):
            for item in listpieces:
                if item.x == 8 - t.from_x and item.y == t.from_y:
                    listMoveEnabel.append([item, 8 - t.to_x, t.to_y])

    piecesbest = listMoveEnabel[0]

    return piecesbest
