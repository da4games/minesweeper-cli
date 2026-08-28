from lib.key_reader import KeyReader
from board import Board

from rich.console import Console

console = Console()
rprint = console.print

MIN_WIDTH = 40
MIN_HEIGHT = 20

if console.width < MIN_WIDTH or console.height < MIN_HEIGHT:
    rprint(
        f"Terminal is too small. "
        f"Need at least {MIN_WIDTH}×{MIN_HEIGHT}, "
        f"but got {console.width}×{console.height}."
    )
    raise SystemExit(1)


def rprint_board(board: list[list[int]]) -> None:
    for list_y in board:
        for i in list_y:
            color: str = "white"
            match i:
                case 0:
                    color = "white"
                case 1:
                    color = "blue"
                case 2:
                    color = "green"
                case 3:
                    color = "red"
                case 4:
                    color = "purple"
                case 5:
                    color = "dark_red"
                case 6:
                    color = "cyan"
                case 7:
                    color = "black"
                case 8:
                    color = "gray"
            rprint(f"[{color}]" + str(i) + f"[{color}]" if not i == -1 else "[red]X[/]", end=" ")
        rprint()


board = Board(MIN_WIDTH, MIN_HEIGHT)

board.generate_board()
rprint_board(board.return_board())
