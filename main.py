import pygame
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
engine = GameEngine(WIDTH, HEIGHT)

# --- Functions ---
def show_game_over(winner):
    SCREEN.fill(BLACK)
    font = pygame.font.SysFont(None, 60)
    text = font.render(f"{winner} Wins!", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    SCREEN.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)

def show_replay_options():
    SCREEN.fill(BLACK)
    font = pygame.font.SysFont(None, 40)
    lines = [
        "Play Again? Choose Best of:",
        "3 - Best of 3",
        "5 - Best of 5",
        "7 - Best of 7",
        "ESC - Exit"
    ]
    for i, line in enumerate(lines):
        text = font.render(line, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80 + i*50))
        SCREEN.blit(text, text_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    return 2  # Best of 3 → first to 2 points
                elif event.key == pygame.K_5:
                    return 3  # Best of 5 → first to 3 points
                elif event.key == pygame.K_7:
                    return 4  # Best of 7 → first to 4 points
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

# --- Main Loop ---
def main():
    TARGET_SCORE = show_replay_options()  # Ask for match length
    paused = False

    running = True
    while running:
        SCREEN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Pause toggle ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            paused = not paused
            pygame.time.delay(200)  # prevent rapid toggle

        engine.handle_input()

        if not paused:
            engine.update()

        engine.render(SCREEN)

        # --- Game Over Check ---
        if engine.player_score >= TARGET_SCORE:
            show_game_over("Player")
            TARGET_SCORE = show_replay_options()
            engine.reset()
        elif engine.ai_score >= TARGET_SCORE:
            show_game_over("AI")
            TARGET_SCORE = show_replay_options()
            engine.reset()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

# --- Run ---
if __name__ == "__main__":
    main()
