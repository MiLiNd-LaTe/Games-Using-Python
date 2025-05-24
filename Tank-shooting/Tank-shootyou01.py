wimport pygame
iwmport sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
BULLET_WIDTH, BULLET_HEIGHT = 10, 5
PLAYER_SPEED = 5
BULLET_SPEED = 10
FPS = 60
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 20, 150
OBSTACLE_SPEED = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2-Player Shooting Game with Moving Obstacle")

# Fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Initialize variables
player1 = pygame.Rect(50, HEIGHT // 2 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)
player2 = pygame.Rect(WIDTH - 50 - PLAYER_WIDTH, HEIGHT // 2 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)
player1_score = 0
player2_score = 0
bullets = []
WINNING_SCORE = None

# Obstacle
obstacle = pygame.Rect(WIDTH // 2 - OBSTACLE_WIDTH // 2, HEIGHT // 2 - OBSTACLE_HEIGHT // 2, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
obstacle_direction = 1  # 1: moving down, -1: moving up

# Reset game
def reset_game():
    global player1_score, player2_score, bullets
    player1_score, player2_score = 0, 0
    bullets.clear()

# Winning screen
def display_winning_screen(winner):
    while True:
        screen.fill(BLACK)
        winner_text = font.render(f"{winner} Wins!", True, YELLOW)
        restart_text = small_font.render("Press ESC to Restart or Q to Quit", True, WHITE)

        screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 3))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "restart"
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Setup screen for winning score
def setup_winning_score():
    input_text = ""
    while True:
        screen.fill(BLACK)

        title_text = font.render("Set Winning Score", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))

        input_surface = font.render(input_text, True, YELLOW)
        screen.blit(input_surface, (WIDTH // 2 - input_surface.get_width() // 2, HEIGHT // 2))

        instruction_text = small_font.render("Press ENTER to confirm", True, WHITE)
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_text.isdigit():
                    return int(input_text)
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isdigit():
                    input_text += event.unicode

# Main game loop
clock = pygame.time.Clock()
running = True

# Prompt for winning score
WINNING_SCORE = setup_winning_score()

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Player 1 shoots
            if event.key == pygame.K_f:
                bullet_rect = pygame.Rect(player1.right, player1.centery - BULLET_HEIGHT // 2, BULLET_WIDTH, BULLET_HEIGHT)
                bullets.append({'rect': bullet_rect, 'direction': 1, 'owner': 1})
            # Player 2 shoots
            if event.key == pygame.K_SLASH:
                bullet_rect = pygame.Rect(player2.left - BULLET_WIDTH, player2.centery - BULLET_HEIGHT // 2, BULLET_WIDTH, BULLET_HEIGHT)
                bullets.append({'rect': bullet_rect, 'direction': -1, 'owner': 2})

    # Player movement
    keys = pygame.key.get_pressed()
    # Player 1 movement (W, S)
    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= PLAYER_SPEED
    if keys[pygame.K_s] and player1.bottom < HEIGHT:
        player1.y += PLAYER_SPEED
    # Player 2 movement (UP, DOWN)
    if keys[pygame.K_UP] and player2.top > 0:
        player2.y -= PLAYER_SPEED
    if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
        player2.y += PLAYER_SPEED

    # Move bullets
    for bullet in bullets[:]:
        bullet['rect'].x += bullet['direction'] * BULLET_SPEED

        # Check collision with players
        if bullet['owner'] == 1 and player2.colliderect(bullet['rect']):
            player1_score += 1
            bullets.remove(bullet)
        elif bullet['owner'] == 2 and player1.colliderect(bullet['rect']):
            player2_score += 1
            bullets.remove(bullet)

        # Check collision with obstacle
        elif obstacle.colliderect(bullet['rect']):
            bullets.remove(bullet)

        # Remove bullets that go off-screen
        if bullet['rect'].right < 0 or bullet['rect'].left > WIDTH:
            bullets.remove(bullet)

    # Move obstacle
    obstacle.y += obstacle_direction * OBSTACLE_SPEED
    if obstacle.top <= 0 or obstacle.bottom >= HEIGHT:
        obstacle_direction *= -1

    # Check for winning condition
    if player1_score >= WINNING_SCORE:
        result = display_winning_screen("Player 1")
        if result == "restart":
            WINNING_SCORE = setup_winning_score()
            reset_game()
    if player2_score >= WINNING_SCORE:
        result = display_winning_screen("Player 2")
        if result == "restart":
            WINNING_SCORE = setup_winning_score()
            reset_game()

    # Drawing
    # Draw players
    pygame.draw.rect(screen, RED, player1)
    pygame.draw.rect(screen, BLUE, player2)
    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, bullet['rect'])
    # Draw obstacle
    pygame.draw.rect(screen, GRAY, obstacle)
    # Draw scores
    score_text = font.render(f"{player1_score} - {player2_score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
