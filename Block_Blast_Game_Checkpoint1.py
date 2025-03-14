import pygame  # importing pygame to create Block
import random  # import random library which creates random numbers

# Initialize Pygame
pygame.init()

# Screen dimensions
# Tells us how big the grid size is and the block size
GRID_SIZE = 10
BLOCK_SIZE = 40
WIDTH, HEIGHT = GRID_SIZE * BLOCK_SIZE, GRID_SIZE * BLOCK_SIZE + 50  # height has to be a little bigger to fit the scoreboard
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Blast")

# Colors
WHITE = (255, 255, 255)  # (Red, Green, Blue)
GRAY = (200, 200, 200)

# Preset block colors
BLOCK_COLORS = [
    (255, 255, 102), # Yellow
    (255, 165, 0),   # Orange
    (255, 102, 102), # Red
    (119, 221, 119), # Green
    (137, 207, 240), # Blue
    (177, 156, 217),   # Purple
    (255, 105, 180)  # Pink
]

# Function to get a random block color from the preset list
def random_color():
    return random.choice(BLOCK_COLORS)

# Grid setup (stores tuples: (filled, color))
grid = [[(0, None)] * GRID_SIZE for _ in range(GRID_SIZE)]  # creates a 10 by 10 2D list, each cell stores (0, None) meaning it's empty

# Block shapes
SHAPES = [  # grid starts with all 0 and the '1' takes up a cell in grid making different block shapes
    [[1, 1, 1]],  # horizontal 3 cell block
    [[1], [1], [1]],  # vertical 3 cell block
    [[1, 1], [1, 1]],  # square
    [[1, 1, 0], [0, 1, 1]],  # s block
    [[0, 1, 1], [1, 1, 0]],  # opposite s block
    [[0, 1], [1, 1]],  # corner block
    [[1, 1, 1], [0, 1, 0], [0, 1, 0]],  # T block
    [[0,0,1], [0,1,1], [0,0,1]] 
]

# Score
score = 0

# Generate a new block
def new_block():
    shape = random.choice(SHAPES)  # takes a random shape from the list
    color = random_color()  # Assign a random color to the new block
    return shape, color, 0, GRID_SIZE // 2 - len(shape[0]) // 2

block, block_color, block_x, block_y = new_block()  # generates the block and starts it at the center horizontally

# Check if block can be placed
def can_place(shape, x, y):  # placed without placing it on top of another block (x=row, y=column)
    for row in range(len(shape)):
        for col in range(len(shape[0])):
            if shape[row][col] and (x + row >= GRID_SIZE or y + col >= GRID_SIZE or grid[x + row][y + col][0]):
                # checks if block goes beyond grid and also check if cell is occupied
                return False  # then becomes false
    return True

# Place block on grid
def place_block(shape, color, x, y):
    global score
    for row in range(len(shape)):  # loop through each row
        for col in range(len(shape[0])):  # loop through each column
            if shape[row][col]:  # If the shape has a block (1) at this position
                grid[x + row][y + col] = (1, color)  # Place the block in the grid with its color

    # Check for cleared rows/columns
    cleared = 0  # keep track of how many rows and columns are cleared
    for i in range(GRID_SIZE):
        if all(grid[i][j][0] for j in range(GRID_SIZE)):  # checks if entire row is filled (all the values are 1)
            grid[i] = [(0, None)] * GRID_SIZE  # resets row to 0
            cleared += 1  # add 1 to cleared
        if all(grid[j][i][0] for j in range(GRID_SIZE)):  # j is column, checks if column is filled
            for j in range(GRID_SIZE):
                grid[j][i] = (0, None)  # resets column to 0
            cleared += 1  # add 1 to cleared

    if cleared >= 2:  # clear count greater than 2
        score += 50 * cleared  # the score count is 50 x cleared count
    else:
        score += cleared * 50

    if all(all(cell[0] for cell in row) for row in grid):
        score += 200  # Full clear bonus

# Game loop
running = True  # Keeps game running
clock = pygame.time.Clock()  # controls the frame rate
while running:
    screen.fill(WHITE)  # display of the game is white

    # Event handling
    for event in pygame.event.get():  # getting a list of events (mouse clicking, exiting game, key presses,...)
        if event.type == pygame.QUIT:  # pygame.QUIT means when you press the x button
            running = False  # running becomes false which stops the game
        elif event.type == pygame.KEYDOWN:  # If a key is pressed
            if event.key == pygame.K_LEFT and block_y > 0:
                block_y -= 1  # when the left key is pressed (decr y coordinate), makes sure block doesn't go past left edge
            if event.key == pygame.K_RIGHT and block_y < GRID_SIZE - len(block[0]):
                block_y += 1  # when the right key is pressed (incr y coordinate), makes sure block doesn't go past right edge
            if event.key == pygame.K_DOWN and block_x < GRID_SIZE - len(block):
                block_x += 1  # when down is pressed (incr x coordinate), makes block not go past bottom edge
            if event.key == pygame.K_UP and block_x > 0:
                block_x -= 1  # when up is pressed (decr x coordinate), moves block upward
            if event.key == pygame.K_RETURN and can_place(block, block_x, block_y):  # ensures block can be placed (not on top of other blocks) when pressing return button
                place_block(block, block_color, block_x, block_y)  # places block
                block, block_color, block_x, block_y = new_block()  # generates new block
                if not can_place(block, block_x, block_y):  # If I can't place block
                    running = False  # No more space, game over

    # Draw grid
    for i in range(GRID_SIZE + 1):  # all grid lines including the last boundary line
        pygame.draw.line(screen, GRAY, (i * BLOCK_SIZE, 0), (i * BLOCK_SIZE, GRID_SIZE * BLOCK_SIZE))  # uses gray color, creates vertical lines
        pygame.draw.line(screen, GRAY, (0, i * BLOCK_SIZE), (GRID_SIZE * BLOCK_SIZE, i * BLOCK_SIZE))  # uses gray color, creates horizontal lines

    # Draw blocks in grid
    for i in range(GRID_SIZE):  # loop each row
        for j in range(GRID_SIZE):  # loop each column
            if grid[i][j][0]:  # checks if cell is occupied
                pygame.draw.rect(screen, grid[i][j][1], (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                # if occupied, pygame places the block and keeps its color

    # Draw current block (falling block)
    for i in range(len(block)):  # loop each row of block
        for j in range(len(block[0])):  # loop each column of block
            if block[i][j]:  # If the cell in the block is filled (1), draw it
                pygame.draw.rect(screen, block_color, ((block_y + j) * BLOCK_SIZE, (block_x + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                # creates the block and gives it a random color

    # Draw score
    font = pygame.font.Font(None, 36)  
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))  
    screen.blit(score_text, (10, GRID_SIZE * BLOCK_SIZE + 10))

    pygame.display.flip()  
    clock.tick(30)  

pygame.quit()  

