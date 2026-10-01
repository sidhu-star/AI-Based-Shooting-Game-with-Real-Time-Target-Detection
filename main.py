from game import Game

if __name__ == '__main__':
    app = Game()
    try:
        app.run()
    finally:
        app.close()
