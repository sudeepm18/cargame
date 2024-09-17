import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CAR_WIDTH, CAR_HEIGHT = 50, 80
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 50
ROAD_LINE_WIDTH = 5
BACKGROUND_COLOR = (0, 0, 0)
OBSTACLE_COLOR = (0, 255, 0)
CAR_COLOR = (255, 0, 0)
LINE_COLOR = (255, 255, 255)
FPS = 60
SCORE_INCREMENT = 1
INITIAL_OBSTACLE_SPEED = 5
SPEED_INCREASE_INTERVAL = 10  # Increase speed every 10 seconds
ROAD_LINE_GAP = HEIGHT // 2  # Distance between road lines

# Load images
car_image = pygame.image.load('car.png')
car_image = pygame.transform.scale(car_image, (CAR_WIDTH, CAR_HEIGHT))
crash_sound = pygame.mixer.Sound('crash.mp3')
pygame.mixer.music.load('background.mp3')

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Car Game')

clock = pygame.time.Clock()

# Functions for game
def draw_car(x, y):
    screen.blit(car_image, (x, y))

def draw_obstacle(x, y):
    pygame.draw.rect(screen, OBSTACLE_COLOR, (x, y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

def draw_road_lines(offset):
    for i in range(2):
        line_y = offset + i * ROAD_LINE_GAP
        pygame.draw.line(screen, LINE_COLOR, (WIDTH // 2 - ROAD_LINE_WIDTH // 2, line_y), 
                         (WIDTH // 2 - ROAD_LINE_WIDTH // 2, line_y + 30), ROAD_LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH // 2 + ROAD_LINE_WIDTH // 2, line_y), 
                         (WIDTH // 2 + ROAD_LINE_WIDTH // 2, line_y + 30), ROAD_LINE_WIDTH)

def display_score(score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def game_over(score):
    pygame.mixer.music.stop()
    crash_sound.play()
    font = pygame.font.Font(None, 74)
    text = font.render(f'Game Over! Score: {score}', True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

def button(msg, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    small_text = pygame.font.Font(None, 36)
    text_surface = small_text.render(msg, True, (0, 0, 0))
    screen.blit(text_surface, (x + (w // 2 - text_surface.get_width() // 2), y + (h // 2 - text_surface.get_height() // 2)))

def game_intro():
    intro = True
    pygame.mixer.music.play(-1)  # Play background music

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BACKGROUND_COLOR)
        large_text = pygame.font.Font(None, 74)
        text_surf = large_text.render("Car Game", True, (255, 255, 255))
        screen.blit(text_surf, (WIDTH // 2 - text_surf.get_width() // 2, HEIGHT // 3))

        # Button("message", x, y, width, height, inactive_color, active_color, action)
        button("Start Game", WIDTH // 2 - 100, HEIGHT // 2, 200, 50, (0, 200, 0), (0, 255, 0), main)
        button("Quit", WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, (200, 0, 0), (255, 0, 0), pygame.quit)

        pygame.display.update()
        clock.tick(15)

def main():
    x, y = WIDTH // 2 - CAR_WIDTH // 2, HEIGHT - CAR_HEIGHT - 10
    obstacle_x, obstacle_y = random.randint(0, WIDTH - OBSTACLE_WIDTH), -OBSTACLE_HEIGHT
    obstacle_speed = INITIAL_OBSTACLE_SPEED
    score = 0
    last_speed_increase = pygame.time.get_ticks()

    road_offset = 0
    road_line_speed = 5

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x -= 10
        if keys[pygame.K_RIGHT]:
            x += 10

        screen.fill(BACKGROUND_COLOR)

        road_offset += road_line_speed
        if road_offset >= ROAD_LINE_GAP:
            road_offset -= ROAD_LINE_GAP

        draw_road_lines(road_offset)

        obstacle_y += obstacle_speed
        if obstacle_y > HEIGHT:
            obstacle_y = -OBSTACLE_HEIGHT
            obstacle_x = random.randint(0, WIDTH - OBSTACLE_WIDTH)
            score += SCORE_INCREMENT

        draw_obstacle(obstacle_x, obstacle_y)
        draw_car(x, y)
        display_score(score)

        if (obstacle_x < x + CAR_WIDTH and obstacle_x + OBSTACLE_WIDTH > x and
            obstacle_y < y + CAR_HEIGHT and obstacle_y + OBSTACLE_HEIGHT > y):
            game_over(score)

        pygame.display.flip()

        current_time = pygame.time.get_ticks()
        if current_time - last_speed_increase > SPEED_INCREASE_INTERVAL * 1000:
            obstacle_speed += 1
            last_speed_increase = current_time

        clock.tick(FPS)

if __name__ == "__main__":
    game_intro()
