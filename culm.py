import pygame
from random import randint

# TODO: redo the entire past system it's messing things up & confusing
# TODO: implement full block shapes instead of individiual tiles

# importantly for this code I made it that the shape of a tetromino directly
# corresponds to its color so here's the guide:
# 1 = YELLOW = O block
# 2 = CYAN = I block
# 3 = RED = Z block
# 4 = GREEN = S block
# 5 = ORANGE = L block
# 6 = BLUE = J block
# 7 = PURPLE = T block

# set up pygame stuff
pygame.init()
screen = pygame.display.set_mode((250, 500))

# run until user asks to quit
running = True

class Tile:
    def __init__(self, location, past, color, attached):
        self.location = location
        self.past = past
        self.color = color
        self.attached = attached

    def movement(self, keys):
        # move block left if a is pressed, also makes the past location one tile right of the block's new location
        if keys[pygame.K_a]:
            if self.location[1] != 0 and game_grid[self.location[0]][self.location[1] - 1] == 0:
                self.location[1] -= 1
                self.past[1] = self.location[1] + 1
            else:
                self.past[1] = self.location[1]
        # same thing but for right side
        elif keys[pygame.K_d]:
            if self.location[1] != 9 and game_grid[self.location[0]][self.location[1] + 1] == 0:
                self.location[1] += 1
                self.past[1] = self.location[1] - 1
            else:
                self.past[1] = self.location[1]
        # if neither a or d are being touched it knows that it's last x location
        # has to be the same
        else:
            self.past[1] = self.location[1]

    def gravity(self):
        if self.location[0] != 19 and (game_grid[self.location[0] + 1][self.location[1]] == 0 or self.attached[0].location[0] == self.location[0]+1 or self.attached[1].location[0] == self.location[0]+1 or self.attached[2].location[0] == self.location[0]+1):
            self.location[0] += 1
            if self.location[0] != 0:
                self.past[0] = self.location[0] - 1
        else:
            # keeps the current block location as filled while bringing the block back to the beginning
            self.location = [0, 4]
            self.past = [0, 4]
            self.color = randint(1, 7)

    def update_grid(self):
        # reset the block's last location to empty
        game_grid[self.past[0]][self.past[1]] = 0

        # set grid to block location
        game_grid[self.location[0]][self.location[1]] = self.color

    
class Tetromino:
    def __init__(self, location, shape):
        self.shape = shape
        self.location = location
        self.block1 = Tile(self.location, self.location, self.shape, [])
        if self.shape == 1:
            self.block2 = Tile([self.location[0], self.location[1]+1], [self.location[0], self.location[1]+1], self.shape, [])
            self.block3 = Tile([self.location[0]+1, self.location[1]], [self.location[0]+1, self.location[1]], self.shape, [])
            self.block4 = Tile([self.location[0]+1, self.location[1]+1], [self.location[0]+1, self.location[1]+1], self.shape, [])
            self.block1.attached = [self.block2, self.block3, self.block4]
            self.block2.attached = [self.block1, self.block3, self.block4]
            self.block3.attached = [self.block1, self.block2, self.block4]
            self.block4.attached = [self.block1, self.block2, self.block3]

    def movement(self, keys):
        self.block1.movement(keys)
        self.block2.movement(keys)
        self.block3.movement(keys)
        self.block4.movement(keys)

    def gravity(self):
        self.block1.gravity()
        self.block2.gravity()
        self.block3.gravity()
        self.block4.gravity()

    def update_grid(self):
        self.block1.update_grid()
        self.block2.update_grid()
        self.block3.update_grid()
        self.block4.update_grid()

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

clock = pygame.time.Clock()
time = 0
tetro =  Tile([0, 4], [0, 4], 1, [])
interval = 30

# main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    time += 1

    # basically multiplies the index by 25 to draw a 25 by 25 square at the appropriate place
    # relative to the grid. i found enumerate on google to have access to both the indices and values
    for row_index, row in enumerate(game_grid):
        for col_index, value in enumerate(row):
            if value == 1:
                pygame.draw.rect(screen, "yellow", (col_index * 25, row_index * 25, 25, 25))
            elif value == 2:
                pygame.draw.rect(screen, "cyan", (col_index * 25, row_index * 25, 25, 25))
            elif value == 3:
                pygame.draw.rect(screen, "red", (col_index * 25, row_index * 25, 25, 25))
            elif value == 4:
                pygame.draw.rect(screen, "green", (col_index * 25, row_index * 25, 25, 25))
            elif value == 5:
                pygame.draw.rect(screen, "orange", (col_index * 25, row_index * 25, 25, 25))
            elif value == 6:
                pygame.draw.rect(screen, "blue", (col_index * 25, row_index * 25, 25, 25))
            elif value == 7:
                pygame.draw.rect(screen, "purple", (col_index * 25, row_index * 25, 25, 25))

    full_count = 0

    # checks and clears line at bottom.
    for i in game_grid[19]:
        if i != 0:
            full_count += 1
    if full_count == 10:
        for i in range(10):
            game_grid[19][i] = 0

        # brings everything down 1 tile after clearing tile
        for i in range(19, 0, -1):
            game_grid[i] = game_grid[i-1]
        game_grid[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        

    keys = pygame.key.get_pressed()

    # makes the block fall faster if s is held
    if keys[pygame.K_s]:
        gravity_interval = 5
    # mega slow down for debugging
    elif keys[pygame.K_p]:
        gravity_interval = 120
    else:
        gravity_interval = 30

    # the interval dictactes how often the blocks move down a tile
    if time % gravity_interval == 0:
        tetro.movement(keys)
        tetro.update_grid()
        tetro.gravity()

    # update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()