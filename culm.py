import pygame
from random import randint

# TODO: refactor everything to make it easier to implement tetrominoes
# the past thing might need to be done on a tetromino level
# TODO: implement full block shapes instead of individiual tiles

# importantly for this code I made it that the shape of a tetromino directly
# corresponds to its color so here's the guide:
# 1 = YELLOW = O
# 2 = CYAN = I
# 3 = RED = Z
# 4 = GREEN = S
# 5 = ORANGE = L
# 6 = BLUE = J
# 7 = PURPLE = T

# set up pygame stuff
pygame.init()
screen = pygame.display.set_mode((250, 500))

# run until user asks to quit
running = True

# i dont really know classes that well I just wanted to have these variables in 1 "container" I guess.
class Tile:
    def __init__(self, location, past, color):
        self.location = location
        self.past = past
        self.color = color
    
class Tetromino:
    def __init__(self, shape, location):
        self.shape = shape
        self.location = location
        block1 = Tile(self.location, self.location, self.shape)

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
block =  Tile([0, 4], [0, 4], 2)
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
        interval = 5
    # mega slow down for debugging
    elif keys[pygame.K_p]:
        interval = 120
    else:
        interval = 30

    # the interval dictactes how often the blocks move down a tile
    if time % interval == 0:
        # move block left if a is pressed, also makes the past location one tile right of the block's new location
        if keys[pygame.K_a]:
            if block.location[1] != 0 and game_grid[block.location[0]][block.location[1] - 1] == 0:
                block.location[1] -= 1
                block.past[1] = block.location[1] + 1
            else:
                block.past[1] = block.location[1]
        # same thing but for right side
        elif keys[pygame.K_d]:
            if block.location[1] != 9 and game_grid[block.location[0]][block.location[1] + 1] == 0:
                block.location[1] += 1
                block.past[1] = block.location[1] - 1
            else:
                block.past[1] = block.location[1]

        # if neither a or d aren't being touched it knows that it's last x location
        # has to be the same
        else:
            block.past[1] = block.location[1]

        # reset the block's last location to empty
        game_grid[block.past[0]][block.past[1]] = 0

        # checks collision below to allow block to go down
        game_grid[block.location[0]][block.location[1]] = block.color
        if block.location[0] != 19 and game_grid[block.location[0] + 1][block.location[1]] == 0:
            
            block.location[0] += 1
            if block.location[0] != 0:
                block.past[0] = block.location[0] - 1
        else:
            # keeps the current block location as filled while bringing the block back to the beginning
            block.location = [0, 4]
            block.past = [0, 4]
            block.color = randint(1, 7)

    # update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()