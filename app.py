import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nim Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.Font(None, 36)

def draw_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def get_initial_tokens():
    input_text = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode.isdigit():
                    input_text += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if input_text and int(input_text) > 0:
                        return int(input_text)
        
        screen.fill(BLACK)
        draw_text("Enter the number of initial tokens:", WIDTH // 2, HEIGHT // 2 - 50)
        draw_text(input_text, WIDTH // 2, HEIGHT // 2 + 50, GREEN)
        pygame.display.flip()

def minimax(tokens, is_maximizing):
    if tokens == 0:
        return 1 if is_maximizing else -1  # Reverse the scores

    if is_maximizing:
        best_score = float('-inf')
        for i in range(1, min(4, tokens + 1)):
            score = minimax(tokens - i, False)
            best_score = max(score, score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(1, min(4, tokens + 1)):
            score = minimax(tokens - i, True)
            best_score = min(score, score)
        return best_score

def get_best_move(tokens):
    best_score = float('-inf')
    best_move = -1
    for i in range(1, min(4, tokens + 1)):
        score = minimax(tokens - i, False)
        if score > best_score:
            best_score = score
            best_move = i
    return best_move

def main():
    tokens = get_initial_tokens()
    player_turn = True
    game_over = False
    winner = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_r:
                        return
                elif player_turn and not game_over:
                    if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                        move = int(event.unicode)
                        if move <= tokens:
                            tokens -= move
                            if tokens == 0:
                                game_over = True
                                winner = "Computer"
                            else:
                                player_turn = False

        screen.fill(BLACK)

        if not game_over:
            draw_text(f"Tokens left: {tokens}", WIDTH // 2, 50)
            draw_text("Your turn" if player_turn else "Computer's turn", WIDTH // 2, 100)
            
            if player_turn:
                draw_text("Press 1, 2, or 3 to remove tokens", WIDTH // 2, HEIGHT - 50)
            else:
                computer_move = get_best_move(tokens)
                tokens -= computer_move
                if tokens == 0:
                    game_over = True
                    winner = "You"
                else:
                    player_turn = True

        if game_over:
            draw_text(f"{winner} won!", WIDTH // 2, HEIGHT // 2 - 50)
            draw_text("Press Q to quit or R to restart", WIDTH // 2, HEIGHT // 2 + 50)

        pygame.display.flip()

if __name__ == "__main__":
    while True:
        main()