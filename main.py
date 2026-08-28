from board import Board

from rich.console import Console
import re
import os
import time

console = Console()
rprint = console.print

MIN_WIDTH: int = 40
MIN_HEIGHT: int = 20

LIGHT_GREEN: str = "#c9ff8d"
BEIGE: str = "#e5c29f"

if console.width < MIN_WIDTH or console.height < MIN_HEIGHT:
    rprint(
        f"Terminal is too small. "
        f"Need at least {MIN_WIDTH}×{MIN_HEIGHT}, "
        f"but got {console.width}×{console.height}."
    )
    raise SystemExit(1)


def alphabet_label(n):
    result = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        result = chr(97 + remainder) + result
    return result


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def rprint_board(board: list[list[int]], mask: list[list[int]]) -> None:
    clear()
    rprint(
        "    "
        + "".join(
            f"[bold cyan]{alphabet_label(i):<3}[/]" for i in range(1, MIN_WIDTH + 1)
        )
    )
    for j, list_y in enumerate(board):
        rprint(f"{j:<4}", end="")
        for i, cell in enumerate(list_y):
            color: str = "white"
            match cell:
                case 0:
                    color = BEIGE
                    cell = "."
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

            if mask[j][i] == 1:
                rprint("#", end="  ", style=f"{LIGHT_GREEN}")
            else:
                rprint(
                    f"[{color}]" + str(cell) + "[/]" if not cell == -1 else "[red]X[/]",
                    end="  ",
                )
        rprint()


if __name__ == "__main__":
    board = Board(MIN_WIDTH, MIN_HEIGHT, 100, 300)

    board.generate_board()
    board.generate_mask()

    rprint_board(board.board, board.mask)

    running: bool = True
    while running:
        raw_input: str = console.input()
        try:
            command, coords_str = raw_input.split(" ")
            match = re.fullmatch(r"([a-zA-Z]+)(\d+)", coords_str)
            if not match:
                raise ValueError

        except ValueError:

            rprint_board(board.board, board.mask)
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
            pass

        if board.board[coords[1]][coords[0]] == -1:
            rprint("[red]GAME OVER[/]")
            rprint_board(board.board, board.mask)
            raise SystemExit(1)

        rprint_board(board.board, board.mask)

        time.sleep(0.1)
