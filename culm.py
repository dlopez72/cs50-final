import pygame
from random import choice, shuffle

# the arrays on the right are the shapes of the blockss
# eg the T is [
# [0, 1, 0]
# [1, 1, 1]
# ]
tetrominoes = {
    'O': {'color': "yellow", 'shape': [[1, 1], [1, 1]]},
    'I': {'color': "cyan", 'shape': [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]},
    'Z': {'color': "red", 'shape': [[1, 1, 0], [0, 1, 1]]},
    'S': {'color': "green", 'shape': [[0, 1, 1], [1, 1, 0]]},
    'J': {'color': "blue", 'shape': [[1, 0, 0], [1, 1, 1]]},
    'L': {'color': "orange", 'shape': [[0, 0, 1], [1, 1, 1]]},
    'T': {'color': "purple", 'shape': [[0, 1, 0], [1, 1, 1]]}
}

# set up pygame stuff
pygame.init()
screen = pygame.display.set_mode((250, 600))
pygame.display.set_caption("ICS3U1 Tetris")
state = "title"

# run until user asks to quit
running = True

class Tetromino:
    def __init__(self, shapecolor=None):
        # generates a random shapecolor if one isn't provided
        if not shapecolor:
            self.shapecolor = choice(list(tetrominoes.keys()))
        else:
            self.shapecolor = shapecolor
        # uses the dict to assign a color and shape to the main key
        self.color = tetrominoes[self.shapecolor]['color']
        self.shape = tetrominoes[self.shapecolor]['shape']
        self.position = [0, round(10 / 2) - round(len(self.shape[0]) / 2)]

    # move block left if a is pressed and it's a valid position.
    def movement(self, direction):
        if direction == "left":
            self.position[1] -= 1
            if not self.valid_position():
                self.position[1] += 1
        elif direction == "right":
            self.position[1] += 1
            if not self.valid_position():
                self.position[1] -= 1
        
    def gravity(self):
        self.position[0] += 1
        if not self.valid_position():
            self.position[0] -= 1
            self.lockin()

    def slam(self):
        # tries to go 1 down over and over until it can't anymore which simulates a hard drop
        for i in range(19): 
            self.position[0] += 1
            if not self.valid_position():
                self.position[0] -= 1
                self.lockin()
                break

    def rotate(self, direction):
        if direction == "right":
            # found this neat line on stack overflow, it rotates a 2d list clockwise
            # (in this case the block)
            self.shape = list(zip(*self.shape[::-1]))
            if not self.valid_position():
                # this trys moving the block to the left (this fixes the block being unable to rotate on the right)
                self.position[1] -= 1
                if not self.valid_position():
                    # same but counter clockwise
                    self.position[1] += 1
                    self.shape = list(zip(*self.shape))[::-1]
        elif direction == "left":
            self.shape = list(zip(*self.shape))[::-1]
            if not self.valid_position():
                self.position[1] -= 1
                if not self.valid_position():
                    self.position[1] += 1
                    self.shape = list(zip(*self.shape[::-1]))

    # checks if the position you're trying to go to is valid
    # if nothing is inputted it uses the position of the tetromino otherwise it will use the provided coordinates
    def valid_position(self, pos=None):
        if not pos:
            for row_index, row in enumerate(self.shape):
                for col_index, value in enumerate(row):
                    if value != 0:
                        new_x = self.position[1] + col_index
                        new_y = self.position[0] + row_index
                        if new_x < 0 or new_x > 9 or new_y > 19 or (new_y >= 0 and game_grid[new_y][new_x] != 0):
                            return False
            return True
        else:
            for row_index, row in enumerate(self.shape):
                for col_index, value in enumerate(row):
                    if value != 0:
                        new_x = pos[1] + col_index
                        new_y = pos[0] + row_index
                        if new_x < 0 or new_x > 9 or new_y > 19 or (new_y >= 0 and game_grid[new_y][new_x] != 0):
                            return False
            return True
    
    # locks in current position into the main game grid.
    def lockin(self):
        for row_index, row in enumerate(self.shape):
            for col_index, value in enumerate(row):
                if value != 0:
                    game_grid[self.position[0] + row_index][self.position[1] + col_index] = self.color
        # restets game if you reach the top
        if game_grid[0][4] or game_grid[0][5] or game_grid[0][3] or game_grid[0][6]:
            global state
            state = "loss"
            pygame.mixer.music.rewind()
        else:
            global justHeld, tetrorder_index
            justHeld = False
            tetrorder_index = bag_increment(tetrorder_index)
            self.__init__(tetromino_order[tetrorder_index])

    # drawing of tetronimoes is done seperately from placed grid, because doing them together was a nightmare
    def draw(self):
        for row_index, row in enumerate(self.shape):
            for col_index, value in enumerate(row):
                if value != 0:
                    pygame.draw.rect(screen, self.color, ((self.position[1] + col_index) * 25, (self.position[0] + row_index) * 25, 25, 25))

    # this function is mixed code from draw() and slam() to draw a ghost of where you will hard drop
    def draw_ghost(self):
        ghost_y = 0
        for i in range(19): 
            ghost_y += 1
            if not self.valid_position([ghost_y, self.position[1]]):
                ghost_y -= 1
                break
        for row_index, row in enumerate(self.shape):
            for col_index, value in enumerate(row):
                if value != 0:
                    pygame.draw.rect(screen, "gray", ((self.position[1] + col_index) * 25, (ghost_y + row_index) * 25, 25, 25))

    # resets every variable used for game
    def reset_game(self):
        global game_grid, score, held, justHeld, lines_cleared, level
        game_grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        score = 0
        held = None
        justHeld = False
        lines_cleared = 0
        level = 1

# grid used for game
#!!!! THE GRID IS IN Y, X !!!! [0][1] IS 1 TILE RIGHT OF THE TOP LEFT!!!
game_grid = [
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  ]

# sets up psuedo-random "bag shuffle". prevents you from getting the same piece over and over
tetromino_order = ['O', 'I', 'Z', 'S', 'J', 'L', 'T']
shuffle(tetromino_order)
tetrorder_index = 0

def bag_increment(tetrorder_index):
    if tetrorder_index != 6:
        return tetrorder_index + 1
    else:
        shuffle(tetromino_order)
        return 0

clock = pygame.time.Clock()
time = 0
movement_timer = 0
tetro =  Tetromino(tetromino_order[tetrorder_index])
interval = 30
score = 0
held = None
justHeld = False
lines_cleared = 0
level = 1

# set up text
font = pygame.font.Font('freesansbold.ttf', 20)
title_font = pygame.font.Font('freesansbold.ttf', 58)
title_text = title_font.render("TETRIS", True, "white")
explain_text1 = font.render("Press Enter to start", True, "white")
explain_text2 = font.render("Move block with ASD", True, "white")
explain_text3 = font.render("QE to rotate", True, "white")
explain_text4 = font.render("LSHIFT to hold", True, "white")
explain_text5 = font.render("SPACE to drop", True, "white")
gameover_text1 = title_font.render("Game", True, "white")
gameover_text2 = title_font.render("Over!", True, "white")

# set up music
pygame.mixer.music.load('main_theme.mp3')
pygame.mixer.music.play(-1)

# main game loop
while running:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # some inputs r done here instead of with the "keys" variable i use later bc
        # these are for ones that aren't held down, just the inital press.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT and state == "playing":
                # the purpose of justHeld is to prevent hold spamming. it gets set to False in Tetronimo.lockin()
                if not justHeld:
                    if held:
                        temp = tetro.shapecolor
                        tetro.__init__(held)
                        held = temp
                    else:
                        held = tetro.shapecolor
                        tetro.__init__()
                    justHeld = True
            if event.key == pygame.K_RETURN and (state == "title" or state == "loss"):
                tetro.reset_game()
                state = "playing"
            if event.key == pygame.K_q and state == "playing":
                tetro.rotate("left")
            elif event.key == pygame.K_e and state == "playing":
                tetro.rotate("right")
            if event.key == pygame.K_SPACE and state == "playing":
                tetro.slam()
            if event.key == pygame.K_a and state == "playing":
                tetro.movement("left")
                # this is neccessary to make movement not so finicky and sensitive
                movement_timer = 0
            elif event.key == pygame.K_d and state == "playing":
                tetro.movement("right")
                movement_timer = 0

    time += 1
    movement_timer += 1

    if lines_cleared != 0:
        # every 10 lines your level increases
        level = (lines_cleared + 10) // 10

    if state == "playing":
        # play music
        pygame.mixer.music.unpause()

        # updates and draws text
        scoretext = font.render(f"Score: {score}", True, "white")
        heldtext = font.render(f"Held:", True, "white")
        screen.blit(scoretext, (15, 540))
        screen.blit(heldtext, (160, 520))
        held_render_pos = [160, 540]
        
        # slightly tweaked code from Tetronimo.draw() to render the block you're holding
        if held:
            for row_index, row in enumerate(tetrominoes[held]['shape']):
                    for col_index, value in enumerate(row):
                        if value != 0:
                            pygame.draw.rect(screen, tetrominoes[held]['color'], (held_render_pos[0] + (col_index * 25), held_render_pos[1] + (row_index * 25), 25, 25))

        # basically multiplies the index by 25 to draw a 25 by 25 square at the appropriate place
        # relative to the grid. i found enumerate on google to have access to both the indices and values
        for row_index, row in enumerate(game_grid):
            for col_index, value in enumerate(row):
                pygame.draw.rect(screen, value, (col_index * 25, row_index * 25, 25, 25))

        # checks every line and clears if full
        for row_index, row in enumerate(game_grid):
            full_count = 0
            for value in row:
                if value != 0:
                    full_count += 1
            if full_count == 10:
                for i in range(10):
                    game_grid[row_index][i] = 0
                # level is dictated by how many lines you've cleared which increases score and makes the game go faster
                score += 100 * level
                lines_cleared += 1

                # brings everything down 1 tile after clearing row
                for i in range(row_index, 0, -1):
                    game_grid[i] = game_grid[i-1]
                game_grid[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        keys = pygame.key.get_pressed()

        # gravity falls faster based on level
        if level <= 10:
            base_gravity = 35 - (3*level)

        # makes the block fall faster if s is held
        if keys[pygame.K_s]:
            gravity_interval = 5
        # mega slow down for debugging
        elif keys[pygame.K_p]:
            gravity_interval = 120
        else:
            gravity_interval = base_gravity

        movement_interval = 7

        tetro.draw_ghost()
        tetro.draw()

        if keys[pygame.K_a]:
            if movement_timer % movement_interval == 0:
                tetro.movement("left")
        elif keys[pygame.K_d]:
            if movement_timer % movement_interval == 0:
                tetro.movement("right")

        # the interval dictactes how often the blocks move down a tile or are allowed to move
        if time % gravity_interval == 0:
            tetro.gravity()

        # generates grid lines for visibility
        for row_index, row in enumerate(game_grid):
            for col_index, value in enumerate(row):
                pygame.draw.line(screen, "gray", [col_index * 25, 0], [col_index * 25, 500])
                pygame.draw.line(screen, "gray", [0, row_index * 25], [250, row_index * 25])

        # two extra lines that dont get drawn in the for loop
        pygame.draw.line(screen, "gray", [0, 499], [250, 499])
        pygame.draw.line(screen, "gray", [249, 0], [249, 500])
    elif state == "title":
        pygame.mixer.music.pause()
        screen.blit(title_text, (15, 200))
        screen.blit(explain_text1, (30, 300))
        screen.blit(explain_text2, (30, 325))
        screen.blit(explain_text3, (30, 350))
        screen.blit(explain_text4, (30, 375))
        screen.blit(explain_text5, (30, 400))
    elif state == "loss":
        pygame.mixer.music.pause()
        scoretext = font.render(f"Score: {score}", True, "white")
        screen.blit(gameover_text1, (15, 175))
        screen.blit(gameover_text2, (80, 225))
        screen.blit(scoretext, (80, 300))
        screen.blit(explain_text1, (30, 325))
    # update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()