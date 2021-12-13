from random import randrange
import pygame

# Define some colors
BLACK = (0, 0, 0,)
WHITE = (255, 255, 255,)

RED = (255, 0, 0,)
BLUE = (0, 0, 255,)
GREEN = (0, 255, 0,)
YELLOW = (255, 255, 0,)

SELECTED_RED = (255, 120, 120,)
SELECTED_BLUE = (120, 120, 255,)
SELECTED_GREEN = (120, 255, 120,)
SELECTED_YELLOW = (255, 255, 120,)

SHOW_RED = (135, 0, 0,)
SHOW_BLUE = (0, 0, 135,)
SHOW_GREEN = (0, 135, 0,)
SHOW_YELLOW = (135, 135, 0,)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 250
HEIGHT = 250

COLORS = (({'color': RED, 'name': 'red', 'selectedColor': SELECTED_RED, 'showColor': SHOW_RED},
           {'color': BLUE, 'name': 'blue', 'selectedColor': SELECTED_BLUE, 'showColor': SHOW_BLUE},),
          ({'color': GREEN, 'name': 'green', 'selectedColor': SELECTED_GREEN, 'showColor': SHOW_GREEN},
           {'color': YELLOW, 'name': 'yellow', 'selectedColor': SELECTED_YELLOW, 'showColor': SHOW_YELLOW},),)

CLICK_TIME = .1 * 60
SHOW_TIME = .3 * 60
SHOW_SPACE_TIME = .15 * 60

pygame.init()

FONT = pygame.font.Font('freesansbold.ttf', 32)

# Set the width and height of the screen [width, height]
size = (WIDTH * 2, HEIGHT * 2,)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("TDE grupo 7")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

chose_new = True
sequence = []
selected_sequence = []

show_sequence = True
show_color = ''
show_next_index = 0
show_time = 0

show_space = False
show_space_time = 0

selected_color = ''
click_time = 0

curr_fase = "menu"
defeat = False


def select_color_from_index(idx):
    if idx == 0:
        return 'red'
    elif idx == 1:
        return 'blue'
    elif idx == 2:
        return 'green'

    return 'yellow'


# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # quit
            done = True
        elif curr_fase == "menu":
            # menu
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if WIDTH - 75 <= mouse[0] <= WIDTH + 75 and HEIGHT - 30 <= mouse[1] <= HEIGHT + 30:
                    curr_fase = "game"
        elif defeat:
            # defeat
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if WIDTH - 75 <= mouse[0] <= WIDTH + 75 and HEIGHT + 100 - 30 <= mouse[1] <= HEIGHT + 100 + 30:
                    defeat = False
                    chose_new = True
                    sequence = []
                    selected_sequence = []

                    show_sequence = True
                    show_color = ''
                    show_next_index = 0
                    show_time = 0

                    selected_color = ''
                    click_time = 0
        else:
            # game
            if event.type == pygame.MOUSEBUTTONDOWN and not show_sequence:
                pos = pygame.mouse.get_pos()

                column = pos[0] // WIDTH
                row = pos[1] // HEIGHT

                selected = -1

                if row == 0 and column == 0:
                    # Red
                    selected = 0
                elif row == 0 and column == 1:
                    # Blue
                    selected = 1
                elif row == 1 and column == 0:
                    # Green
                    selected = 2
                else:
                    # Yellow
                    selected = 3
                selected_color = select_color_from_index(selected)

                selected_sequence.append(selected)

                for color, index in zip(selected_sequence, range(len(selected_sequence))):
                    if color != sequence[index]:
                        defeat = True

                if len(selected_sequence) == len(sequence):
                    # Win
                    chose_new = True
                    selected_sequence = []
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                chose_new = True
                sequence = []
                selected_sequence = []

                show_sequence = True
                show_color = ''
                show_next_index = 0
                show_time = 0

                selected_color = ''
                click_time = 0

    if curr_fase == "menu":
        # menu
        blue = (0, 0, 128)

        text = FONT.render('Iniciar', True, WHITE)

        textRect = text.get_rect()

        textRect.center = (WIDTH, HEIGHT)

        screen.fill(WHITE)
        pygame.draw.rect(screen, blue, [WIDTH - 75, HEIGHT - 30, 150, 60])

        screen.blit(text, textRect)
    elif defeat:
        # defeat
        text = FONT.render('Defeat', True, GREEN)
        score = FONT.render('Points: ' + str(len(sequence) - 1), True, BLACK)
        retry = FONT.render('Retry', True, WHITE)

        textRect = text.get_rect()
        textRect.center = (WIDTH, HEIGHT - 50)

        scoreRect = score.get_rect()
        scoreRect.center = (WIDTH, HEIGHT)

        retryRect = retry.get_rect()
        retryRect.center = (WIDTH, HEIGHT + 100)

        screen.fill(WHITE)

        pygame.draw.rect(screen, BLUE, [WIDTH - 75, HEIGHT + 100 - 30, 150, 60])

        screen.blit(text, textRect)
        screen.blit(score, scoreRect)
        screen.blit(retry, retryRect)
    else:
        # --- Game logic should go here
        if selected_color != '':
            click_time += 1
            if click_time >= CLICK_TIME:
                selected_color = ''
                click_time = 0

        if chose_new:
            show_sequence = True
            chose_new = False

            selected = randrange(4)

            sequence.append(selected)

        if show_sequence:
            show_time += 1
            if show_time >= SHOW_TIME:
                show_sequence = False
                show_time = 0
                if show_next_index >= len(sequence):
                    show_next_index = 0
                    show_color = ''
                else:
                    show_space = True

        if show_space:
            show_space_time += 1
            if show_space_time >= SHOW_SPACE_TIME:
                show_space = False
                show_space_time = 0

                show_sequence = True

                color_to_show = sequence[show_next_index]
                show_next_index += 1
                show_color = select_color_from_index(color_to_show)

        # --- Screen-clearing code goes here

        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(WHITE)

        # --- Drawing code should go here
        for row in range(2):
            for column in range(2):
                if selected_color == COLORS[row][column]['name']:
                    color = COLORS[row][column]['selectedColor']
                elif show_sequence and show_color == COLORS[row][column]['name'] and not show_space_time:
                    color = COLORS[row][column]['showColor']
                else:
                    color = COLORS[row][column]['color']

                pygame.draw.rect(screen, color, [WIDTH * column,
                                                 HEIGHT * row,
                                                 WIDTH,
                                                 HEIGHT])

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
