from app import Game

if __name__ == '__main__':
    game = Game()
    try:
        game.run()
    finally:
        game.close()
