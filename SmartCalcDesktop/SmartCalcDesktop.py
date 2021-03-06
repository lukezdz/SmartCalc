import os
from PIL import ImageTk, Image, ImageDraw
import PIL
from tkinter import *
from tkinter import messagebox
from tkinter.colorchooser import askcolor
import threading
from Engine import Engine
from Calc import Calc


class SmartCalcDesktop:
    PEN_SIZE = 5.0
    ERASER_SIZE = 15.0
    DEFAULT_COLOR = 'black'
    WIDTH = 800
    HEIGHT = 300

    def __init__(self):
        self.root = Tk()

        self.root.winfo_toplevel().title("SmartCalc Desktop")
        self.root.iconbitmap('data/SmartCalcDesktop.ico')

        self.evaluate_button = Button(self.root, text='Evaluate', command=self.evaluate,)
        self.evaluate_button.grid(row=0, column=0, sticky=N+S+E+W)
        
        self.clear_button = Button(self.root, text='Clear', command=self.clear)
        self.clear_button.grid(row=0, column=1, sticky=N+S+E+W)

        self.erase_button = Button(self.root, text='Erase', command=self.use_eraser)
        self.erase_button.grid(row=0, column=3, sticky=N+S+E+W)

        self.info_button = Button(self.root, text='About', command=self.info)

        self.info_button.grid(row=0, column = 9, sticky=N+S+E+W)

        self.editor_label = Label(self.root, text='Handwritten Editor')
        self.editor_label.grid(row=1, columnspan=10, sticky=W)

        self.c = Canvas(self.root, bg='white', width=self.WIDTH, height=self.HEIGHT, cursor='pencil')
        self.c.grid(row=2, columnspan=10)

        self.can_evaluate = False
        self.evaluate_button.config(state=DISABLED)

        self.output_label = Label(self.root, text='Results')
        self.output_label.grid(row=3, columnspan=10, sticky=W)

        self.scrollbar = Scrollbar(self.root)
        self.scrollbar.grid(row=4, column=9, sticky=N+S+E)

        self.output = Text(self.root)
        self.output.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.output.yview)
        self.output.grid(row=4, columnspan=9, sticky=N+S+E+W)

        self.image = PIL.Image.new("RGB", (self.WIDTH, self.HEIGHT), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)

        self.setup()
        self.root.after(100, self.init_engine)
        self.output.insert(END, "Loading neural network model...\n")
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
        self.engine = Engine()
        self.output.insert(END, "Model successfully loaded!\n")
        self.can_evaluate = True
        self.evaluate_button.config(state=NORMAL)

    def use_eraser(self):
        if self.eraser_on:
            self.erase_button.config(relief=RAISED)
            self.eraser_on = False
            self.line_width = self.PEN_SIZE
            self.c.config(cursor='pencil')
        else:
            self.erase_button.config(relief=SUNKEN)
            self.eraser_on = True
            self.line_width = self.ERASER_SIZE
            self.c.config(cursor='circle')

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

    def info(self):
        title = "About SmartCalc Desktop"
        message = "SmartCalc Desktop can recognize following characters:\n\n\t0 1 2 3 4 5 6 7 8 9 a b c d e + - * / ( )\n\nAfter it recognizes handwritten input, it calculates an answer to your math problem and displays everything in the Results textbox below.\n\n\nTip:\nIn the Handwriting Editor you can draw and erase (toggle Erase button), clear whole canvas (Clear button) and evaluate what is in the canvas (Evaluate button)\n\n\nBeta feature:\nSmartCalc Desktop is *sometimes* able to recognize also = character and solve more complicated equations. Just make sure to have space between two vertical lines in =\n\n\nAuthors:\n\tPawel Lesniewski\n\tLukasz Skold\n\tLukasz Zdziarski"
        messagebox.showinfo(title, message)

    def evaluate(self):
        if not self.can_evaluate:
            return None
        if not os.path.exists("temp"):
            os.mkdir("temp")

        filename = "temp\\temp.jpg"
        self.image.save(filename)
        # evaluationThread = threading.Thread(target=self.evaluation_handler)
        # evaluationThread.start()
        self.evaluation_handler()

    def GetNormalizedEquation(self, equation):
        i = 0
        while i <= len(equation) - 1:
            if equation[i] == "-" and equation[i+1] == "-":
                equation = equation[:i] + equation[i+1:]
                equation = equation[:i] + "=" + equation[i+1:]
                break
            i += 1
        return equation

    def evaluation_handler(self):
        equation = self.engine.get_equation()
        calculator = Calc(equation)
        status, result, char, newEqu = calculator.GetResult()

        if status == "SUCCESS_EVAL":
            solved_equation = newEqu + " = " + str(result) + "\n"
            self.output.insert(END, solved_equation)

        elif status == "SUCCESS_UNKNOWN":
            solved_equation = "For: " + self.GetNormalizedEquation(equation) + "\n" + char + " = " + str(result) + " \n"
            self.output.insert(END, solved_equation)

        else:
            if equation == "":
                equation = "EMPTY"
            self.output.insert(END, "Incorrect equation! [DEBUG INFO: "+ equation + "] \n")


if __name__ == '__main__':
    SmartCalcDesktop()
