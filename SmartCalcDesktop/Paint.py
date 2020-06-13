from PIL import ImageTk, Image, ImageDraw
import PIL
from tkinter import *
from tkinter.colorchooser import askcolor
import threading
from Engine import Engine


class Paint(object):

    PEN_SIZE = 5.0
    ERASER_SIZE = 15.0
    DEFAULT_COLOR = 'black'
    WIDTH = 800
    HEIGHT = 300

    def __init__(self):
        self.root = Tk()

        self.evaluate_button = Button(self.root, text='Evaluate', command=self.evaluate)
        self.evaluate_button.grid(row=0, column=0)

        self.erase_button = Button(self.root, text='Erase', command=self.use_eraser)
        self.erase_button.grid(row=0, column=1)

        self.clear_button = Button(self.root, text='Clear', command=self.clear)
        self.clear_button.grid(row=0, column=3)

        self.c = Canvas(self.root, bg='white', width=self.WIDTH, height=self.HEIGHT)
        self.c.grid(row=1, columnspan=5)

        self.can_evaluate = False
        self.evaluate_button.config(relief=SUNKEN)

        self.scrollbar = Scrollbar(self.root)
        self.scrollbar.grid(row=2, column=4, sticky=N+S+E)
        self.output = Text(self.root)
        self.output.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.output.yview)
        self.output.grid(row=2, columnspan=4)

        self.image = PIL.Image.new("RGB", (self.WIDTH, self.HEIGHT), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)

        self.setup()
        self.root.after(100, self.init_engine)
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.PEN_SIZE
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def init_engine(self):
        self.output.insert(END, "Loading neural network model...\n")
        self.engine = Engine()
        self.output.insert(END, "Model successfully loaded!\n")
        self.can_evaluate = True
        self.evaluate_button.config(relief=RAISED)

    def use_eraser(self):
        if self.eraser_on:
            self.erase_button.config(relief=RAISED)
            self.eraser_on = False
            self.line_width = self.PEN_SIZE
        else:
            self.erase_button.config(relief=SUNKEN)
            self.eraser_on = True
            self.line_width = self.ERASER_SIZE

    def paint(self, event):
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
            self.draw.line([(self.old_x, self.old_y), (event.x, event.y)], fill=paint_color, width=int(self.line_width))
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def clear(self):
        self.c.delete('all')
        self.image = PIL.Image.new("RGB", (self.WIDTH, self.HEIGHT), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)

    def evaluate(self):
        if not self.can_evaluate:
            return None

        filename = "temp\\temp.jpg"
        self.image.save(filename)
        #evaluationThread = threading.Thread(target=self.evaluation_handler)
        #evaluationThread.start()
        self.evaluation_handler()

    def evaluation_handler(self):
        equation = self.engine.get_equation()
        # tu wywolaj liczenie rownania
        solved_equation = equation + "\n" # zmien zeby dawalo z wynikiem, zakoncz \n
        self.output.insert(END, solved_equation)


if __name__ == '__main__':
    Paint()