# Run this file to run the game!
import src.game
import src.utility

src.utility.setup_logger()

game = src.game.Game()
game.run()