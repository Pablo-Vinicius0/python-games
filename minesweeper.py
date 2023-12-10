# Import libraries
from random import randint

# Game config
BOARD_SIZE = 10
NUM_BOMBS = 10

# Constants
DIRECTIONS = (
    (-1, -1), # top-left diagonal
    (-1, 0), # top
    (-1, 1), # top-right diagonal
    (0, 1), # right
    (1, 1), # bottom-right diagonal
    (1, 0), # bottom
    (1, -1), # bottom-left diagonal
    (0, -1), # left
)

class Board:
    def __init__(self, dim_size, num_bombs) -> None:
        self.dim_size = dim_size
        self.num_bombs = num_bombs
        
        self.board = self.generate_board()
        self.visible_board = [[" "] * self.dim_size for _ in range(self.dim_size)]
        self.dug = [[False] * self.dim_size for _ in range(dim_size)]
        self.dug_count = 0

    def generate_board(self) -> list:
        """Method to return a board with the bombs"""  
        board = [[0] * self.dim_size for _ in range(self.dim_size)]
        
        for _ in range(self.num_bombs):
            # Take random positions to plant the bombs
            bomb_pos_i, bomb_pos_j = (randint(0, self.dim_size-1), randint(0, self.dim_size-1))
            # If already have bomb in (bomb_pos_i, bomb_pos_j), other random position is generated
            while True:
                if board[bomb_pos_i][bomb_pos_j] == "*":
                    bomb_pos_i, bom_pos_j = (randint(0, self.dim_size-1), randint(0, self.dim_size-1))
                else:
                    board[bomb_pos_i][bomb_pos_j] = "*"
                    break
            
            # Add "one" for each side of the bomb position
            for i, j in DIRECTIONS:
                tmp_pos_i, tmp_pos_j = bomb_pos_i + i, bomb_pos_j + j
                if tmp_pos_i < 0 or tmp_pos_i >= self.dim_size or tmp_pos_j < 0 or tmp_pos_j >= self.dim_size:
                    continue
                
                if board[tmp_pos_i][tmp_pos_j] == "*":
                    continue
                
                board[tmp_pos_i][tmp_pos_j] += 1
                
        return board
    
    def dig(self, pos_i, pos_j) -> bool:
        """Dig at that position"""
        if self.board[pos_i][pos_j] == "*":
            return False
        elif self.board[pos_i][pos_j] > 0:
            self.visible_board[pos_i][pos_j] = self.board[pos_i][pos_j]
            self.dug[pos_i][pos_j] = True
            self.dug_count += 1
            return True
        # If that position is zero and it's not already dug, reveal the neighbors
        elif not self.dug[pos_i][pos_j]:
            self.dug[pos_i][pos_j] = True
            self.dug_count += 1
            self.visible_board[pos_i][pos_j] = self.board[pos_i][pos_j]
            for i, j in DIRECTIONS:
                tmp_pos_i, tmp_pos_j = pos_i + i, pos_j + j
                if tmp_pos_i < 0 or tmp_pos_i >= self.dim_size or tmp_pos_j < 0 or tmp_pos_j >= self.dim_size:
                    continue
                
                if self.dug[tmp_pos_i][tmp_pos_j]:
                    continue
                
                self.dig(tmp_pos_i, tmp_pos_j)
            
        return True 
        
    def reveal(self) -> None:
        """Reveal all places of the board"""
        self.visible_board = self.board
        
    def __str__(self) -> str:
        """Returns the formatted board"""
        formatted_board = "   "
        for i in range(self.dim_size):
            formatted_board += f"{i}  "
            
        formatted_board += "\n" + "-" * (3 * (self.dim_size + 1))
        
        for i in range(self.dim_size):
            formatted_board += f"\n{i} |"
            tmp = ""
            for j in self.visible_board[i]:
                tmp += f"{j} |"
            formatted_board += tmp
            
        return formatted_board

def play(dim_size=4, num_bombs=4):
    """Main function of the game"""
    board = Board(dim_size, num_bombs)
    
    while board.dug_count < ((dim_size ** 2) - num_bombs):
        print(board)
        
        pos = input("> Choose a position. Input as row, col: ")
        print()
        i, j = (int(n) for n in pos.split(","))
        
        if i < 0 or i >= dim_size or j < 0 or j >= dim_size:
            print("\n> Invalid position!\n")
            continue

        alive = board.dig(i, j)
        if not alive:
            break

    if alive:
        print(board)
        print("\n> YOU WIN!!!!!\n")
    else:
        board.reveal()
        print(board)
        print("\n> Game over.\n")

play(BOARD_SIZE, NUM_BOMBS)