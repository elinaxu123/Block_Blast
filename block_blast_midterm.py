import pygame
import random

# Constants
WIDTH, HEIGHT = 500, 700  # Increased height for more gameplay space
GRID_WIDTH, GRID_HEIGHT = 10, 12  # Grid is 12 rows tall
BLOCK_SIZE = WIDTH // GRID_WIDTH
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Red line properties
RED_LINE_ROWS = 4  # The top 4 rows are the "spawn area"

# Define colors for blocks
COLORS = [
    (255, 255, 102), # Yellow
    (255, 165, 0),   # Orange
    (255, 102, 102), # Red
    (119, 221, 119), # Green
    (137, 207, 240), # Blue
    (177, 156, 217),   # Purple
    (255, 105, 180)  # Pink
]

# Define possible blocks
BLOCKS = [
    [[1, 1, 1]],  # horizontal 3-cell block
    [[1], [1], [1]],  # vertical 3-cell block
    [[1, 1], [1, 1]],  # square
    [[1, 1, 0], [0, 1, 1]],  # S block
    [[0, 1, 1], [1, 1, 0]],  # Z block
    [[0, 1], [1, 1]],  # corner block
    [[1, 0], [1, 1]],  # opposite corner block
    [[1, 1, 1], [0, 1, 0]],  # T block
    [[0, 0, 1], [0, 1, 1], [0, 0, 1]], 
    [[1, 0, 0], [1, 1, 0], [1, 0, 0]]
]
# make the grid smaller on top or red line, and make it a full color so it differentiates from the game
#a way for the game to end when there is no where to put another block
def initialize_game():
    """Initialize the game state: create an empty grid and set score to 0."""
    grid = [[(0, None) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    score = 0
    return grid, score

def new_block():
    """Generate a new random block above the red line."""
    shape = random.choice(BLOCKS)
    color = random.choice(COLORS)
    x, y = random.randint(0, RED_LINE_ROWS - len(shape)), (GRID_WIDTH - len(shape[0])) // 2  
    return shape, color, x, y

def can_place(grid, shape, x, y):
    """Check if a block can be placed at (x, y)."""
    for row in range(len(shape)):
        for col in range(len(shape[0])):
            if shape[row][col]:
                if x + row >= GRID_HEIGHT or y + col >= GRID_WIDTH or y + col < 0 or grid[x + row][y + col][0]:
                    return False
    return True

def place_block(grid, shape, color, x, y):
    """Place a block on the grid."""
    for row in range(len(shape)):  
        for col in range(len(shape[0])):  
            if shape[row][col]:  
                grid[x + row][y + col] = (1, color)  

def clear_full_rows(grid, score):
    """Clear full rows **below the red line** and update score."""
    rows_to_clear = [i for i in range(RED_LINE_ROWS, GRID_HEIGHT) if all(grid[i][j][0] for j in range(GRID_WIDTH))]
    
    for row in rows_to_clear:
        grid[row] = [(0, None) for _ in range(GRID_WIDTH)]  # Clear row

    if rows_to_clear:
        score += 50 * len(rows_to_clear)  # One row cleared = 50 points

    return grid, score

def clear_full_columns(grid, score):
    """Clear full columns **below the red line** and update score."""
    cols_to_clear = [
        j for j in range(GRID_WIDTH) if all(grid[i][j][0] for i in range(RED_LINE_ROWS, GRID_HEIGHT))
    ]
    
    for col in cols_to_clear:
        for row in range(RED_LINE_ROWS, GRID_HEIGHT):  # Only clear below the red line
            grid[row][col] = (0, None)

    if cols_to_clear:
        score += 50 * len(cols_to_clear)  # One column cleared = 50 points

    return grid, score

def game_over(grid):
    """Check if the game is over (if a block is placed above the red line)."""
    for row in range(RED_LINE_ROWS):
        if any(grid[row][col][0] for col in range(GRID_WIDTH)):
            return True
    return False

def run_game():
    """Main game loop."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Block Blast")
    clock = pygame.time.Clock()

    grid, score = initialize_game()
    block, block_color, block_x, block_y = new_block()
    running = True

    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and block_y > 0:  
                    block_y -= 1
                if event.key == pygame.K_RIGHT and block_y < GRID_WIDTH - len(block[0]):  
                    block_y += 1
                if event.key == pygame.K_DOWN and block_x < GRID_HEIGHT - len(block):  
                    block_x += 1
                if event.key == pygame.K_UP and block_x > RED_LINE_ROWS:  # Allow up movement within playable area
                    block_x -= 1
                if event.key == pygame.K_RETURN and can_place(grid, block, block_x, block_y):
                    place_block(grid, block, block_color, block_x, block_y)
                    grid, score = clear_full_rows(grid, score)
                    grid, score = clear_full_columns(grid, score)  # Now clears full columns too
                    block, block_color, block_x, block_y = new_block()
                    if game_over(grid):
                        running = False  # Game over

        # Draw grid
        for i in range(GRID_HEIGHT + 1):
            pygame.draw.line(screen, GRAY, (i * BLOCK_SIZE, 0), (i * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE))
            pygame.draw.line(screen, GRAY, (0, i * BLOCK_SIZE), (GRID_WIDTH * BLOCK_SIZE, i * BLOCK_SIZE))

        # Draw red line
        pygame.draw.rect(screen, RED, (0, RED_LINE_ROWS * BLOCK_SIZE, WIDTH, 2))

        # Draw placed blocks
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if grid[i][j][0]:
                    pygame.draw.rect(screen, grid[i][j][1], (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # Draw current block
        for i in range(len(block)):
            for j in range(len(block[0])):
                if block[i][j]:
                    pygame.draw.rect(screen, block_color, ((block_y + j) * BLOCK_SIZE, (block_x + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, GRID_HEIGHT * BLOCK_SIZE + 10))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    run_game()

