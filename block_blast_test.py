import unittest
from block_blast_midterm import initialize_game, place_block, clear_full_rows, GRID_SIZE, COLORS

class TestBlockBlast(unittest.TestCase):
    def setUp(self):
        """Create a new game state before each test."""
        self.grid, self.score = initialize_game()

    def test_place_block_and_grid_update(self):
        """Test placing a block and verifying grid update for all possible colors."""
        block_shape = [[1, 1], [1, 1]]  # 2x2 square block
        x, y = 3, 4  # Arbitrary position

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

    def test_full_row_clear(self):
        """Test that a full row clears properly"""
        for j in range(GRID_SIZE):
            self.grid[5][j] = (1, (255, 0, 0))  # Fill row 5 with red blocks

        self.grid, self.score = clear_full_rows(self.grid, self.score)

        # Ensure row 5 is cleared
        self.assertTrue(all(self.grid[5][j] == (0, None) for j in range(GRID_SIZE)), "Full row should be cleared")

if __name__ == '__main__':
    unittest.main()

