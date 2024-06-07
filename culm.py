import pygame

# set up pygame stuff
pygame.init()
screen = pygame.display.set_mode((250, 500))

# run until user asks to quit
running = True

# i dont really know classes that well I just wanted to have these variables in 1 "container" I guess.
class MovableTile:
    location = [0, 4]
    past = [0, 4]
    color = 1

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
block = MovableTile()
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
                pygame.draw.rect(screen, "blue", (col_index * 25, row_index * 25, 25, 25))
            elif value == 3:
                pygame.draw.rect(screen, "red", (col_index * 25, row_index * 25, 25, 25))
            elif value == 4:
                pygame.draw.rect(screen, "green", (col_index * 25, row_index * 25, 25, 25))
            elif value == 5:
                pygame.draw.rect(screen, "orange", (col_index * 25, row_index * 25, 25, 25))
            elif value == 6:
                pygame.draw.rect(screen, "pink", (col_index * 25, row_index * 25, 25, 25))
            elif value == 7:
                pygame.draw.rect(screen, "purple", (col_index * 25, row_index * 25, 25, 25))

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

        # i have zero clue why this works but it does so im not gonna touch it
        else:
            block.past[1] = block.location[1]

        # reset the block's last location to empty
        game_grid[block.past[0]][block.past[1]] = 0
        print(f"BLOCK PAST X, Y: {block.past[1]},{block.past[0]}")

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

    # update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()