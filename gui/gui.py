
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *

class App:
    def __init__(self):
        #setting title
        root=tk.Tk()
        root.title("xml editor")
    
        #setting window size
        width=800
        height=600

        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        xml_cover = PhotoImage(file=r"123.png")
        # Create a label to display the image
        label = Label(root, image=xml_cover)
        label.place(x=0, y=0)
        Button1=tk.Button(root)
        Button1["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        Button1["font"] = ft
        Button1["fg"] = "#000000"
        Button1["justify"] = "center"
        Button1["text"] = "check valid"
        Button1.place(x=360,y=220,width=70,height=25)
        Button1["command"] = self.check_valid

        Button2=tk.Button(root)
        Button2["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        Button2["font"] = ft
        Button2["fg"] = "#000000"
        Button2["justify"] = "center"
        Button2["text"] = "Fix errors"
        Button2.place(x=360,y=250,width=70,height=25)
        Button2["command"] = self.fix_errors

        Button3=tk.Button(root)
        Button3["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        Button3["font"] = ft
        Button3["fg"] = "#000000"
        Button3["justify"] = "center"
        Button3["text"] = "Prettify"
        Button3.place(x=360,y=280,width=70,height=25)
        Button3["command"] = self.prettify

        Button4=tk.Button(root)
        Button4["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        Button4["font"] = ft
        Button4["fg"] = "#000000"
        Button4["justify"] = "center"
        Button4["text"] = "Minify"
        Button4.place(x=360,y=310,width=70,height=25)
        Button4["command"] = self.minify

        Button5=tk.Button(root)
        Button5["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        Button5["font"] = ft
        Button5["fg"] = "#000000"
        Button5["justify"] = "center"
        Button5["text"] = "Compress"
        Button5.place(x=360,y=340,width=70,height=25)
        Button5["command"] = self.compress

        Button6=tk.Button(root)
        Button6["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        Button6["font"] = ft
        Button6["fg"] = "#000000"
        Button6["justify"] = "center"
        Button6["text"] = "To JSON"
        Button6.place(x=360,y=370,width=70,height=25)
        Button6["command"] = self.convert_to_json

        Button7=tk.Button(root)
        Button7["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        Button7["font"] = ft
        Button7["fg"] = "#000000"
        Button7["justify"] = "center"
        Button7["text"] = "Prettify"
        Button7.place(x=360,y=400,width=70,height=25)
        Button7["command"] = self.prettify

