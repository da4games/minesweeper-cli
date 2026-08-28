import random


class Board:
    def __init__(self, MIN_WIDTH: int, MIN_HEIGHT: int) -> None:
        self.MIN_WIDTH: int = MIN_WIDTH
        self.MIN_HEIGHT: int = MIN_HEIGHT
        self.board: list[list[int]] = []
        self.MAX_MINES: int = 100
        self.MIN_MINES: int = 30
        self.mines: set[tuple[int, int]] = set()  # might end up unused

    def generate_board(self) -> None:
        board: list[list[int]] = []

        for i in range(self.MIN_HEIGHT):
            board.append([])
            for j in range(self.MIN_WIDTH):
                board[i].append(0)

        # -1 = mine
        # 0  = empty
        # 1-8 = number

        # spread the mines
        cells: list[tuple[int, int]] = [
            (x, y) for x in range(self.MIN_WIDTH) for y in range(self.MIN_HEIGHT)
        ]

        random.shuffle(cells)

        mine_count = random.randint(self.MIN_MINES, self.MAX_MINES)
        mines: set[tuple[int, int]] = set(cells[:mine_count])

        coordinate_set = set(cells)

        for mine in mines:
            board[mine[1]][mine[0]] = -1

            neighbors: list[tuple[int, int]] = [
                (mine[0] + dx, mine[1] + dy)
                for dx in (-1, 0, 1)
                for dy in (-1, 0, 1)
                if (dx, dy) != (0, 0) and (mine[0] + dx, mine[1] + dy) in coordinate_set
            ]

            for neighbor in neighbors:
                if not neighbor in mines:
                    board[neighbor[1]][neighbor[0]] += 1

        self.mines = mines
        self.board = board

    def return_board(self) -> list[list[int]]:
        return self.board
