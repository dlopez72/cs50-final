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
screen = pygame.display.set_mode((650, 600))
pygame.display.set_caption("CS50 Tetris")
state = "title"

# run until user asks to quit
running = True

class Tetromino:
    def __init__(self, player, shapecolor=None):
        # generates a random shapecolor if one isn't provided
        if not shapecolor:
            self.shapecolor = choice(list(tetrominoes.keys()))
        else:
            self.shapecolor = shapecolor
        # uses the dict to assign a color and shape to the main key
        self.color = tetrominoes[self.shapecolor]['color']
        self.shape = tetrominoes[self.shapecolor]['shape']
        self.position = [0, round(10 / 2) - round(len(self.shape[0]) / 2)]
        self.player = player

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
                        if new_x < 0 or new_x > 9 or new_y > 19 or (new_y >= 0 and self.player.grid[new_y][new_x] != 0):
                            return False
            return True
        else:
            for row_index, row in enumerate(self.shape):
                for col_index, value in enumerate(row):
                    if value != 0:
                        new_x = pos[1] + col_index
                        new_y = pos[0] + row_index
                        if new_x < 0 or new_x > 9 or new_y > 19 or (new_y >= 0 and self.player.grid[new_y][new_x] != 0):
                            return False
            return True
    
    # locks in current position into the main game grid.
    def lockin(self):
        for row_index, row in enumerate(self.shape):
            for col_index, value in enumerate(row):
                if value != 0:
                    self.player.grid[self.position[0] + row_index][self.position[1] + col_index] = self.color
        # restets game if you reach the top
        if self.player.grid[0][4] or self.player.grid[0][5] or self.player.grid[0][3] or self.player.grid[0][6]:
            global state, loser
            state = "loss"
            loser = self.player
            pygame.mixer.music.rewind()
        else:
            global tetromino_queue
            self.player.justHeld = False
            tetromino_queue = bag_increment()
            self.__init__(self.player, tetromino_queue[0])

    # drawing of tetronimoes is done seperately from placed grid, because doing them together was a nightmare
    def draw(self):
        for row_index, row in enumerate(self.shape):
            for col_index, value in enumerate(row):
                if value != 0:
                    pygame.draw.rect(screen, self.color, (((self.position[1] + col_index) * 25) + self.player.offset, (self.position[0] + row_index) * 25, 25, 25))

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
                    pygame.draw.rect(screen, "gray", (((self.position[1] + col_index) * 25) + self.player.offset, (ghost_y + row_index) * 25, 25, 25))

    # resets every variable used for game
    def reset_game(self):
        self.player.grid = [
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
        self.player.score = 0
        self.player.held = None
        self.player.justHeld = False
        self.player.lines_cleared = 0
        self.player.level = 1
        self.__init__(self.player, tetromino_queue[0])

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
tetromino_queue = []
tetromino_order = ['O', 'I', 'Z', 'S', 'J', 'L', 'T']
shuffle(tetromino_order)
tetromino_queue += tetromino_order
shuffle(tetromino_order)
tetromino_queue += tetromino_order

def bag_increment():
    tetromino_queue.pop(0)
    if len(tetromino_queue) <= 7:
        shuffle(tetromino_order)
        return tetromino_queue + tetromino_order
    return tetromino_queue

    
clock = pygame.time.Clock()
time = 0
movement_timer = 0
interval = 30

# player class includes tetronimo object and stats for your own game.
class Player:
    def __init__(self, tetromino_queue, grid, offset):
        self.tetro =  Tetromino(self, tetromino_queue[0])
        self.score = 0
        self.held = None
        self.justHeld = False
        self.lines_cleared = 0
        self.level = 1
        self.grid = grid
        self.offset = offset

p1 = Player(tetromino_queue, game_grid, 0)
p2 = Player(tetromino_queue, game_grid, 400)
players = [p1, p2]

# set up text
font = pygame.font.Font('freesansbold.ttf', 20)
title_font = pygame.font.Font('freesansbold.ttf', 58)
title_text = title_font.render("TETRIS", True, "white")
player_text1 = font.render("Player 1:", True, "white")
player_text2 = font.render("Player 2:", True, "white")
explain_text1 = font.render("Press Enter to start", True, "white")
explain_text2 = font.render("Move block with ASD", True, "white")
explain_text3 = font.render("QE to rotate", True, "white")
explain_text4 = font.render("LSHIFT to hold", True, "white")
explain_text5 = font.render("SPACE to drop", True, "white")
explain_text6 = font.render("Move block with arrow keys", True, "white")
explain_text7 = font.render("Up arrow & NumPad0 to rotate", True, "white")
explain_text8 = font.render("RSHIFT to hold", True, "white")
explain_text9 = font.render("RCTRL to drop", True, "white")
gameover_text1 = title_font.render("Winner: ", True, "white")
heldtext = font.render(f"Held:", True, "white")
nexttext = font.render(f"Next:", True, "white")

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
            if event.key == pygame.K_RETURN and (state == "title" or state == "loss"):
                p1.tetro.reset_game()
                p2.tetro.reset_game()
                state = "playing"
            if state == "playing":
                if event.key == pygame.K_LSHIFT:
                # the purpose of justHeld is to prevent hold spamming. it gets set to False in Tetronimo.lockin()
                    if not p1.justHeld:
                        if p1.held:
                            temp = p1.tetro.shapecolor
                            p1.tetro.__init__(p1, p1.held)
                            p1.held = temp
                        else:
                            p1.held = p1.tetro.shapecolor
                            tetromino_queue = bag_increment()
                            p1.tetro.__init__(p1, tetromino_queue[0])
                        p1.justHeld = True
                if event.key == pygame.K_RSHIFT:
                    if not p2.justHeld:
                        if p2.held:
                            temp = p2.tetro.shapecolor
                            p2.tetro.__init__(p2, p2.held)
                            p2.held = temp
                        else:
                            p2.held = p2.tetro.shapecolor
                            tetromino_queue = bag_increment()
                            p2.tetro.__init__(p2, tetromino_queue[0])
                        p2.justHeld = True
                if event.key == pygame.K_q:
                    p1.tetro.rotate("left")
                elif event.key == pygame.K_e:
                    p1.tetro.rotate("right")
                if event.key == pygame.K_UP:
                    p2.tetro.rotate("left")
                elif event.key == pygame.K_KP_0:
                    p2.tetro.rotate("right") 
                if event.key == pygame.K_SPACE:
                    p1.tetro.slam()
                if event.key == pygame.K_RCTRL:
                    p2.tetro.slam()
                if event.key == pygame.K_a:
                    p1.tetro.movement("left")
                    # this is neccessary to make movement not so finicky and sensitive
                    movement_timer = 0
                elif event.key == pygame.K_d:
                    p1.tetro.movement("right")
                    movement_timer = 0
                if event.key == pygame.K_LEFT:
                    p2.tetro.movement("left")
                    movement_timer = 0
                elif event.key == pygame.K_RIGHT:
                    p2.tetro.movement("right")
                    movement_timer = 0

    time += 1
    movement_timer += 1

    if state == "playing":
        # play music
        pygame.mixer.music.unpause()
        keys = pygame.key.get_pressed()

        # slightly tweaked code from Tetronimo.draw() to render the upcoming blocks
        screen.blit(nexttext, (260, 15))
        next_render_index = 0
        next_render_pos = [285, 40]
        for shape in tetromino_queue[1:5]:
            for row_index, row in enumerate(tetrominoes[shape]['shape']):
                for col_index, value in enumerate(row):
                    if value != 0:
                        pygame.draw.rect(screen, tetrominoes[shape]['color'], (next_render_pos[0] + (col_index * 25), (next_render_pos[1] + (70 * next_render_index)) + (row_index * 25), 25, 25))
            next_render_index += 1

        # this code is executed individually for each player
        for player_num, player in enumerate(players):
            # updates and draws text
            scoretext = font.render(f"Score: {player.score}", True, "white")
            screen.blit(scoretext, (15 + player.offset, 540))
            screen.blit(heldtext, (160 + player.offset, 520))
            held_render_pos = [160 + player.offset, 540]

            if player.lines_cleared != 0:
                # every 10 lines your level increases
                player.level = (player.lines_cleared + 10) // 10

            # slightly tweaked code from Tetronimo.draw() to render the block you're holding
            if player.held:
                for row_index, row in enumerate(tetrominoes[player.held]['shape']):
                        for col_index, value in enumerate(row):
                            if value != 0:
                                pygame.draw.rect(screen, tetrominoes[player.held]['color'], (held_render_pos[0] + (col_index * 25), held_render_pos[1] + (row_index * 25), 25, 25))

            # basically multiplies the index by 25 to draw a 25 by 25 square at the appropriate place
            # relative to the grid. i found enumerate on google to have access to both the indices and values
            for row_index, row in enumerate(player.grid):
                for col_index, value in enumerate(row):
                    pygame.draw.rect(screen, value, ((col_index * 25) + player.offset, row_index * 25, 25, 25))

            # checks every line and clears if full
            for row_index, row in enumerate(player.grid):
                full_count = 0
                for value in row:
                    if value != 0:
                        full_count += 1
                if full_count == 10:
                    for i in range(10):
                        player.grid[row_index][i] = 0
                    # level is dictated by how many lines you've cleared which increases score and makes the game go faster
                    player.score += 100 * player.level
                    player.lines_cleared += 1

                    # brings everything down 1 tile after clearing row
                    for i in range(row_index, 0, -1):
                        player.grid[i] = player.grid[i-1]
                    player.grid[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

            # gravity falls faster based on level, caps at level 10
            if player.level <= 10:
                base_gravity = 35 - (3*player.level)
            else:
                base_gravity = 5

            # makes the block fall faster if s or down arrow is held
            if player_num == 0:
                if keys[pygame.K_s]:
                    gravity_interval = 5
                # mega slow down for debugging
                elif keys[pygame.K_p]:
                    gravity_interval = 120
                else:
                    gravity_interval = base_gravity
            else:
                if keys[pygame.K_DOWN]:
                    gravity_interval = 5
                # mega slow down for debugging
                elif keys[pygame.K_p]:
                    gravity_interval = 120
                else:
                    gravity_interval = base_gravity

            movement_interval = 7

            player.tetro.draw_ghost()
            player.tetro.draw()

            if player_num == 0:
                if keys[pygame.K_a]:
                    if movement_timer % movement_interval == 0:
                        player.tetro.movement("left")
                elif keys[pygame.K_d]:
                    if movement_timer % movement_interval == 0:
                        player.tetro.movement("right")
            else:
                if keys[pygame.K_LEFT]:
                    if movement_timer % movement_interval == 0:
                        player.tetro.movement("left")
                elif keys[pygame.K_RIGHT]:
                    if movement_timer % movement_interval == 0:
                        player.tetro.movement("right")

            # the interval dictactes how often the blocks move down a tile or are allowed to move
            if time % gravity_interval == 0:
                player.tetro.gravity()

            # generates grid lines for visibility
            for row_index, row in enumerate(player.grid):
                for col_index, value in enumerate(row):
                    pygame.draw.line(screen, "gray", [(col_index * 25) + player.offset, 0], [(col_index * 25) + player.offset, 500])
                    pygame.draw.line(screen, "gray", [player.offset, row_index * 25], [250 + player.offset, row_index * 25])

        # four extra lines that dont get drawn in the for loop
        pygame.draw.line(screen, "gray", [0, 499], [250, 499])
        pygame.draw.line(screen, "gray", [249, 0], [249, 500])
        pygame.draw.line(screen, "gray", [400, 499], [650, 499])
        pygame.draw.line(screen, "gray", [649, 0], [649, 500])


    elif state == "title":
        pygame.mixer.music.pause()
        screen.blit(title_text, (210, 200))
        screen.blit(explain_text1, (225, 300))
        screen.blit(player_text1, (50, 355))
        screen.blit(explain_text2, (50, 380))
        screen.blit(explain_text3, (50, 405))
        screen.blit(explain_text4, (50, 430))
        screen.blit(explain_text5, (50, 455))
        screen.blit(player_text2, (350, 355))
        screen.blit(explain_text6, (350, 380))
        screen.blit(explain_text7, (350, 405))
        screen.blit(explain_text8, (350, 430))
        screen.blit(explain_text9, (350, 455))

    elif state == "loss":
        pygame.mixer.music.pause()
        screen.blit(gameover_text1, (165, 175))
        if loser == p1:
            gameover_text2 = title_font.render("Player 2!", True, "white")
            scoretext = font.render(f"Score: {p2.score}", True, "white")
        else:
            gameover_text2 = title_font.render("Player 1!", True, "white")
            scoretext = font.render(f"Score: {p1.score}", True, "white")
        screen.blit(gameover_text2, (230, 235))
        screen.blit(scoretext, (280, 300))
        screen.blit(explain_text1, (230, 325))
    # update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()