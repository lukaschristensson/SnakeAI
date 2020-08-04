import tkinter as tk
import numpy as np
import SnakeGame.GameGenerator as GameGenerator
import time


class NetSnakeViewer(tk.Tk):
    def __init__(self, cellSize: int, netWindowSize: [int, int], trainer):
        super().__init__()
        self.showVisionRays = False
        self.cellSize = cellSize
        self.trainer = trainer
        self.netSnake = self.trainer.bestSnake
        self.generator = GameGenerator.GameGenerator([10, 10], 4, 50)
        self.generator.startingSize = 4
        self.game = self.generator.newGame()
        self.mps = 3
        self._root().resizable = False
        self.feedBackLabel = tk.Label(self, font="Helvetica, 15")
        self.feedBackLabel.grid(row=0, column=0, columnspan=2)
        self.feedBackLabelText: [str] = []
        self.gameCanvas = tk.Canvas(self,
                                    width=self.generator.boardSize[0] * self.cellSize,
                                    height=self.generator.boardSize[1] * self.cellSize,
                                    bd=0, highlightthickness=0)
        self.gameCanvas.grid(row=1, column=0)

        self.gameCanvas.focus_force()

        self.netCanvas = tk.Canvas(self,
                                   width=netWindowSize[0],
                                   height=netWindowSize[1],
                                   bd=0, highlightthickness=0)
        self.netCanvas.grid(row=1, column=1)

        def focusCanvas(event):
            self.gameCanvas.focus_force()

        def increaseMPS(event):
            if self.mps < 999:
                self.mps += 1
                self.feedBackLabelText[1] = "Max mps: " + str(self.mps)

        def decreaseMPS(event):
            if self.mps > 0:
                self.mps -= 1
                self.feedBackLabelText[1] = "Max mps: " + str(self.mps)

        self.gameCanvas.bind("<Up>", increaseMPS)
        self.gameCanvas.bind("<Down>", decreaseMPS)
        self.bind("Button-1", focusCanvas)

        def raycontrol(event):
            self.showVisionRays = not self.showVisionRays

        self.gameCanvas.bind("<space>", raycontrol)

    def start(self):
        self.feedBackLabelText = []
        self.feedBackLabelText.append("Score: 0")
        self.feedBackLabelText.append("Max mps: " + str(self.mps))
        self.feedBackLabelText.append("Generation: " + str(self.trainer.generation))
        self.after(1, self.advanceFrame)

    lastFrame = 0
    gameOver = False
    gameResult = ""
    waitUntil = 0
    bufferGenerationString = ""

    def advanceFrame(self) -> (bool, str):
        if self.waitUntil < time.time():
            if self.bufferGenerationString != "":
                self.feedBackLabelText[2] = self.bufferGenerationString
                self.bufferGenerationString = ""
            if time.time() - self.lastFrame > 1 / self.mps:
                res = self.game.move()
                self.gameOver = not res[0]
                self.gameResult = res[1]
                moveData = self.netSnake.getMoveAndActivation(self.game)
                self.game.currentDirection = moveData[0]
                self.drawNet(moveData[1])
                self.lastFrame = time.time()

            self.gameCanvas.delete(tk.ALL)
            self.gameCanvas.create_rectangle(0, 0, self.gameCanvas.winfo_width(), self.gameCanvas.winfo_height(),
                                             fill='#444', outline="")
            self.drawSnake()
            self.drawApple()
            if self.showVisionRays:
                self.drawRays()

        self.updateFeedbackLabel()

        if not self.gameOver:
            self.after(1, self.advanceFrame)
        else:
            self.netSnake = self.trainer.bestSnake
            self.bufferGenerationString = "Generation: " + str(self.trainer.generation)
            self.game = self.generator.newGame()
            self.gameCanvas.create_text(
                (self.cellSize * self.generator.boardSize[0] / 2, self.cellSize * self.generator.boardSize[1] / 2),
                text=self.gameResult,
                font=("Helvetica", 20),
                anchor=tk.CENTER,
                fill='white'
            )
            self.gameOver = False
            self.waitUntil = time.time() + 1.2
            self.after(1, self.advanceFrame())

    def updateFeedbackLabel(self):
        finalString = ""
        for s in self.feedBackLabelText:
            finalString += s + "||"
        finalString = finalString[:len(finalString) - 2]
        self.feedBackLabel.configure(text=finalString)

    def drawNet(self, activations):
        self.netCanvas.delete(tk.ALL)
        # make the background gray
        self.netCanvas.create_rectangle(0, 0, self.netCanvas.winfo_width(), self.netCanvas.winfo_height(), fill='#aaa',
                                        outline="")

        # amount of layers in the net
        layerCount = len(activations)

        # calculate largest column for the orb size
        largestColumn = 0
        for i in range(len(activations)):
            if len(activations[i]) > largestColumn:
                largestColumn = len(activations[i])

        # all layers have the same x offset, calculated here
        xPadding = 40
        layerXPos = (self.netCanvas.winfo_width() - xPadding * 2) / (layerCount - 1)

        # largest y offset found to create the largest orb size possible while still fitting in all the orbs in every layer
        largestLayerYPos = self.netCanvas.winfo_height() / (largestColumn + 1)
        orbsSize = min(layerXPos, largestLayerYPos) / 1.1

        layerYPos = []
        # get the y offset for each orb in layer i to space them evenly
        for i in range(layerCount):
            layerYPos.append(self.netCanvas.winfo_height() / (len(activations[i]) + 1))

        getOrbPos = lambda layer, weightIndex: \
            (xPadding + layer * layerXPos - (orbsSize / 2),
             self.netCanvas.winfo_height() - ((weightIndex + 1) * layerYPos[layer]))

        # draw weights
        for tIndex in range(len(self.netSnake.net.thetas)):
            t = self.netSnake.net.thetas[tIndex].copy()
            maxWeight = np.max(np.abs(t))
            for i in range(t.shape[0]):
                for j in range(t.shape[1]):
                    posOfFromOrb = getOrbPos(tIndex, i)
                    posOfToOrb = getOrbPos(tIndex + 1, j)
                    weightColor = int(np.round(255 * (t[i, j] / maxWeight)))

                    if weightColor < 0:
                        self.netCanvas.create_line(posOfFromOrb[0], posOfFromOrb[1], posOfToOrb[0], posOfToOrb[1],
                                                   width=1,
                                                   fill=NetSnakeViewer.ColorFromrgb(
                                                       (255, 255 + weightColor, 255 + weightColor)))
                    else:
                        self.netCanvas.create_line(posOfFromOrb[0], posOfFromOrb[1], posOfToOrb[0], posOfToOrb[1],
                                                   width=1,
                                                   fill=NetSnakeViewer.ColorFromrgb(
                                                       (255 - weightColor, 255, 255 - weightColor)))
        # draw activation orbs
        for i in range(layerCount):
            for j in range(len(activations[i])):
                # activationStrength is calculated as a percentage of the largest activation
                nodeActivationStrength = int(np.round(255 * (activations[i][j] / np.max(activations[i]))))
                orbPos = getOrbPos(i, j)
                # if it's the highest up node it gets blue to indicate the fact that it's a bias
                if j == len(activations[i]) - 1 and i != layerCount - 1:
                    NetSnakeViewer.drawCircle(
                        (orbPos[0] - orbsSize / 2, orbPos[1] - orbsSize / 2),
                        NetSnakeViewer.ColorFromrgb((0, 0, nodeActivationStrength)),
                        orbsSize, self.netCanvas)
                else:
                    NetSnakeViewer.drawCircle(
                        (orbPos[0] - orbsSize / 2, orbPos[1] - orbsSize / 2),
                        NetSnakeViewer.ColorFromrgb((nodeActivationStrength, 0, nodeActivationStrength)),
                        orbsSize, self.netCanvas)

    def drawSnake(self):
        for p in self.game.tail:
            self.drawSnakeCircle(p, '#20cb53')
        self.drawSnakeCircle(self.game.head, '#116e2d')

    def drawApple(self):
        self.drawSnakeCircle(self.game.apple, 'red')

    def drawRays(self):
        vectors = [[0, -1],
                   [1, -1],
                   [1, 0],
                   [1, 1],
                   [0, 1],
                   [-1, 1],
                   [-1, 0],
                   [-1, -1]
                   ]

        def distance(p1, p2) -> float:
            return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

        for vec in vectors:
            tileCursor = self.game.head
            nonFound = True
            fill = ""
            while nonFound:
                tileCursor = [tileCursor[0] + vec[0], tileCursor[1] + vec[1]]
                if tileCursor in self.game.tail:
                    fill = "green"
                    nonFound = False
                elif not (
                        0 <= tileCursor[0] < self.game.boardSize[0] and
                        0 <= tileCursor[1] < self.game.boardSize[1]
                ):
                    fill = "black"
                    nonFound = False
                elif tileCursor == self.game.apple:
                    fill = "red"
                    nonFound = False
            dist = distance(tileCursor, self.game.head)
            self.gameCanvas.create_line(
                self.game.head[0] * self.cellSize + self.cellSize / 2,
                self.game.head[1] * self.cellSize + self.cellSize / 2,
                tileCursor[0] * self.cellSize + self.cellSize / 2, tileCursor[1] * self.cellSize + self.cellSize / 2,
                fill=fill, width=2 * max(self.game.boardSize[0], self.game.boardSize[1]) / (2 * dist)
            )

    @staticmethod
    def drawCircle(p: [int, int], fill: str, size: int, canvas: tk.Canvas):
        canvas.create_oval(p[0], p[1],
                           p[0] + size, p[1] + size,
                           fill=fill)

    @staticmethod
    def ColorFromrgb(rgb):
        return "#%02x%02x%02x" % rgb

    def drawSnakeCircle(self, p: [int, int], fill: str):
        self.gameCanvas.create_oval(p[0] * self.cellSize, p[1] * self.cellSize,
                                    (p[0] + 1) * self.cellSize, (p[1] + 1) * self.cellSize,
                                    fill=fill)
