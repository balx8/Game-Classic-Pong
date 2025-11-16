import pygame
from pygame.locals import *

from ball import Ball
from move_paddle import Paddle, move_ai_paddle

# ----------------- BIẾN ÂM THANH -----------------
sound_hit = None
sound_score = None
SOUND_ENABLED = True   # sau này nếu muốn tắt âm thì set = False


# ----------------- CẤU HÌNH CƠ BẢN -----------------
WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE = (230, 230, 245)
LIGHT_GRAY = (150, 200, 255)
BG_COLOR = (5, 5, 25)

STATE_MENU = "menu"
STATE_GAME = "game"
STATE_SETTINGS = "settings"


class GameConfig:
    def __init__(self, ball_speed, paddle_speed, ai_speed, name):
        self.ball_speed = ball_speed
        self.paddle_speed = paddle_speed
        self.ai_speed = ai_speed
        self.name = name


EASY = GameConfig(ball_speed=5, paddle_speed=7, ai_speed=4, name="EASY")
MEDIUM = GameConfig(ball_speed=7, paddle_speed=7, ai_speed=6, name="MEDIUM")
HARD = GameConfig(ball_speed=9, paddle_speed=8, ai_speed=9, name="HARD")

current_config = MEDIUM


# ----------------- VẼ MENU / SETTINGS -----------------
def draw_menu(screen, font_big, font_small, difficulty_name):
    screen.fill(BG_COLOR)
    w, h = screen.get_size()

    title_surf = font_big.render("CLASSIC PONG", True, WHITE)
    start_surf = font_small.render("ENTER - Start game", True, LIGHT_GRAY)
    settings_surf = font_small.render("S - Settings", True, LIGHT_GRAY)
    quit_surf = font_small.render("Q - Quit", True, LIGHT_GRAY)
    diff_surf = font_small.render(f"Current difficulty: {difficulty_name}", True, LIGHT_GRAY)

    screen.blit(title_surf, (w // 2 - title_surf.get_width() // 2, h // 3))
    screen.blit(start_surf, (w // 2 - start_surf.get_width() // 2, h // 2))
    screen.blit(settings_surf, (w // 2 - settings_surf.get_width() // 2, h // 2 + 40))
    screen.blit(quit_surf, (w // 2 - quit_surf.get_width() // 2, h // 2 + 80))
    screen.blit(diff_surf, (w // 2 - diff_surf.get_width() // 2, h // 2 + 140))


def draw_settings(screen, font_big, font_small, difficulty_name):
    screen.fill((20, 20, 40))
    w, h = screen.get_size()

    title = font_big.render("SETTINGS", True, WHITE)
    line1 = font_small.render("1 - Easy   2 - Medium   3 - Hard", True, LIGHT_GRAY)
    line2 = font_small.render("ESC - Back to menu", True, LIGHT_GRAY)
    current = font_small.render(f"Current difficulty: {difficulty_name}", True, WHITE)

    screen.blit(title, (w // 2 - title.get_width() // 2, h // 3))
    screen.blit(line1, (w // 2 - line1.get_width() // 2, h // 2))
    screen.blit(line2, (w // 2 - line2.get_width() // 2, h // 2 + 40))
    screen.blit(current, (w // 2 - current.get_width() // 2, h // 2 + 100))


# ----------------- KHỞI TẠO OBJECT GAME -----------------
def init_game_objects(config: GameConfig):
    paddle_width, paddle_height = 20, 100

    left_paddle = Paddle(
        x=50,
        y=HEIGHT // 2 - paddle_height // 2,
        width=paddle_width,
        height=paddle_height,
        speed=config.paddle_speed,
        screen_height=HEIGHT,
    )

    right_paddle = Paddle(
        x=WIDTH - 50 - paddle_width,
        y=HEIGHT // 2 - paddle_height // 2,
        width=paddle_width,
        height=paddle_height,
        speed=config.paddle_speed,
        screen_height=HEIGHT,
    )

    ball_radius = 10
    ball = Ball(
        x=WIDTH // 2,
        y=HEIGHT // 2,
        radius=ball_radius,
        speed_x=config.ball_speed,
        speed_y=config.ball_speed,
        color=WHITE,
    )

    scores = [0, 0]  # [left, right]
    return left_paddle, right_paddle, ball, scores


# ----------------- LOGIC GAME (PLAYER + AI + ÂM THANH) -----------------
def update_game(left_paddle: Paddle, right_paddle: Paddle, ball: Ball, scores, config: GameConfig, keys):
    # dùng âm thanh toàn cục
    global sound_hit, sound_score

    # ---- PLAYER 1: điều khiển bằng W/S ----
    left_paddle.move_with_keys(keys, pygame.K_w, pygame.K_s)

    # ---- PADDLE PHẢI: AI BOT ----
    move_ai_paddle(right_paddle, ball_y=ball.y, ai_speed=config.ai_speed)

    # ---- CẬP NHẬT BÓNG (va chạm TRÊN/DƯỚI) ----
    ball.update(WIDTH, HEIGHT)

    # tạo rect bao bóng để check va chạm paddle
    ball_rect = pygame.Rect(
        int(ball.x - ball.radius),
        int(ball.y - ball.radius),
        ball.radius * 2,
        ball.radius * 2,
    )

    # va chạm paddle trái
    if ball_rect.colliderect(left_paddle.rect) and ball.speed_x < 0:
        ball.speed_x = abs(ball.speed_x)
        if SOUND_ENABLED and sound_hit is not None:
            sound_hit.play()

    # va chạm paddle phải
    if ball_rect.colliderect(right_paddle.rect) and ball.speed_x > 0:
        ball.speed_x = -abs(ball.speed_x)
        if SOUND_ENABLED and sound_hit is not None:
            sound_hit.play()

    # ---- GHI ĐIỂM ----
    if ball.x + ball.radius < 0:  # ra ngoài trái
        scores[1] += 1
        if SOUND_ENABLED and sound_score is not None:
            sound_score.play()
        ball.reset(WIDTH, HEIGHT, direction=1)

    if ball.x - ball.radius > WIDTH:  # ra ngoài phải
        scores[0] += 1
        if SOUND_ENABLED and sound_score is not None:
            sound_score.play()
        ball.reset(WIDTH, HEIGHT, direction=-1)


def draw_game(screen, font_small, left_paddle: Paddle, right_paddle: Paddle, ball: Ball, scores):
    screen.fill(BG_COLOR)

    # vẽ đường giữa
    for y in range(0, HEIGHT, 40):
        pygame.draw.rect(screen, LIGHT_GRAY, (WIDTH // 2 - 5, y + 10, 10, 20))

    # vẽ paddles & ball
    left_paddle.draw(screen, WHITE)
    right_paddle.draw(screen, WHITE)
    ball.draw(screen)

    # vẽ điểm
    score_text = font_small.render(f"{scores[0]}   :   {scores[1]}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))


# ----------------- HÀM MAIN -----------------
def main():
    global current_config, sound_hit, sound_score

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Classic Pong")
    clock = pygame.time.Clock()

    font_big = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 36)

    # --- KHỞI TẠO ÂM THANH ---
    pygame.mixer.init()
    sound_hit = pygame.mixer.Sound("sounds/hit.wav")
    sound_score = pygame.mixer.Sound("sounds/score.wav")

    state = STATE_MENU
    running = True

    left_paddle, right_paddle, ball, scores = init_game_objects(current_config)

    while running:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == STATE_MENU and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    left_paddle, right_paddle, ball, scores = init_game_objects(current_config)
                    state = STATE_GAME
                elif event.key == pygame.K_s:
                    state = STATE_SETTINGS
                elif event.key == pygame.K_q:
                    running = False

            elif state == STATE_SETTINGS and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_config = EASY
                elif event.key == pygame.K_2:
                    current_config = MEDIUM
                elif event.key == pygame.K_3:
                    current_config = HARD
                elif event.key == pygame.K_ESCAPE:
                    state = STATE_MENU

            elif state == STATE_GAME and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = STATE_MENU

        # --------- UPDATE + DRAW THEO STATE ---------
        if state == STATE_MENU:
            draw_menu(screen, font_big, font_small, current_config.name)

        elif state == STATE_SETTINGS:
            draw_settings(screen, font_big, font_small, current_config.name)

        elif state == STATE_GAME:
            update_game(left_paddle, right_paddle, ball, scores, current_config, keys)
            draw_game(screen, font_small, left_paddle, right_paddle, ball, scores)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
