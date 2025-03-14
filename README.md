A summary of what the current code does:
    The Block Blast game is a grid-based puzzle where players place Tetris-like blocks to fill rows and columns. 
    Blocks appear at the top and can be moved left, right, down, or up before being placed. If a row or column 
    is completely filled, it disappears, earning the player 50 points per line, with extra bonuses for clearing 
    multiple lines at once. The game ends when no more blocks can fit on the grid. 
    The score updates as players clear lines, and a restart button appears when the game is over. 
    Future improvements could include a high score system and difficulty levels.

How to Run the Game:
    To run the game, install Pygame (pip install pygame), then execute block_blast_midterm.py. The game involves placing blocks on a grid to form full rows, which then clear for points.

    For testing, run block_blast_test.py using python -m unittest block_blast_test.py. The tests verify block placement and row clearing without using global variables.

How long (cumulative) have you spent on the code?
    Probably around 10 hours, just starting the code, making the test, peer review, etc.
What was the most time consuming part?
    I think the most time-consuming part of the project was figuring out the test and how to put it all together. It was just confusing since you make the game but have to kind of work backwards to make the test
In retrospect, how could you have worked more efficiently?
    I could have worked more efficiently by structuring the code without global variables from the start, making it easier to test and modify. Breaking down functions earlier would have also streamlined debugging.
What libraries/starter code were most useful? To what extent did you
need to modify them?
    The Pygame library was essential for rendering the game, and unittest was crucial for testing. While Pygame provided the core game loop structure, I had to modify it to remove global variables and improve modularity. The test code required adjustments to work without a Game class and pass state explicitly.
