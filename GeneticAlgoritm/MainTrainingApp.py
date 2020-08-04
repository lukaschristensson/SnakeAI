import SnakeGame.GUI.NetSnakeViewer as Viewer
import GeneticAlgoritm.GeneticTrainer as Trainer
import threading


if __name__ == '__main__':
    trainer = Trainer.GeneticTrainer()
    viewer = Viewer.NetSnakeViewer(40, [700, 700], trainer)
    t = threading.Thread(target=trainer.startTraining)
    t.setDaemon(True)
    t.start()
    viewer.start()
    viewer.mainloop()
