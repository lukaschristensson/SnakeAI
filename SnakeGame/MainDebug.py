import SnakeGame.GUI.GameViewer as Viewer
import SnakeGame.SnakeEngine.Snake as Game
import SnakeGame.DebugController


if __name__ == '__main__':
    game = Game.Snake([5, 5], [10, 10], 30, 3)
    cont = SnakeGame.DebugController.DebugController()
    win = Viewer.GameViewer(40, game, cont)
    win.start()
    win.mainloop()
