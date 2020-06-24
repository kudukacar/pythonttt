class Board:
    def __init__(self):
        self.board = [None for x in range(9)]

    def get(self, position):
        return self.board[position - 1]

    def place(self, position, token):
        self.board[position - 1] = token

    def available(self, position):
        return self.board[position - 1] == None

    def lines(self):
        return [
            [1, 2, 3],
            [4, 5, 6], 
            [7, 8, 9],
            [1, 4, 7],
            [2, 5, 8], 
            [3, 6, 9],
            [1, 5, 9],
            [3, 5, 7]
        ]

    def winner(self):
        winning_line = list(filter(lambda line: self.get(line[0]) == self.get(line[1]) == self.get(line[2]) and self.get(line[0]), self.lines()))
        if len(winning_line) > 0:
            return self.get(winning_line[0][0])
        else:
            return None

    def draw(self):
        return (self.winner() == None) and not(None in self.board)


class Display:
    def output(self, message):
        print(message)

    def input(self):
        return input()

class Presenter:
    def present(self, board):
        return f'''
         {board.get(1) or " "} | {board.get(2) or " "} | {board.get(3) or " "}
        ---+---+---
         {board.get(4) or " "} | {board.get(5) or " "} | {board.get(6) or " "}
        ---+---+---
         {board.get(7) or " "} | {board.get(8) or " "} | {board.get(9) or " "}
        ''' + self.outcome(board)

    def outcome(self, board):
        if board.draw():
            return "Draw!"
        elif winner := board.winner():
            return f'{winner} wins!'
        else:
            return ""

class Player:
    def __init__(self, token):
        self.token = token

    def selection(self, display, board):
        while True:
            display.output("Please enter a selection [1, 9]")
            try:
                input = int(display.input().strip())
            except:
                input = 0

            if input in range(1, 10):
                if board.available(input):
                    return input
                else:
                    display.output("Selection taken")
            else:
                display.output("Selection invalid")


class TicTacToe:
    def __init__(self, board, presenter, display, players):
        self.board = board
        self.presenter = presenter
        self.display = display
        self.players = players

    def run(self):
        i = 0
        self.show_board()
        while self.board.draw() == False and self.board.winner() == None:
            self.play_turn(self.players[i % 2])
            self.show_board()
            i += 1


    def show_board(self):
        self.display.output(self.presenter.present(self.board))

    def play_turn(self, player):
        selection = player.selection(self.display, self.board)
        self.board.place(selection, player.token)

if __name__ == "__main__":
    board = Board()
    presenter = Presenter()
    display = Display()
    first_player = Player("X")
    second_player = Player("O")
    TicTacToe(board, presenter, display, [first_player, second_player]).run()