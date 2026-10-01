from game.game_engine import GameEngine

if __name__ == "__main__":
    game = GameEngine()
    try:
        game.run()
    finally:
        game.shutdown()
