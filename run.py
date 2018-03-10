import board

try:
    search_depth = int(input("AI search depth "))
except ValueError:
    print("Not a number")
    print("auto set to 4")
    search_depth = 4

try:
    side_num = int(input("What is the side length of the board? "))
except ValueError:
    print("Not a number")
    side_num = 15
    print("auto set to 10")

try:
    win_len = int(input("length to connect? "))
except ValueError:
    print("Not a number")
    win_len = 5
    print("auto set to 5")

print("setting first player")
print("1 -- this computer")
print("-1 -- the opponent")
go_first = int(input("Who goes first? (1 or -1)  "))
if go_first != 1 and go_first != -1:
    print("error input")
    print("auto set to computer")
    go_first = 1

#   initial board of the game
game = board.Board(side_num, win_len, search_depth)

#   place in the center when go first
if int(go_first) == 1:
    game.set_piece(int(side_num / 2), int(side_num / 2), 1)
    print(game.panel)

while True:
    #   player move
    opponent_move = input("Your move? input in x,y format ")
    opponent_move_list = opponent_move.split(",")
    x = int(opponent_move_list[0])
    y = int(opponent_move_list[1])

    game.set_piece(x, y, -1)
    board.game_state(game, x, y)

    if game.current_score == game.WIN:
        print("You lose!")
        break

    if game.current_score == game.LOSE:
        print("You win!")
        break

    if game.current_score == game.DRAW:
        print("It's a tie!")
        break

    my_move = game.minimax_x(game.panel, search_depth, x, y)
    my_x = my_move[0]
    my_y = my_move[1]
    game.set_piece(my_x, my_y, 1)
    print(game.panel)
    print(" AI went ", my_x, ", ", my_y)


def draw_board():
    print()
    print(game.panel)
    print()
