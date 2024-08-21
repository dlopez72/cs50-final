# Tetris for Two
#### Video Demo:  <URL HERE>
#### Description: WIP
Tetris for a Two is a multiplayer pygame recreation of the game "Tetris" created originally by Alexey Pajitnov. This recreation is for two local players, and you both share the oncoming pieces.

I chose to make my recreation of Tetris in pygame for a few reasons.
Firstly, I am familiar with Python as much of the CS50 curriculum uses python. Secondly, Python is relatively simple syntax-wise, meaning that I don’t have to worry about making simple syntax errors, and can instead focus on functionality. Finally, when it comes to game development Pygame doesn’t have as much built in functionality as game engines such as unity, unreal engine and Godot. This means that I can focus more on practicing my coding abilities, and less on using built in engine features.

There are two classes in the code, one for the Player which was added when I turned the game into a local multiplayer game, and a Tetromino class. This is my first time using classes, and while I did find them confusing to learn through YouTube tutorials I felt that they were necessary because Tetrominoes are constantly being created, meaning that the Tetromino can call `self.__init__` on itself once it locks in, which will bring the “playing Tetromino” back to the top with a new set of attributes. I also wanted to have classes for players because when I implemented a second player, I figured it was a convenient way of not having to rewrite all the code I had already written for the first player.

The game also features a “bag shuffle” where instead of the next Tetromino being selected randomly, a bag of each different Tetromino is shuffled and then picked from. This is commonly used in official Tetris games, as it prevents the player from getting the same Tetromino more than twice in a row (at the end of the first bag and the beginning of the second bag). The choice was also made to have both players share the oncoming Tetrominoes, as I felt this would add an interesting dynamic of trying to “steal” a useful piece before the other player can get to it. 

The gravity of the blocks operates on a tick-based system where an interval is set in the code, and every time the game time is divisible by that interval it calls on the Tetromino’s gravity function. This also makes it very easy to speed up time as the player clears more lines since you can just decrease the interval which will make ticks come by faster.

Tetris For Two uses a 2d list internally to handle the playing grid. Each piece is also its own 2d array, and a dictionary at the beginning associates every Tetromino name with a color and shape. Tetrominoes also aren’t added to the internal playing grid until they have been “locked in” (either hard dropped or reached the bottom). I had initially had each falling tile be separate, as well as in the playing grid as they fall, but I changed this after much headache because it made it very difficult to move four tiles as a Tetromino without them catching on each other since they kept “colliding” with their fellow tile.

