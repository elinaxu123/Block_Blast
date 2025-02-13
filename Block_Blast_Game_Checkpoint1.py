import pygame #importing pygame to create Block
import random #import random library which creates random numbers

# Initialize Pygame
pygame.init() 

# Screen dimensions
#Tells us how big the grid size is and the block size
GRID_SIZE = 10
BLOCK_SIZE = 40
WIDTH, HEIGHT = GRID_SIZE * BLOCK_SIZE, GRID_SIZE * BLOCK_SIZE + 50 #height has to be a little bigger to fit the scoreboard
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Blast")

# Colors
WHITE = (255, 255, 255) #(Red, Green, Blue)
GRAY = (200, 200, 200)
BLUE = (50, 150, 255)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (50, 255, 50)


# Grid setup
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)] #creates a 10 by 10 2D list, everything becomes zero meaning the cell is empty

# Block shapes
SHAPES = [ #grid starts with all 0 and the '1' takes up a cell in grid making different block shapes
    [[1, 1, 1]], #horizontal 3 cell block
    [[1], [1], [1]], #vertical 3 cell block
    [[1, 1], [1, 1]], #square
    [[1, 1, 0], [0, 1, 1]], #s block
    [[0, 1, 1], [1, 1, 0]], #opposite s block
    [[0,1],[1,1]], #corner block
    [[1,1,1],[0,1,0], [0,1,0]] #T block
]

# Score
score = 0
high_score = 0

# Generate a new block
def new_block():
    shape = random.choice(SHAPES) #takes a random list 
    return shape, 0, GRID_SIZE // 2 - len(shape[0]) // 2 

block, block_x, block_y = new_block()
#generates the block and starts it at the center horizontally

# Check if block can be placed
def can_place(shape, x, y): #placed without placing it on top of another block (x=row, y=column)
    for row in range(len(shape)):
        for col in range(len(shape[0])):
            if shape[row][col] and (x + row >= GRID_SIZE or y + col >= GRID_SIZE or grid[x + row][y + col]): 
                #checks if block goes beyond grid and also check if cell is occupied
                return False #then becomes false
    return True

# Place block on grid
def place_block(shape, x, y):
    global score
    for row in range(len(shape)): #loop through each row
        for col in range(len(shape[0])): #loop through each column
            if shape[row][col]:# If the shape has a block (1) at this position
                grid[x + row][y + col] = 1 # Place the block in the grid
    
    # Check for cleared rows/columns
    cleared = 0 #keep track of how many rows and columns are cleared
    for i in range(GRID_SIZE):
        if all(grid[i]): #checks if entire row is filled (all the values are 1)
            grid[i] = [0] * GRID_SIZE #resets row to 0
            cleared += 1 #add 1 to cleared
        if all(grid[j][i] for j in range(GRID_SIZE)): #j is column, checks if column is filled
            for j in range(GRID_SIZE): 
                grid[j][i] = 0 #resets column to 0
            cleared += 1 #add 1 to cleared
    
    if cleared >= 2: #clear count greater than 2
        score += 50 * cleared #the score count is 50 x cleared count
    else:
        score += cleared * 50
    
    if all(all(row) for row in grid):
        score += 200  # Full clear bonus

# Game loop
running = True #Keeps game running 
clock = pygame.time.Clock() #controls the frame rate
while running:
    screen.fill(WHITE) #display of the game is white
    
    # Event handling
    for event in pygame.event.get(): #getting a list of events (mouse clicking, exiting game, key presses,...)
        print(event) #helps debug the event that are detected
        if event.type == pygame.QUIT: #pygame,QUIT means when you press the x button 
            running = False #running becomes false which stops the game
        elif event.type == pygame.KEYDOWN: #If a key is pressed
            if event.key == pygame.K_LEFT and block_y > 0: 
                block_y -= 1 #when the left key is pressed (decr y coordinate), makes sure block doesn't go past left edge
            if event.key == pygame.K_RIGHT and block_y < GRID_SIZE - len(block[0]):
                block_y += 1 #when the right key is pressed (incr y coordinate), makes such block doesnt go past right edge
            if event.key == pygame.K_DOWN and block_x < GRID_SIZE - len(block):
                block_x += 1 #when down is pressed (incr x coordinate), makes block not go past bottom edge
            if event.key == pygame.K_RETURN and can_place(block, block_x, block_y): #ensures block can be placed (not ontop of other blocks) when pressing return button
                place_block(block, block_x, block_y) #places block
                block, block_x, block_y = new_block() #generates new block
                if not can_place(block, block_x, block_y): #If I cant place block
                    running = False  # No more space, game over
    #printing everything out on the grid so it actually shows up when you play it
    # Draw grid
    for i in range(GRID_SIZE + 1): #all grid lines including the last boundary line
        pygame.draw.line(screen, GRAY, (i * BLOCK_SIZE, 0), (i * BLOCK_SIZE, GRID_SIZE * BLOCK_SIZE)) #uses gray color, creates vertical lines
        pygame.draw.line(screen, GRAY, (0, i * BLOCK_SIZE), (GRID_SIZE * BLOCK_SIZE, i * BLOCK_SIZE)) #uses gray color, creates horizontal lines
    
    # Draw blocks in grid
    for i in range(GRID_SIZE): #loop each row
        for j in range(GRID_SIZE): #loop eac column
            if grid[i][j]: #checks if cell is occupied
                pygame.draw.rect(screen, BLUE, (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                #if not pygame places the block and turns in blue
    
    # Draw current block
    for i in range(len(block)): #loop each row of block
        for j in range(len(block[0])): #loop each column of block
            if block[i][j]: #If the cell in the block is filled (1), draw it
                pygame.draw.rect(screen, RED, ((block_y + j) * BLOCK_SIZE, (block_x + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                #creates the block and makes it red
    
    # Draw score
    font = pygame.font.Font(None, 36) #font and size of the score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0)) #(formats score into string, Smooths Text, Black Color)
    screen.blit(score_text, (10, GRID_SIZE * BLOCK_SIZE + 10))
    
    pygame.display.flip() #refreses screen
    clock.tick(30) #30 frames per second

pygame.quit() #quits the game

#A summary of what the current code does:
    #The Block Blast game is a grid-based puzzle where players place Tetris-like blocks to fill rows and columns. 
    #Blocks appear at the top and can be moved left, right, down, or up before being placed. If a row or column 
    #is completely filled, it disappears, earning the player 50 points per line, with extra bonuses for clearing 
    #multiple lines at once. The game ends when no more blocks can fit on the grid. 
    #The score updates as players clear lines, and a restart button appears when the game is over. 
    #Future improvements could include a high score system and difficulty levels.

#A description of what more needs to be done for the midterm project:
    #There needs to be more types of blocks added to the game, I will a lot more blocks into the game 
    #such as there being more a L block, longer and shorter vertical and horizontal blocks and bigger square block, etc.
    #the score needs to be at the top of the screen and centered as well
    #Also there needs to be more added colors when the blocks are placed down so I will add orange, purple, and pink
#A list of bugs that you are aware of:
    #One of the bugs in the game is that when I place the block at the center where the block is normally teleported to
    #The game automatically ends so I need to change it where the block will either move to a different spot to teleport
    #or the grid will be bigger and there will be a line to show that the block must be placed under the line
    #Also I cannot move my block upwards so I will need to create a pygame.K_UP so everything still works even when moving
    #the block up
    #I also have multiple colors on my colors section but only red and blue show up on the app so I need to alter the code to 
    #add more colors
