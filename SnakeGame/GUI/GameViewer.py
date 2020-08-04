import SnakeGame.SnakeEngine.Snake as SnakeGame
import SnakeGame.SnakeEngine.SnakeController as Controller
import numpy as np
import tkinter as tk


class GameViewer(tk.Tk):

    def __init__(self, cellSize: int, snakeGame: SnakeGame, controller: Controller.SnakeController):
        super().__init__()
        self.cellSize = cellSize
        self.snakeGame = snakeGame
        self.controller = controller
        self.mps = 3
        self.feedBackLabel = tk.Label(self, font="Helvetica, 15")
        self.feedBackLabel.grid(row=0)
        self.feedBackLabelText: [str] = []
        self.canvas = tk.Canvas(self,
                                width=self.snakeGame.boardSize[0] * self.cellSize,
                                height=self.snakeGame.boardSize[1] * self.cellSize,
                                bd=0, highlightthickness=0)
        self.canvas.grid(row=1)

        self.canvas.focus_force()

        def focusCanvas(event):
            self.canvas.focus_force()

        def increaseMPS(event):
            if self.mps < 999:
                self.mps += 1
                self.feedBackLabelText[1] = "Max mps: " + str(self.mps)

        def decreaseMPS(event):
            if self.mps > 2:
                self.mps -= 1
                self.feedBackLabelText[1] = "Max mps: " + str(self.mps)

        self.canvas.bind("<Up>", increaseMPS)
        self.canvas.bind("<Down>", decreaseMPS)
        self.bind("Button-1", focusCanvas)

    def start(self):
        self.feedBackLabelText.append("Score: 0")
        self.feedBackLabelText.append("Max mps: " + str(self.mps))
        self.after(1, self.advanceFrame)

    def advanceFrame(self) -> (bool, str):
        self.snakeGame.currentDirection = self.controller.getMove(self.snakeGame)
        res = self.snakeGame.move()
        self.canvas.delete(tk.ALL)
        self.drawSnake()
        self.drawApple()
        self.updateFeedbackLabel()
        if res[0]:
            self.after(int(np.floor(1000 / self.mps)), self.advanceFrame)
        else:
            print(res[1])

    def updateFeedbackLabel(self):
        finalString = ""
        for s in self.feedBackLabelText:
            finalString += s + "||"
        finalString = finalString[:len(finalString) - 2]
        self.feedBackLabel.configure(text=finalString)

    def drawSnake(self):
        for p in self.snakeGame.tail:
            self.drawCircle(p, '#20cb53')
        self.drawCircle(self.snakeGame.head, '#116e2d')

    def drawApple(self):
        self.drawCircle(self.snakeGame.apple, 'red')

    def drawCircle(self, p: [int, int], fill: str):
        self.canvas.create_oval(p[0] * self.cellSize, p[1] * self.cellSize,
                                (p[0] + 1) * self.cellSize, (p[1] + 1) * self.cellSize,
                                fill=fill)
