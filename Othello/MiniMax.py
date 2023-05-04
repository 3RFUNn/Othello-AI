import random
import time
import turtle
import copy
import math
import time

class OthelloUI:
    def __init__(self, board_size=6, square_size=60):
        self.board_size = board_size
        self.square_size = square_size
        self.screen = turtle.Screen()
        self.screen.setup(self.board_size * self.square_size + 50, self.board_size * self.square_size + 50)
        self.screen.bgcolor('white')
        self.screen.title('Othello')
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)
        turtle.tracer(0, 0)

    def draw_board(self, board):
        self.pen.penup()
        x, y = -self.board_size / 2 * self.square_size, self.board_size / 2 * self.square_size
        for i in range(self.board_size):
            self.pen.penup()
            for j in range(self.board_size):
                self.pen.goto(x + j * self.square_size, y - i * self.square_size)
                self.pen.pendown()
                self.pen.fillcolor('green')
                self.pen.begin_fill()
                self.pen.setheading(0)
                for _ in range(4):
                    self.pen.forward(self.square_size)
                    self.pen.right(90)
                self.pen.penup()
                self.pen.end_fill()
                self.pen.goto(x + j * self.square_size + self.square_size / 2,
                              y - i * self.square_size - self.square_size + 5)
                if board[i][j] == 1:
                    self.pen.fillcolor('white')
                    self.pen.begin_fill()
                    self.pen.circle(self.square_size / 2 - 5)
                    self.pen.end_fill()
                elif board[i][j] == -1:
                    self.pen.fillcolor('black')
                    self.pen.begin_fill()
                    self.pen.circle(self.square_size / 2 - 5)
                    self.pen.end_fill()

        turtle.update()


class Othello:
    def __init__(self, ui, minimax_depth, prune):
        self.size = 6
        self.ui = OthelloUI(self.size) if ui else None
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.board[int(self.size / 2) - 1][int(self.size / 2) - 1] = self.board[int(self.size / 2)][
            int(self.size / 2)] = 1
        self.board[int(self.size / 2) - 1][int(self.size / 2)] = self.board[int(self.size / 2)][
            int(self.size / 2) - 1] = -1
        self.current_turn = random.choice([1, -1])
        self.minimax_depth = minimax_depth
        self.prune = prune

    def get_winner(self):
        white_count = sum([row.count(1) for row in self.board])
        black_count = sum([row.count(-1) for row in self.board])
        if white_count > black_count:
            return 1
        elif white_count < black_count:
            return -1
        else:
            return 0

    def get_valid_moves(self, player):
        moves = set()
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            if di == 0 and dj == 0:
                                continue
                            x, y = i, j
                            captured = []
                            while 0 <= x + di < self.size and 0 <= y + dj < self.size and self.board[x + di][
                                    y + dj] == -player:
                                captured.append((x + di, y + dj))
                                x += di
                                y += dj
                            if 0 <= x + di < self.size and 0 <= y + dj < self.size and self.board[x + di][
                                    y + dj] == player and len(captured) > 0:
                                moves.add((i, j))
        return list(moves)

    def make_move(self, player, move):
        i, j = move
        self.board[i][j] = player
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                x, y = i, j
                captured = []
                while 0 <= x + di < self.size and 0 <= y + dj < self.size and self.board[x + di][y + dj] == -player:
                    captured.append((x + di, y + dj))
                    x += di
                    y += dj
                if 0 <= x + di < self.size and 0 <= y + dj < self.size and self.board[x + di][y + dj] == player:
                    for (cx, cy) in captured:
                        self.board[cx][cy] = player

    def get_cpu_move(self):
        moves = self.get_valid_moves(-1)
        if len(moves) == 0:
            return None
        return random.choice(moves)
    
    # ---------------------- minimax without prune ----------------------------

    # def get_best_move(self, player):
    #     moves = self.get_valid_moves(player)
    #     if len(moves) == 0:
    #         return None
    #     best_move, best_value = None, -math.inf
    #     for move in moves:
    #         new_board = copy.deepcopy(self.board)
    #         self.make_move(player, move)
    #         value = self.minimax(-player, self.minimax_depth - 1)
    #         if value > best_value:
    #             best_move, best_value = move, value
    #         self.board = new_board
    #     return best_move
    
    # def minimax(self, player, depth):
    #     if depth == 0:
    #         return self.heuristic(player)
    #     moves = self.get_valid_moves(player)
    #     if len(moves) == 0:
    #         return self.heuristic(player)
    #     best_value = -math.inf if player == 1 else math.inf
    #     for move in moves:
    #         new_board = copy.deepcopy(self.board)
    #         self.make_move(player, move)
    #         value = self.minimax(-player, depth - 1)
    #         if player == 1:
    #             best_value = max(best_value, value)
    #         else:
    #             best_value = min(best_value, value)
    #         self.board = new_board
    #         if self.prune and best_value == 1:
    #             break
    #     return best_value
    
    # def heuristic(self, player):
    #     white_count = sum([row.count(1) for row in self.board])
    #     black_count = sum([row.count(-1) for row in self.board])
    #     if player == 1:
    #         return white_count - black_count
    #     else:
    #         return black_count - white_count

    # def get_ai_move(self):
    #     return self.get_best_move(1)
    

    #----------------------- minimax with prune ---------------------------
    
    def calculate_the_best_move(self, player):
        moves = self.get_valid_moves(player)
        if len(moves) == 0:
            return None
        best_move = None
        best_score = -math.inf
        for move in moves:
            board_copy = copy.deepcopy(self.board)
            self.make_move(player, move)
            score = self.minimax(-player, self.minimax_depth, -math.inf, math.inf)
            if score > best_score:
                best_score = score
                best_move = move
            self.board = board_copy
        return best_move
    
    def minimax(self, player, depth, alpha, beta):
        if depth == 0:
            return self.evaluate(player)
        moves = self.get_valid_moves(player)
        if len(moves) == 0:
            return self.evaluate(player)
        if player == 1:
            best_score = -math.inf
            for move in moves:
                board_copy = copy.deepcopy(self.board)
                self.make_move(player, move)
                score = self.minimax(-player, depth - 1, alpha, beta)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                self.board = board_copy
                if self.prune and alpha >= beta:
                    break
            return best_score
        else:
            best_score = math.inf
            for move in moves:
                board_copy = copy.deepcopy(self.board)
                self.make_move(player, move)
                score = self.minimax(-player, depth - 1, alpha, beta)
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                self.board = board_copy
                if self.prune and alpha >= beta:
                    break
            return best_score
        
    def evaluate(self, player):
        score = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == player:
                    score += 1
                elif self.board[i][j] == -player:
                    score -= 1
        return score
    
    def get_ai_move(self):
        return self.calculate_the_best_move(1)


    
    
    def get_number_of_moves_for_each_round(self):
        moves = self.get_valid_moves(self.current_turn)
        return len(moves)

    def terminal_test(self):
        return len(self.get_valid_moves(1)) == 0 and len(self.get_valid_moves(-1)) == 0

    def play(self):
        winner = None
        while not self.terminal_test():
            if self.ui:
                self.ui.draw_board(self.board)
            if self.current_turn == 1:
                nodes = self.get_number_of_moves_for_each_round()
                print(f"visited nodes :{nodes}")
                move = self.get_ai_move()
                if move:
                    self.make_move(self.current_turn, move)
            else:
                move = self.get_cpu_move()
                if move:
                    self.make_move(self.current_turn, move)
            self.current_turn = -self.current_turn
            if self.ui:
                self.ui.draw_board(self.board)
                time.sleep(1)
        winner = self.get_winner()
        return winner

def main():
    othello = Othello(8, 7, True)
    start_time = time.time()
    winner = othello.play()
    end_time = time.time()
    print(f"Winner: {winner}")
    print(f"Execution time: {end_time - start_time} seconds")
    
if __name__ == "__main__":
    main()