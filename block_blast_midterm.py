import pygame
import random

# Constants
WIDTH, HEIGHT = 500, 600
GRID_SIZE = 10
BLOCK_SIZE = WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

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
BLOCKS = [  # grid starts with all 0 and the '1' takes up a cell in grid making different block shapes
    [[1, 1, 1]],  # horizontal 3 cell block
    [[1], [1], [1]],  # vertical 3 cell block
    [[1, 1], [1, 1]],  # square
    [[1, 1, 0], [0, 1, 1]],  # s block
    [[0, 1, 1], [1, 1, 0]],  # opposite s block
    [[0, 1], [1, 1]],  # corner block
    [[1,0],[1,1]], #opposite corner block
    [[1, 1, 1], [0, 1, 0], [0, 1, 0]],  # T block
    [[0,0,1], [0,1,1], [0,0,1]], 
    [[1,0,0], [1,1,0], [1,0,0]]
]

def initialize_game():
    """Initialize the game state: create an empty grid and set score to 0."""
    grid = [[(0, None) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    score = 0
    return grid, score

def new_block():
    """Generate a new random block."""
    shape = random.choice(BLOCKS)
    color = random.choice(COLORS)
    x, y = 0, (GRID_SIZE - len(shape[0])) // 2  # Start in the middle
    return shape, color, x, y

def can_place(grid, shape, x, y):
    """Check if a block can be placed at (x, y)."""
    for row in range(len(shape)):
        for col in range(len(shape[0])):
            if shape[row][col]:
                if x + row >= GRID_SIZE or y + col >= GRID_SIZE or y + col < 0 or grid[x + row][y + col][0]:
                    return False
    return True

def place_block(grid, shape, color, x, y):
    """Place a block on the grid."""
    for row in range(len(shape)):  
        for col in range(len(shape[0])):  
            if shape[row][col]:  
                grid[x + row][y + col] = (1, color)  

def clear_full_rows(grid, score):
    """Clear full rows and update score."""
    rows_to_clear = [i for i in range(GRID_SIZE) if all(grid[i][j][0] for j in range(GRID_SIZE))]
    
    for row in rows_to_clear:
        grid[row] = [(0, None) for _ in range(GRID_SIZE)]  # Clear row

    if rows_to_clear:
        score += 50 * len(rows_to_clear) #one row clear gain 50 points

    return grid, score

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
                if event.key == pygame.K_LEFT and block_y > 0: #left arrow
                    block_y -= 1
                if event.key == pygame.K_RIGHT and block_y < GRID_SIZE - len(block[0]): #right arrow
                    block_y += 1
                if event.key == pygame.K_DOWN and block_x < GRID_SIZE - len(block): #down arrow
                    block_x += 1
                if event.key == pygame.K_UP and block_x > 0: #up arrow
                    block_x -= 1
                if event.key == pygame.K_RETURN and can_place(grid, block, block_x, block_y):
                    place_block(grid, block, block_color, block_x, block_y)
                    grid, score = clear_full_rows(grid, score)
                    block, block_color, block_x, block_y = new_block()
                    if not can_place(grid, block, block_x, block_y):
                        running = False  # Game over

        # Draw grid
        for i in range(GRID_SIZE + 1):
            pygame.draw.line(screen, GRAY, (i * BLOCK_SIZE, 0), (i * BLOCK_SIZE, GRID_SIZE * BLOCK_SIZE))
            pygame.draw.line(screen, GRAY, (0, i * BLOCK_SIZE), (GRID_SIZE * BLOCK_SIZE, i * BLOCK_SIZE))

        # Draw placed blocks
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
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
        screen.blit(score_text, (10, GRID_SIZE * BLOCK_SIZE + 10))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    run_game()
