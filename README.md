# minesweeper as a CLI application
This project is nothing more than a week long project to build minesweeper from scratch as an exercise using minimal help from ai to not get converted to a vibe coder.

## Notable things
- It automatically adjusts the minesweeper board to the size of the terminal it is opened in
  - restart using "restart" to regenerate the board to a new size
- works using minimal imports

## How to play
Tiles are provided in an xy format. Example `a1` or `g10`

Commands:
- "d" or "dig" to dig at a given tile
- "f" or "flag" to toggle a flag on a tile
- "restart" restarts the game
  
Debug:
- "_discover" with any tile to uncover the __whole__ board
- "_flag" to flag all mines and win

## To build from source
1. Clone the repo in any way you like
    >It is recommended to clone the latest release and not the repo itself (download the "Source code.zip")
2. Extract the folder and open it in Vs Code
3. Open a Terminal and execute:
    ```bash
    pyinstaller main.py --icon=assets/icon.ico --onefile --name="[whatever_you_want]"
    ```
    on Debian Linux:
    ```bash
    python3 -m PyInstaller main.py --icon=assets/icon.ico --onefile --name="[whatever_you_want]"F
    ```
