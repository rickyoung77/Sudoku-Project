import random
import math

class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0 for _ in range(row_length)] for _ in range(row_length)]

    def get_board(self):
        return self.board

    def print_board(self):
        for row in self.board:
            print(row)

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        return num not in [self.board[row][col] for row in range(self.row_length)]

    def valid_in_box(self, row_start, col_start, num):
        for i in range(3):
            for j in range(3):
                if self.board[row_start + i][col_start + j] == num:
                    return False
        return True

    def is_valid(self, row, col, num):
        return (self.valid_in_row(row, num) and
                self.valid_in_col(col, num) and
                self.valid_in_box(row - row % 3, col - col % 3, num))

    def fill_box(self, row_start, col_start):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                self.board[row_start + i][col_start + j] = nums.pop()

    def fill_diagonal(self):
        for i in range(0, self.row_length, 3):
            self.fill_box(i, i)

    def fill_remaining(self, i=0, j=0):
        if i == self.row_length:
            return True
        if j == self.row_length:
            return self.fill_remaining(i + 1, 0)
        if self.board[i][j] != 0:
            return self.fill_remaining(i, j + 1)

        for num in range(1, 10):
            if self.is_valid(i, j, num):
                self.board[i][j] = num
                if self.fill_remaining(i, j + 1):
                    return True
                self.board[i][j] = 0

        return False

    def remove_cells(self):
        cells_removed = 0
        while cells_removed < self.removed_cells:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                cells_removed += 1

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining()
        
    
    def generate_sudoku(size, removed):
        sudoku = SudokuGenerator(size, removed)
        sudoku.fill_values()
        board = sudoku.get_board()
        sudoku.remove_cells()
        board = sudoku.get_board()
        return board
        





class Cell:
    def __init__(self, value, row, col, screen, width, height):
        self.value = value
        self.sketched_value = 0
        self.row = row
        self.col = col
        self.screen = screen
        self.width = width
        self.height = height
        self.selected = False

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        x = self.col * self.width
        y = self.row * self.height
        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, self.width, self.height), 3)
        if self.value != 0:
            font = pygame.font.Font(None, 36)
            text = font.render(str(self.value), True, (0, 0, 0))
            self.screen.blit(text, (x + 20, y + 10))
        elif self.sketched_value != 0:
            font = pygame.font.Font(None, 24)
            text = font.render(str(self.sketched_value), True, (128, 128, 128))
            self.screen.blit(text, (x + 5, y + 5))

# Board Class (updated for interaction)
class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.board = self.generate_sudoku(9, difficulty)
        self.cells = [[Cell(self.board[i][j], i, j, screen, width // 9, height // 9) for j in range(9)] for i in range(9)]
        self.selected = None

    def generate_sudoku(self, size, removed):
        sudoku = SudokuGenerator(size, removed)
        sudoku.fill_values()
        sudoku.remove_cells()
        return sudoku.get_board()

    def draw(self):
        for i in range(10):
            thick = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * self.height // 9), (self.width, i * self.height // 9), thick)
            pygame.draw.line(self.screen, (0, 0, 0), (i * self.width // 9, 0), (i * self.width // 9, self.height), thick)
        for row in self.cells:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        if self.selected:
            self.cells[self.selected[0]][self.selected[1]].selected = False
        self.selected = (row, col)
        self.cells[row][col].selected = True

    def click(self, x, y):
        row = y // (self.height // 9)
        col = x // (self.width // 9)
        if row < 9 and col < 9:
            self.select(row, col)

    def sketch(self, value):
        if self.selected:
            row, col = self.selected
            self.cells[row][col].set_sketched_value(value)

    def place_number(self):
        if self.selected:
            row, col = self.selected
            if self.cells[row][col].value == 0:
                self.cells[row][col].set_cell_value(self.cells[row][col].sketched_value)
                self.cells[row][col].set_sketched_value(0)

    def move_selection(self, direction):
        if not self.selected:
            return
        row, col = self.selected
        if direction == "UP" and row > 0:
            self.select(row - 1, col)
        elif direction == "DOWN" and row < 8:
            self.select(row + 1, col)
        elif direction == "LEFT" and col > 0:
            self.select(row, col - 1)
        elif direction == "RIGHT" and col < 8:
            self.select(row, col + 1)

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True
    
    def reset_board(self, initial_state):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].set_cell_value(initial_state[i][j])
                self.cells[i][j].set_sketched_value(0) 
                

    def get_row(self, row_idx):
        return [cell.value for cell in self.cells[row_idx]]

    def get_col(self, col_idx):
        return [self.cells[row][col_idx].value for row in range(9)]

    def get_box(self, start_row, start_col):
        box = []
        for i in range(3):
            for j in range(3):
                box.append(self.cells[start_row + i][start_col + j].value)
        return box


def draw_buttons(screen):
    reset_button = pygame.draw.rect(screen, (173, 216, 230), (50, 560, 140, 30))
    restart_button = pygame.draw.rect(screen, (135, 206, 250), (200, 560, 140, 30))
    exit_button = pygame.draw.rect(screen, (255, 99, 71), (350, 560, 140, 30))

    font = pygame.font.Font(None, 24)
    reset_text = font.render("Reset", True, (0, 0, 0))
    restart_text = font.render("Restart", True, (0, 0, 0))
    exit_text = font.render("Exit", True, (0, 0, 0))

    screen.blit(reset_text, (90, 565))
    screen.blit(restart_text, (230, 565))
    screen.blit(exit_text, (390, 565))

    return reset_button, restart_button, exit_button

# Check if the Board is Solved Correctly
def is_board_solved_correctly(board):
    # Check rows, columns, and boxes
    for i in range(9):
        if not check_unique(board.get_row(i)) or not check_unique(board.get_col(i)):
            return False

    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            if not check_unique(board.get_box(row, col)):
                return False

    return True

# Check if a List Contains Unique Non-Zero Values
def check_unique(values):
    values = [v for v in values if v != 0]  # Ignore zeros
    return len(values) == len(set(values))

# Display End Screen
def display_end_screen(screen, message, color):
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 74)
    text = font.render(message, True, color)
    screen.blit(text, (150, 250))
    pygame.display.flip()
    pygame.time.wait(3000)  # Wait for 3 seconds
    
    

    
    
    
def display_game_won_screen(screen):
    screen.fill((255, 255, 255))  # Clear the screen with white
    font = pygame.font.Font(None, 74)
    message = font.render("You Win!", True, (0, 255, 0))
    screen.blit(message, (150, 200))

    # Exit Button
    exit_button = pygame.draw.rect(screen, (255, 99, 71), (200, 400, 140, 50))
    button_font = pygame.font.Font(None, 36)
    exit_text = button_font.render("Exit", True, (255, 255, 255))
    screen.blit(exit_text, (235, 410))

    pygame.display.flip()

    # Wait for user interaction
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    return


def display_game_over_screen(screen):
    screen.fill((255, 255, 255))  # Clear the screen with white
    font = pygame.font.Font(None, 74)
    message = font.render("Game Over!", True, (255, 0, 0))
    screen.blit(message, (150, 200))

    # Restart Button
    restart_button = pygame.draw.rect(screen, (0, 191, 255), (200, 400, 140, 50))
    button_font = pygame.font.Font(None, 36)
    restart_text = button_font.render("Restart", True, (255, 255, 255))
    screen.blit(restart_text, (215, 410))

    pygame.display.flip()

    # Wait for user interaction
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    main()  # Restart the game
                    return
