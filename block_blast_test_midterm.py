import unittest
from block_blast_midterm import (
    initialize_game, 
    place_block, 
    clear_full_rows, 
    clear_full_columns, 
    game_over, 
    GRID_WIDTH, 
    GRID_HEIGHT, 
    RED_LINE_ROWS, 
    COLORS
)

class TestBlockBlast(unittest.TestCase):
    def setUp(self):
        """Create a new game state before each test."""
        self.grid, self.score = initialize_game()

    def test_place_block_and_grid_update(self):
        """Test placing a block and verifying grid update for all possible colors."""
        block_shape = [[1, 1], [1, 1]]  # 2x2 square block
        x, y = RED_LINE_ROWS + 1, 4  # Place below the red line

        for color in COLORS:
            place_block(self.grid, block_shape, color, x, y)

            for i in range(len(block_shape)):
                for j in range(len(block_shape[0])):
                    if block_shape[i][j]:
                        self.assertEqual(
                            self.grid[x + i][y + j], (1, color),
                            f"Block placement incorrect in grid for color {color}"
                        )

            # Reset grid for next color test
            self.grid, self.score = initialize_game()

    def test_full_row_clear_below_red_line(self):
        """Test that a full row clears properly below the red line."""
        row_to_fill = RED_LINE_ROWS + 2  # A row in the playable area

        for j in range(GRID_WIDTH):
            self.grid[row_to_fill][j] = (1, (255, 0, 0))  # Fill row with red blocks

        self.grid, self.score = clear_full_rows(self.grid, self.score)

        # Ensure row is cleared
        self.assertTrue(all(self.grid[row_to_fill][j] == (0, None) for j in range(GRID_WIDTH)), 
                        "Full row should be cleared below the red line.")

    def test_full_column_clear_below_red_line(self):
        """Test that a full column clears properly below the red line."""
        col_to_fill = 3  # Pick any column

        for i in range(RED_LINE_ROWS, GRID_HEIGHT):  # Fill column only below red line
            self.grid[i][col_to_fill] = (1, (255, 0, 0))

        self.grid, self.score = clear_full_columns(self.grid, self.score)

        # Ensure column is cleared
        self.assertTrue(all(self.grid[i][col_to_fill] == (0, None) for i in range(RED_LINE_ROWS, GRID_HEIGHT)), 
                        "Full column should be cleared below the red line.")

    def test_game_over_when_block_above_red_line(self):
        """Test that the game ends when a block is placed above the red line."""
        for j in range(GRID_WIDTH):
            self.grid[RED_LINE_ROWS - 1][j] = (1, (255, 0, 0))  # Fill a row above the red line

        self.assertTrue(game_over(self.grid), "Game should end when a block is placed above the red line.")

    def test_game_continues_when_blocks_below_red_line(self):
        """Test that the game does NOT end when blocks are placed correctly below the red line."""
        for j in range(GRID_WIDTH):
            self.grid[RED_LINE_ROWS + 1][j] = (1, (255, 0, 0))  # Fill a row BELOW red line

        self.assertFalse(game_over(self.grid), "Game should continue when blocks are below the red line.")

if __name__ == '__main__':
    unittest.main()
