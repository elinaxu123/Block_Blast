import unittest
from block_blast_final import (
    initialize_game, 
    place_block, 
    clear_full_rows, 
    clear_full_columns, 
    game_over, 
    no_more_moves,
    new_block,
    GRID_WIDTH, 
    GRID_HEIGHT, 
    RED_LINE_ROWS, 
    COLORS
)
class TestBlockBlast(unittest.TestCase):
    def setUp(self):
        """Create a fresh game state before each test."""
        self.grid, self.score = initialize_game()

    def test_place_block_and_grid_update(self):
        """Test placing a block and verifying grid update with all colors."""
        block_shape = [[1, 1], [1, 1]]  # 2x2 block
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

            # Reset grid for next color
            self.grid, self.score = initialize_game()

    def test_full_row_clear_below_red_line(self):
        """Test clearing a full row below the red line."""
        row_to_fill = RED_LINE_ROWS + 2

        for j in range(GRID_WIDTH):
            self.grid[row_to_fill][j] = (1, (255, 0, 0))  # Fill row with red blocks

        self.grid, self.score = clear_full_rows(self.grid, self.score)

        self.assertTrue(all(self.grid[row_to_fill][j] == (0, None) for j in range(GRID_WIDTH)), 
                        "Full row should be cleared below the red line.")

    def test_full_column_clear_below_red_line(self):
        """Test clearing a full column below the red line."""
        col_to_fill = 2

        for i in range(RED_LINE_ROWS, GRID_HEIGHT):
            self.grid[i][col_to_fill] = (1, (255, 0, 0))  # Fill column with red blocks

        self.grid, self.score = clear_full_columns(self.grid, self.score)

        self.assertTrue(all(self.grid[i][col_to_fill] == (0, None) for i in range(RED_LINE_ROWS, GRID_HEIGHT)), 
                        "Full column should be cleared below the red line.")

    def test_game_over_if_block_above_red_line(self):
        """Test that the game ends if a block is placed above the red line."""
        self.grid[RED_LINE_ROWS - 1][0] = (1, (255, 0, 0))  # Place a block in spawn area

        self.assertTrue(game_over(self.grid), "Game should end when a block appears above red line.")

    def test_game_continues_if_blocks_below_red_line(self):
        """Test that the game continues if blocks stay below the red line."""
        self.grid[RED_LINE_ROWS + 2][0] = (1, (255, 0, 0))  # Place a block below the red line

        self.assertFalse(game_over(self.grid), "Game should continue when blocks are placed below the red line.")

    def test_no_more_moves_detected_correctly(self):
        """Test that no more moves detection works."""
        block_shape = [[1, 1], [1, 1]]

        # Fill almost all grid below the red line so no block fits
        for i in range(RED_LINE_ROWS, GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                self.grid[i][j] = (1, (255, 0, 0))

        self.assertTrue(no_more_moves(self.grid, block_shape), "Game should detect no more possible moves.")

if __name__ == '__main__':
    unittest.main()
