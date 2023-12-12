
import tkinter as tk
from tkinter import font as tkfont
from .addface import AddFace
from .recognizefaces import RecognizeFaces


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.geometry = ("400x400")
        tk.Tk.minsize=(400,400)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, AddFacePage, RecognizeFacePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def recognizeFaces(self):
        recognizeFaces = RecognizeFaces()
        recognizeFaces.recognize_faces()


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="KNN Facial Recognition", font=controller.title_font)
        label.pack(side="top", fill="x", padx=100, pady=50)

        button1 = tk.Button(self, text="Add Face",
                            command=lambda: controller.show_frame("AddFacePage"))
        button2 = tk.Button(self, text="Recognize Faces",
                            command= self.recognizeFaces)
        button1.pack(pady=20)
        button2.pack(pady=20)


class AddFacePage(tk.Frame):

    entry= tk.Entry()
    label = tk.Label()
    

    def didSubmit(self):
        string= self.entry.get()
        face = AddFace(string)
        success = face.capture_face()
        if (success):
            self.label.configure(text="Face was added succesfully. Add another?")
        else:
            self.label.configure(text="Face was NOT added succesfully. Try again?")




    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="What is your name?", font=controller.title_font)
        self.label.pack(side="top", fill="x", pady=10)

        self.entry= tk.Entry(self, width=10)
        self.entry.focus_set()
        self.entry.pack()

        addFaceButton = tk.Button(self, text="Submit",
                           command=self.didSubmit)
        addFaceButton.pack()

        goBackButton = tk.Button(self, text="Go Back",
                           command=lambda: controller.show_frame("StartPage"))
        goBackButton.pack()


class RecognizeFacePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()








