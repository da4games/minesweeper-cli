# miesweeper as a cli application
Thsi project is nothing more than a week long project to build minesweeper from scratch as an exercise using minimal help from ai to not get converted to a vibe coder.

## Notable things:
- It automatically adjusts the minesweeper board to the size of the terminal it is opened in
  - restart using "restart" to regenerste the board to a new size
- works using minimal imports
- using "discover" and any coordinates will uncover the whole board for debug puroses

## To build from source:
1. Clone the repo in any way you like
    >It is reccomended to clone the latest release and not the repo itself (download the "Source code.zip")
2. Extract the folder and open it in VSCode
3. Open a Terminal and execute:
    ```bash
    pyinstaller main.py --icon=assets/icon.ico --onefile --name="[whatever_you_want]"
    ```
    on debian linux:
    ```bash
    python3 -m PyInstaller main.py --icon=assets/icon.ico --onefile --name="[whatever_you_want]"F
    ```
