from board import Board

from rich.console import Console
import re
import os
import math

console = Console()
rprint = console.print


class Game:
    def __init__(self, MIN_WIDTH: int, MIN_HEIGHT: int, MINE_COUNT: int) -> None:
        self.MIN_WIDTH: int = MIN_WIDTH
        self.MIN_HEIGHT: int = MIN_HEIGHT

        self.LIGHT_GREEN: str = "#c9ff8d"
        self.BEIGE: str = "#e5c29f"

        if (
            console.width < MIN_WIDTH or console.height < MIN_HEIGHT + 2
        ):  # +2 because of status info and input line
            rprint(
                f"Terminal is too small. "
                f"Need at least {MIN_WIDTH}×{MIN_HEIGHT + 2}, "
                f"but got {console.width}×{console.height}."
            )
            raise SystemExit(1)

        self.board = Board(self.MIN_WIDTH, self.MIN_HEIGHT, MINE_COUNT)

    def alphabet_label(self, n):
        result = ""
        while n > 0:
            n, remainder = divmod(n - 1, 26)
            result = chr(97 + remainder) + result
        return result

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def rprint_board(self) -> None:
        board: Board = self.board

        self.clear()
        rprint(
            "    "
            + "".join(
                f"[bold cyan]{self.alphabet_label(i):<3}[/]"
                for i in range(1, self.MIN_WIDTH + 1)
            )
        )
        for j, list_y in enumerate(board.board):
            rprint(f"{j:<4}", end="")
            for i, cell in enumerate(list_y):
                color: str = "white"
                match cell:
                    case 0:
                        color = self.BEIGE
                        cell = "."
                    case 1:
                        color = "blue"
                    case 2:
                        color = "green"
                    case 3:
                        color = "yellow"
                    case 4:
                        color = "dark_orange"
                    case 5:
                        color = "purple"
                    case 6:
                        color = "cyan"
                    case 7:
                        color = "black"
                    case 8:
                        color = "gray"

                if (i, j) in board.flags:
                    rprint("[red]¶[/]", end="  ")  # ¶ looks kind of like a flag i think
                elif board.mask[j][i] == 1:
                    rprint("#", end="  ", style=f"{self.LIGHT_GREEN}")
                else:
                    rprint(
                        (
                            f"[{color}]" + str(cell) + "[/]"
                            if not cell == -1
                            else "[red bold]X[/]"
                        ),
                        end="  ",
                    )
            rprint()
        rprint(f"  [red]¶ {len(board.flags)}/{len(board.mines)}[/]")

    def main(self) -> bool:
        board: Board = self.board

        self.rprint_board()

        running: bool = True
        while running:
            raw_input: str = console.input()

            if raw_input == "exit":
                return False
            elif raw_input == "restart":
                return True

            try:
                command, coords_str = raw_input.split(" ")
                match = re.fullmatch(r"([a-zA-Z]+)(\d+)", coords_str)
                if not match:
                    raise ValueError

            except ValueError:

                self.rprint_board()
                rprint(
                    "[red]Please enter a valide command like [reverse]'d r10'[/]. Use [reverse]'d'[/] for [reverse]dig[/] and [reverse]'f'[/] for placing a [reverse]flag[/] followed by coordinates.[/]"
                )
                continue

            letter, number = match.groups()

            result: int = 0
            for c in letter:
                result = result * 26 + (ord(c) - ord("a") + 1)
            coords: tuple[int, int] = (
                result - 1,
                int(number),
            )  # -1 because we use list-based coordinates

            if command == "d":
                board.dig(*coords)
            elif command == "f":
                board.flag(*coords)
            if command == "discover":
                for i in range(len(board.mask)):
                    for j in range(len(board.mask[i])):
                        board.mask[i][j] = 0

            if board.board[coords[1]][coords[0]] == -1 and command == "d":
                for mine in board.mines:
                    board.mask[mine[1]][mine[0]] = 0

                self.rprint_board()

                rprint("[red]GAME OVER[/]", end="")
                console.input()
                return True

            self.rprint_board()


if __name__ == "__main__":
    play_again: bool = True
    while play_again:
        size_str: str = console.input("Size[x, y] (leave empty for auto) ")
        width: int
        height: int
        try:
            x, y = size_str.split(" ")
            width = int(x)
            height = int(y)
        except ValueError:
            width = console.width // 3 - 1
            height = console.height - 3
            # //3 becuse of the two " " buffers in between each char
            # -1 because of margin (and the numbers on the left side)
            # -3 because we NEED -2 for the out- and input and then -1 for margin
        
        total_tiles: int = width * height
        mine_density: float = 0.05 * math.log2(total_tiles / 9)
        min_mines: int = 1
        max_mines: int = 2500
        mine_count = round(5 * (total_tiles / 9) ** 0.75)
        mine_count = max(min_mines, min(max_mines, mine_count))

        g = Game(width, height, mine_count)
        play_again = g.main()
