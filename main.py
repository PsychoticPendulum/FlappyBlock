import pygame
import random

# Initialize pygame
pygame.init()
screen_size = [500, 800]
screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
clock = pygame.time.Clock()
font = pygame.font.SysFont("SFMono-Regular ", 30)
pygame.display.set_caption("Flappy Block")


# Class for game variables
class Game:
    running = True
    score = 0
    mouse_mode = False


# Class for cursor
class Cursor:
    x = 0
    y = 0
    click = False


# Class for player
class Player:
    w = 30
    h = 30
    x = screen_size[0] / 2 - w / 2
    y = screen_size[1] / 2 - h / 2
    dy = 0
    c = [192, 192, 64]
    rect = pygame.Rect(x, y, w, h)
    health = 100


# Class for the pipes
class Pipe:
    w = 50
    h = screen_size[1]
    x = 200
    y = -600
    dx = -5
    c = [32, 128, 64]
    gap = 200
    offset = [-500, -600, -700]
    rect = pygame.Rect(x, y, w, h)


# Create a pipe array containing two pipes
pipe_array = [Pipe(), Pipe()]
pipe_array[0].x = 400
pipe_array[1].x = 900


# Class for the floor
class Floor:
    w = screen_size[0]
    h = 100
    x = 0
    y = 700
    rect = pygame.Rect(x, y, w, h)


# Class for the rainbow colors
class Colors:
    r = 255
    g = 0
    b = 0
    v = 1


# Draw a box with or without black outlines
def draw_box(x, y, w, h, c, o):
    if o:
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x - 2, y - 2, w + 4, h + 4))
    pygame.draw.rect(screen, c, pygame.Rect(x, y, w, h))


# Draw a button and return true if cursor is hovering over it
def draw_button(x, y, w, h, text):
    color_inactive = [32, 64, 255]
    color_active = [32, 194, 255]
    cursor_rect = pygame.Rect(Cursor.x - 2, Cursor.y - 2, 4, 4)
    button_rect = pygame.Rect(x, y, w, h)
    # Check if cursor hovers over button
    if cursor_rect.colliderect(button_rect):
        draw_box(x, y, w, h, color_active, True)
        screen.blit(font.render(text, True, (0, 0, 0)), (x + 5, y))
        return True
    draw_box(x, y, w, h, color_inactive, True)
    screen.blit(font.render(text, True, (0, 0, 0)), (x + 5, y))
    return False


def update_cursor_pos():
    Cursor.x, Cursor.y = pygame.mouse.get_pos()


# Loop through different colors
def rainbow():
    if Colors.r == 255 and Colors.b == 0:
        Colors.g += Colors.v
    if Colors.g == 255 and Colors.r > 0:
        Colors.r -= Colors.v
    if Colors.g == 255 and Colors.r == 0:
        Colors.b += Colors.v
    if Colors.b == 255 and Colors.g > 0:
        Colors.g -= Colors.v
    if Colors.b == 255 and Colors.g == 0:
        Colors.r += Colors.v
    if Colors.r == 255 and Colors.b > 0:
        Colors.b -= Colors.v


def render_player():
    if Game.mouse_mode:
        Player.y = Cursor.y
    else:
        # Gravity
        Player.dy += 1
        # Add velocity offset
        Player.y += Player.dy

    # Update player rect
    Player.rect = pygame.Rect(Player.x, Player.y, Player.w, Player.h)

    # Draw player
    draw_box(Player.x, Player.y, Player.w, Player.h, Player.c, True)


def render_pipes():
    for pipe in pipe_array:
        # If pipe moves out of screen
        if pipe.x < -screen_size[0]:
            # Put it back around
            pipe.x = screen_size[0]
            # Randomize the offset
            pipe.y = random.choice(pipe.offset)
            # Increment score by 1
            Game.score += 1

        # Move pipes
        if Player.health > 0:
            pipe.x += pipe.dx

        # Set rainbow colors
        pipe.c[0] = Colors.r
        pipe.c[1] = Colors.g
        pipe.c[2] = Colors.b

        # Collision detection
        pipe.rect = pygame.Rect(pipe.x, pipe.y, pipe.w, pipe.h)
        if pipe.rect.colliderect(Player.rect):
            Player.health = 0
        pipe.rect = pygame.Rect(pipe.x, pipe.y + pipe.h + pipe.gap, pipe.w, pipe.h)
        if pipe.rect.colliderect(Player.rect):
            Player.health = 0

        # Top Pipe
        draw_box(pipe.x, pipe.y, pipe.w, pipe.h, pipe.c, True)
        # Bottom Pipe
        draw_box(pipe.x, pipe.y + pipe.h + pipe.gap, pipe.w, pipe.h, pipe.c, True)


def render_floor():
    draw_box(Floor.x, Floor.y, Floor.w, Floor.h, (64, 192, 96), True)


def render_hud():
    screen.blit(font.render(str(Game.score), True, (64, 64, 64)), (screen_size[0] / 2 - 10, 35))


# Main Loop
while Game.running:
    # Check is player quit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.running = False
        # Check if player has pressed a key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if Player.health > 0:
                    Player.dy = -15
        # Handle clicks with mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            Cursor.click = True
        if event.type == pygame.MOUSEBUTTONUP:
            Cursor.click = False

    # Background color and floor
    rainbow()
    update_cursor_pos()
    screen.fill((64, 192, 192))

    render_pipes()
    render_player()
    render_floor()
    render_hud()

    if Player.health == 0:
        if draw_button(100, 720, 300, 60, "Restart") and Cursor.click:
            pipe_array[0].x = 900
            pipe_array[1].x = 1400
            Player.y = screen_size[1] / 2 - Player.h / 2
            Player.dy = 0
            Player.health = 100
            Game.score = 0

    # Update window
    pygame.display.update()
    clock.tick(60)  # Set framerate of game

pygame.quit()
