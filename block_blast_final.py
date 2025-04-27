import pygame
import random
import sys
import time

# Grid size presets
GRID_SIZES = {
    'small': (8, 10),
    'medium': (10, 12),
    'large': (12, 14)
}

# Choose size
def get_grid_size():
    print("Choose a grid size: small / medium / large")
    choice = input("Enter grid size: ").strip().lower()
    return GRID_SIZES.get(choice, GRID_SIZES['medium'])

GRID_WIDTH, GRID_HEIGHT = get_grid_size()

# Constants
BLOCK_SIZE = 50
WIDTH = GRID_WIDTH * BLOCK_SIZE
HEIGHT = (GRID_HEIGHT + 1) * BLOCK_SIZE
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
DARK_GRAY = (100, 100, 100)
RED = (255, 0, 0)
OBSTACLE_COLOR = (128, 128, 128)

RED_LINE_ROWS = 3
MOVE_TIME_LIMIT = 10  # seconds to place a block

# Block colors
COLORS = [
    (255, 255, 102), (255, 165, 0), (255, 102, 102),
    (119, 221, 119), (137, 207, 240), (177, 156, 217), (255, 105, 180)
]

# Block shapes
BLOCKS = [
    [[1, 1, 1]],
    [[1], [1], [1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[0, 1], [1, 1]],
    [[1, 0], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[0, 0, 1], [0, 1, 1], [0, 0, 1]],
    [[1, 0, 0], [1, 1, 0], [1, 0, 0]]
]

def initialize_game():
    grid = [[(0, None) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    score = 0
    # Place random obstacles
    for _ in range(GRID_WIDTH // 2):
        x = random.randint(RED_LINE_ROWS, GRID_HEIGHT - 1)
        y = random.randint(0, GRID_WIDTH - 1)
        grid[x][y] = (2, OBSTACLE_COLOR)  # (2, color) = obstacle
    return grid, score

def new_block():
    shape = random.choice(BLOCKS)
    color = random.choice(COLORS)
    x = random.randint(0, RED_LINE_ROWS - len(shape))
    y = (GRID_WIDTH - len(shape[0])) // 2
    return shape, color, x, y

def can_place(grid, shape, x, y):
    for row in range(len(shape)):
        for col in range(len(shape[0])):
            if shape[row][col]:
                if (x + row >= GRID_HEIGHT or y + col >= GRID_WIDTH or y + col < 0 
                    or grid[x + row][y + col][0] != 0):
                    return False
    return True

def place_block(grid, shape, color, x, y):
    for row in range(len(shape)):
        for col in range(len(shape[0])):
            if shape[row][col]:
                grid[x + row][y + col] = (1, color)

def clear_full_rows(grid, score):
    rows_to_clear = [
        i for i in range(RED_LINE_ROWS, GRID_HEIGHT)
        if all(grid[i][j][0] != 0 for j in range(GRID_WIDTH))  # ✅ FIX: accept obstacles too
    ]
    for row in rows_to_clear:
        grid[row] = [(0, None) for _ in range(GRID_WIDTH)]
    score += 50 * len(rows_to_clear)
    return grid, score

def clear_full_columns(grid, score):
    cols_to_clear = [
        j for j in range(GRID_WIDTH)
        if all(grid[i][j][0] != 0 for i in range(RED_LINE_ROWS, GRID_HEIGHT))  # ✅ FIX: accept obstacles too
    ]
    for col in cols_to_clear:
        for row in range(RED_LINE_ROWS, GRID_HEIGHT):
            grid[row][col] = (0, None)
    score += 50 * len(cols_to_clear)
    return grid, score

def game_over(grid):
    for row in range(RED_LINE_ROWS):
        if any(grid[row][col][0] for col in range(GRID_WIDTH)):
            return True
    return False

def no_more_moves(grid, block):
    for x in range(RED_LINE_ROWS, GRID_HEIGHT - len(block) + 1):
        for y in range(GRID_WIDTH - len(block[0]) + 1):
            if can_place(grid, block, x, y):
                return False
    return True

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Block Blast")
    clock = pygame.time.Clock()

    grid, score = initialize_game()
    block, block_color, block_x, block_y = new_block()
    last_move_time = time.time()
    running = True

    while running:
        screen.fill(WHITE)
        current_time = time.time()

        # Auto-place after timeout
        if current_time - last_move_time > MOVE_TIME_LIMIT:
            if can_place(grid, block, block_x, block_y):
                place_block(grid, block, block_color, block_x, block_y)
                grid, score = clear_full_rows(grid, score)
                grid, score = clear_full_columns(grid, score)
            block, block_color, block_x, block_y = new_block()
            if game_over(grid) or no_more_moves(grid, block):
                running = False
            last_move_time = time.time()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and block_y > 0:
                    block_y -= 1
                    last_move_time = time.time()
                elif event.key == pygame.K_RIGHT and block_y < GRID_WIDTH - len(block[0]):
                    block_y += 1
                    last_move_time = time.time()
                elif event.key == pygame.K_DOWN and block_x < GRID_HEIGHT - len(block):
                    block_x += 1
                    last_move_time = time.time()
                elif event.key == pygame.K_UP and block_x > RED_LINE_ROWS:
                    block_x -= 1
                    last_move_time = time.time()
                elif event.key == pygame.K_RETURN and can_place(grid, block, block_x, block_y):
                    place_block(grid, block, block_color, block_x, block_y)
                    grid, score = clear_full_rows(grid, score)
                    grid, score = clear_full_columns(grid, score)
                    block, block_color, block_x, block_y = new_block()
                    if game_over(grid) or no_more_moves(grid, block):
                        running = False
                    last_move_time = time.time()

        # Draw grid
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                rect = pygame.Rect(j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                if i < RED_LINE_ROWS:
                    pygame.draw.rect(screen, DARK_GRAY, rect)
                elif grid[i][j][0] == 2:
                    pygame.draw.rect(screen, OBSTACLE_COLOR, rect)
                elif grid[i][j][0] == 1:
                    pygame.draw.rect(screen, grid[i][j][1], rect)
                pygame.draw.rect(screen, GRAY, rect, 1)

        # Red line
        pygame.draw.rect(screen, RED, (0, RED_LINE_ROWS * BLOCK_SIZE, WIDTH, 2))

        # Draw current block
        for i in range(len(block)):
            for j in range(len(block[0])):
                if block[i][j]:
                    pygame.draw.rect(screen, block_color,
                                     ((block_y + j) * BLOCK_SIZE, (block_x + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # Score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, HEIGHT - 40))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    run_game()
