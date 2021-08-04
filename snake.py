from random import randint
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

class Snake:
    def __init__(self, init_body, init_direction, board_height, board_width):
        self.body = init_body
        self.direction = init_direction
        self.board_height = board_height
        self.board_width = board_width
        self.mode = "wrap"

    def take_step(self, direction, apple):
        new_head = (self.head[0] + direction[0], self.head[1] + direction[1])

        grow = False
        if new_head == apple.location:
            grow = True

        if grow:
            self.body = [new_head] + self.body
        else:
            self.body = [new_head] + self.body[:-1]

        if self.mode == "wrap":
            self.body = [ (x % self.board_height, y % self.board_width) for x,y in self.body ]

    def set_direction(self, direction):
        self.direction = direction

    @property
    def is_alive(self):
        is_alive_self = len(self.body) == len(set(self.body))
        is_alive_wall = True
        if self.mode == "no_wrap":
            is_alive_wall_x = self.head[0] >= 0 and self.head[0] < self.board_height
            is_alive_wall_y = self.head[1] >= 0 and self.head[1] < self.board_width
            is_alive_wall = is_alive_wall_x and is_alive_wall_y

        return is_alive_self and is_alive_wall

    @property
    def head(self):
        return self.body[0]

    def set_mode(self, mode):
        if mode not in ["wrap", "no_wrap"]:
            return False

        self.mode = mode
        return True

class Apple:
    def __init__(self, location):
        self.location = location

class Game:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.snake = Snake([(0, 0), (1, 0), (2, 0), (3, 0)], UP, self.height, self.width)
        self.commands = {"w": UP, "a": LEFT, "s": DOWN, "d": RIGHT,
                         "h": LEFT, "j": DOWN, "k": UP, "l": RIGHT}

    def board_matrix(self):
        board = []
        for i in range(self.height):
            board.append([])
            for j in range(self.width):
                if self.snake.head == (i,j):
                    board[i].append("x")
                elif (i,j) in self.snake.body:
                    board[i].append("o")
                elif (i,j) == self.apple.location:
                    board[i].append("*")
                else:
                    board[i].append(" ")
        return board


    def render(self):
        print(f"Height: {self.height}")
        print(f"Width: {self.width}")
        board = self.board_matrix()
        print("+" + "-" * self.width + "+")
        for row in board:
            print("|", end="")
            for location in row:
                print(location, end="")
            print("|")
        print("+" + "-" * self.width + "+")

    def gen_apple(self):
        self.apple = Apple((randint(0,self.height-1), randint(0,self.width-1)))



    def run(self):
        while not self.snake.set_mode(input("Choose Mode [wrap/no_wrap]: ")):
            continue
        self.gen_apple()
        points = 0

        self.render()
        while True:
            command = self.commands.get(input(f"Points: {points} Next command: "), None)
            if command is None:
                print("Bad Command Yo")
                continue

            self.snake.take_step(command, self.apple)

            if self.apple.location == self.snake.head:
                points += 1

            while self.apple.location in self.snake.body:
                self.gen_apple()

            self.render()

            if not self.snake.is_alive:
                print("YOU DIED")
                print(f"Points Scored: {points}")
                break

if __name__ == "__main__":
    game = Game(10, 20)
    game.run()
