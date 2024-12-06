# Main Function
import pygame
def main():
    pygame.init()
    screen = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    clock = pygame.time.Clock()

    # Start Screen and Difficulty Selection
    difficulty = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                easy_button, medium_button, hard_button = draw_start_screen(screen)

                if easy_button.collidepoint(mouse_pos):
                    difficulty = 30
                    running = False
                elif medium_button.collidepoint(mouse_pos):
                    difficulty = 40
                    running = False
                elif hard_button.collidepoint(mouse_pos):
                    difficulty = 50
                    running = False

        easy_button, medium_button, hard_button = draw_start_screen(screen)
        pygame.display.flip()
        clock.tick(60)

    # Sudoku Board Gameplay
    if difficulty:
        board = Board(540, 540, screen, difficulty)
        initial_state = [row[:] for row in board.board]  # Store the initial board state
        game_running = True

        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False

                # Handle mouse clicks for cell selection and buttons
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check button clicks
                    reset_button, restart_button, exit_button = draw_buttons(screen)
                    if reset_button.collidepoint(mouse_pos):
                        board.reset_board(initial_state)  # Reset board
                    elif restart_button.collidepoint(mouse_pos):
                        main()  # Restart game
                        return
                    elif exit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        return

                    # Handle cell selection
                    board.click(mouse_pos[0], mouse_pos[1])

                # Handle keyboard inputs (unchanged)
                if event.type == pygame.KEYDOWN:
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        board.sketch(event.key - pygame.K_0)
                    elif event.key == pygame.K_RETURN:
                        board.place_number()
                        if board.is_full():
                            if is_board_solved_correctly(board):
                                display_game_won_screen(screen)
                                return
                            else:
                                display_game_over_screen(screen)
                                return
                    elif event.key == pygame.K_UP:
                        board.move_selection("UP")
                    elif event.key == pygame.K_DOWN:
                        board.move_selection("DOWN")
                    elif event.key == pygame.K_LEFT:
                        board.move_selection("LEFT")
                    elif event.key == pygame.K_RIGHT:
                        board.move_selection("RIGHT")

            screen.fill((255, 255, 255))
            board.draw()
            draw_buttons(screen)
            pygame.display.flip()
            clock.tick(60)

    pygame.quit()

# Start Screen Function
def draw_start_screen(screen):
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 74)
    title_text = font.render("Sudoku Game", True, (0, 0, 0))
    screen.blit(title_text, (150, 100))

    font = pygame.font.Font(None, 50)
    easy_button = pygame.draw.rect(screen, (173, 216, 230), (150, 250, 240, 60))
    medium_button = pygame.draw.rect(screen, (135, 206, 250), (150, 350, 240, 60))
    hard_button = pygame.draw.rect(screen, (0, 191, 255), (150, 450, 240, 60))

    easy_text = font.render("Easy", True, (0, 0, 0))
    medium_text = font.render("Medium", True, (0, 0, 0))
    hard_text = font.render("Hard", True, (0, 0, 0))

    screen.blit(easy_text, (220, 260))
    screen.blit(medium_text, (200, 360))
    screen.blit(hard_text, (220, 460))

    return easy_button, medium_button, hard_button


if __name__ == "__main__":
    main()

