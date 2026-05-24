import pygame
import random
import time
import json

# ==========================================
# Initialize pygame
# ==========================================
pygame.init()

# ==========================================
# Screen settings
# ==========================================
WIDTH = 1000
HEIGHT = 850

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Card Game")

# ==========================================
# Colors
# ==========================================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
RED = (255, 99, 71)
GREEN = (0, 200, 0)
YELLOW = (255, 215, 0)

# ==========================================
# Fonts
# ==========================================
font = pygame.font.SysFont("Arial", 32)
small_font = pygame.font.SysFont("Arial", 24)

# ==========================================
# Medium Mode Settings
# ==========================================
ROWS = 6
COLS = 6

CARD_SIZE = 100
PADDING = 10

TIME_LIMIT = 180

# ==========================================
# Load statistics
# ==========================================
with open("stats.json", "r") as file:
    stats = json.load(file)

# ==========================================
# Buttons
# ==========================================
start_btn = pygame.Rect(380, 20, 220, 60)

restart_btn = pygame.Rect(380, 760, 220, 60)

# ==========================================
# Card Class
# ==========================================
class Card:

    def __init__(self, image, x, y):

        self.image = image

        self.rect = pygame.Rect(
            x,
            y,
            CARD_SIZE,
            CARD_SIZE
        )

        self.revealed = False
        self.matched = False

    def draw(self):

        if self.revealed or self.matched:

            screen.blit(self.image, self.rect)

        else:

            pygame.draw.rect(screen, BLUE, self.rect)

            pygame.draw.rect(
                screen,
                WHITE,
                self.rect,
                3
            )

# ==========================================
# Save stats function
# ==========================================
def save_stats():

    with open("stats.json", "w") as file:

        json.dump(stats, file, indent=4)

# ==========================================
# Create New Game
# ==========================================
def create_new_game():

    global cards
    global first_card
    global second_card

    global game_started
    global game_over
    global game_won

    global start_time

    # --------------------------------------
    # Load images
    # --------------------------------------
    images = []

    for i in range(1, 19):

        img = pygame.image.load(
            f"assets/img{i}.png"
        )

        img = pygame.transform.scale(
            img,
            (CARD_SIZE, CARD_SIZE)
        )

        images.append(img)

    # Duplicate images for matching pairs
    images = images * 2

    # Random shuffle every round
    random.shuffle(images)

    # --------------------------------------
    # Create cards
    # --------------------------------------
    cards = []

    start_x = (
        WIDTH - (
            COLS * CARD_SIZE +
            (COLS - 1) * PADDING
        )
    ) // 2

    start_y = 120

    index = 0

    for row in range(ROWS):

        for col in range(COLS):

            x = start_x + col * (
                CARD_SIZE + PADDING
            )

            y = start_y + row * (
                CARD_SIZE + PADDING
            )

            card = Card(
                images[index],
                x,
                y
            )

            cards.append(card)

            index += 1

    first_card = None
    second_card = None

    game_started = False
    game_over = False
    game_won = False

    start_time = 0

# ==========================================
# Create first game
# ==========================================
create_new_game()

# ==========================================
# Main loop
# ==========================================
running = True

while running:

    screen.fill(BLACK)

    # ======================================
    # Buttons
    # ======================================
    pygame.draw.rect(
        screen,
        GREEN,
        start_btn
    )

    start_text = font.render(
        "START GAME",
        True,
        BLACK
    )

    screen.blit(start_text, (405, 35))

    pygame.draw.rect(
        screen,
        YELLOW,
        restart_btn
    )

    restart_text = font.render(
        "PLAY AGAIN",
        True,
        BLACK
    )

    screen.blit(restart_text, (405, 775))

    # ======================================
    # Statistics display
    # ======================================
    wins_text = small_font.render(
        f"Wins: {stats['wins']}",
        True,
        WHITE
    )

    losses_text = small_font.render(
        f"Losses: {stats['losses']}",
        True,
        WHITE
    )

    best_text = small_font.render(
        f"Best Time: {stats['best_time']}s",
        True,
        WHITE
    )

    screen.blit(wins_text, (30, 760))
    screen.blit(losses_text, (30, 790))
    screen.blit(best_text, (30, 820))

    # ======================================
    # Author Name
    # ======================================
    author_text = small_font.render(
        "Made by Simi Dubey",
        True,
        WHITE
    )

    screen.blit(author_text, (730, 810))

    # ======================================
    # Timer
    # ======================================
    if game_started and not game_over:

        elapsed = int(
            time.time() - start_time
        )

        remaining = TIME_LIMIT - elapsed

        timer_text = font.render(
            f"Time Left: {remaining}s",
            True,
            WHITE
        )

        screen.blit(timer_text, (30, 30))

        # Time Over
        if remaining <= 0:

            game_over = True
            game_won = False

            stats["losses"] += 1

            save_stats()

    # ======================================
    # Draw cards
    # ======================================
    for card in cards:

        if not card.matched:

            card.draw()

    # ======================================
    # Events
    # ======================================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse = pygame.mouse.get_pos()

            # Start game
            if start_btn.collidepoint(mouse) and not game_started:
                game_started = True

                start_time = time.time()

            # Restart game
            if restart_btn.collidepoint(mouse):

                create_new_game()

            # Card clicks
            if game_started and not game_over:

                for card in cards:

                    if (
                        card.rect.collidepoint(mouse)
                        and not card.revealed
                        and not card.matched
                    ):

                        card.revealed = True

                        if first_card is None:

                            first_card = card

                        elif second_card is None:

                            second_card = card

    # ======================================
    # Match Logic
    # ======================================
    if first_card and second_card:


        pygame.display.update()

        pygame.time.delay(60)

        # Match found
        if first_card.image == second_card.image:

            first_card.matched = True
            second_card.matched = True

        # No match
        else:

            first_card.revealed = False
            second_card.revealed = False

        first_card = None
        second_card = None

    # ======================================
    # Win condition
    # ======================================
    if all(card.matched for card in cards):

        if not game_over:

            game_over = True
            game_won = True

            elapsed = int(
                time.time() - start_time
            )

            stats["wins"] += 1

            # Best time update
            if elapsed < stats["best_time"]:

                stats["best_time"] = elapsed

            save_stats()

    # ======================================
    # Result message
    # ======================================
    if game_over:

        if game_won:

            message = (
                f"YOU WON! Time: {elapsed}s"
            )

        else:

            message = "TIME OVER! YOU LOST"

        msg = font.render(
            message,
            True,
            RED
        )

        screen.blit(msg, (280, 720))

    pygame.display.update()

pygame.quit()