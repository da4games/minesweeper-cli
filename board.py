import random


class Board:
    def __init__(
        self, MIN_WIDTH: int, MIN_HEIGHT: int, MIN_MINES: int, MAX_MINES: int
    ) -> None:
        self.MIN_WIDTH: int = MIN_WIDTH
        self.MIN_HEIGHT: int = MIN_HEIGHT
        self.board: list[list[int]] = []
        self.cells: list[tuple[int, int]] = []
        self.mask: list[list[int]] = []
        self.MAX_MINES: int = MAX_MINES
        self.MIN_MINES: int = MIN_MINES
        self.mines: set[tuple[int, int]] = set()  # might end up unused
        self.flags: set[tuple[int, int]] = set()
        
        self.generate_board()
        self.generate_mask()

    def neighbors(
        self, coords: tuple[int, int], set_of_coords: set[tuple[int, int]]
    ) -> list[tuple[int, int]]:
        neighbors: list[tuple[int, int]] = [
            (coords[0] + dx, coords[1] + dy)
            for dx in (-1, 0, 1)
            for dy in (-1, 0, 1)
            if (dx, dy) != (0, 0) and (coords[0] + dx, coords[1] + dy) in set_of_coords
        ]
        return neighbors

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
        self.cells = [
            (x, y) for x in range(self.MIN_WIDTH) for y in range(self.MIN_HEIGHT)
        ]

        cells_copy: list[tuple[int, int]] = self.cells.copy()
        random.shuffle(cells_copy)

        mine_count = random.randint(self.MIN_MINES, self.MAX_MINES)
        mines: set[tuple[int, int]] = set(cells_copy[:mine_count])

        coordinate_set = set(cells_copy)

        for mine in mines:
            board[mine[1]][mine[0]] = -1

            neighbors: list[tuple[int, int]] = self.neighbors(mine, coordinate_set)

            for neighbor in neighbors:
                if not neighbor in mines:
                    board[neighbor[1]][neighbor[0]] += 1

        self.mines = mines
        self.board = board

    def generate_mask(self) -> None:
        mask: list[list[int]] = []

        for i in range(self.MIN_HEIGHT):
            mask.append([])
            for j in range(self.MIN_WIDTH):
                mask[i].append(1)

        self.mask = mask

    def dig(self, x: int, y: int) -> None:
        if (x, y) in self.flags:
            return
        
        self.mask[y][x] = 0

        board_cells = set(self.cells)
        queue: list[tuple[int, int]] = [(x, y)]
        visited: set[tuple[int, int]] = set()

        while queue:
            tile = queue.pop()
            if tile in visited:
                continue
            visited.add(tile)

            self.mask[tile[1]][tile[0]] = 0
            if self.board[tile[1]][tile[0]] != 0:
                continue

            for neighbor in self.neighbors(tile, board_cells):
                if self.board[neighbor[1]][neighbor[0]] == -1:
                    continue
                self.mask[neighbor[1]][neighbor[0]] = 0
                if (
                    neighbor not in visited
                    and self.board[neighbor[1]][neighbor[0]] == 0
                ):
                    queue.append(neighbor)
    
    def flag(self, x: int, y: int) -> None:
        if not (x, y) in self.flags:
            self.flags.add((x, y))
        else:
            self.flags.remove((x, y))