#A summary of what the current code does:
    #The Block Blast game is a grid-based puzzle where players place Tetris-like blocks to fill rows and columns. 
    #Blocks appear at the top and can be moved left, right, down, or up before being placed. If a row or column 
    #is completely filled, it disappears, earning the player 50 points per line, with extra bonuses for clearing 
    #multiple lines at once. The game ends when no more blocks can fit on the grid. 
    #The score updates as players clear lines, and a restart button appears when the game is over. 
    #Future improvements could include a high score system and difficulty levels.

#Say what you are stuck on and how you got unstuck:
    # Basically during class I explained how my test wasn't working properly and I figured out it was cause the global variable I was using for the block_blast_midterm was not transferring over to the block_blast_test. This was an issue and why my game wasn't working. We started to print out the issues of the test. So what I ended up doing was going back to my original plan of not using global variables. I though using global variables would make the game easier to work with but it made it harder. So eventually I got rid of the global variables and split everything into definitions and imported that into the test. 

#I think the most time-consuming part of the project was figuring out the test and how to put it all together. It was just confusing since you make the game but have to kind of work backwards to make the test

