import pygame

#TODO: Fix bug where block duplicates when you hold a or d
#TODO: Fix bug where block can merge with blocks sideways AKA add sideways collision
#TODO: maybe use classes better? not 100 percent sure on that one.

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
#!!!! THE GRID IS IN Y, X !!!!
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

    # the 30 dictactes how often the game updates
    if time % 30 == 0:
        # move block left if a is pressed, also makes the past location 1 right of the block's new location
        if keys[pygame.K_a]:
            if block.location[1] != 0:
                block.location[1] -= 1
                block.past[1] = block.location[1] + 1
        # same thing but for right side
        elif keys[pygame.K_d]:
            if block.location[1] != 9:
                block.location[1] += 1
                block.past[1] = block.location[1] - 1
        else:
            # i have zero clue why this works but it does so im not gonna touch it
            block.past[1] = block.location[1]

        # reset the block's last location to empty
        game_grid[block.past[0]][block.past[1]] = 0

        game_grid[block.location[0]][block.location[1]] = block.color
        if block.location[0] != 19 and (game_grid[block.location[0] + 1][block.location[1]]) == 0:
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