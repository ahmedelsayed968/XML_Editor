import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk


class App:
    def __init__(self):
        # setting title
        self.root = tk.Tk()
        self.root.title("xml editor")
        self.root.PATH = None

        # setting window size
        width = 800
        height = 600

        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        xml_cover = PhotoImage(file=r"123.png")
        # Create a label to display the image
        label = Label(self.root, image=xml_cover)
        label.place(x=0, y=0)
        Button1 = tk.Button(self.root)
        Button1["bg"] = "black"
        ft = tkFont.Font(family='Times', size=12)
        Button1["font"] = ft
        Button1["fg"] = "white"
        Button1["justify"] = "center"
        Button1["text"] = "check valid"
        Button1.place(x=360, y=220, width=85, height=25)
        Button1["command"] = self.check_valid
        Button1["borderwidth"] = "3px"


        Button2 = tk.Button(self.root)
        Button2["bg"] = "black"
        ft = tkFont.Font(family='Times', size=12)
        Button2["font"] = ft
        Button2["fg"] = "white"
        Button2["justify"] = "center"
        Button2["text"] = "Fix errors"
        Button2.place(x=360, y=250, width=85, height=25)
        Button2["command"] = self.fix_errors
        Button2["borderwidth"] = "3px"


        Button3 = tk.Button(self.root)
        Button3["bg"] = "black"
        ft = tkFont.Font(family='Times', size=12)
        Button3["font"] = ft
        Button3["fg"] = "white"
        Button3["justify"] = "center"
        Button3["text"] = "Prettify"
        Button3.place(x=360, y=280, width=85, height=25)
        Button3["command"] = self.prettify
        Button3["borderwidth"] = "3px"


        Button4 = tk.Button(self.root)
        Button4["bg"] = "black"
        ft = tkFont.Font(family='Times', size=12)
        Button4["font"] = ft
        Button4["fg"] = "white"
        Button4["justify"] = "center"
        Button4["text"] = "Minify"
        Button4.place(x=360, y=310, width=85, height=25)
        Button4["command"] = self.minify
        Button4["borderwidth"] = "3px"

        Button5 = tk.Button(self.root)
        Button5["bg"] = "black"
        ft = tkFont.Font(family='Times', size=12)
        Button5["font"] = ft
        Button5["fg"] = "white"
        Button5["justify"] = "center"
        Button5["text"] = "Compress"
        Button5.place(x=360, y=340, width=85, height=25)
        Button5["command"] = self.compress
        Button5["borderwidth"] = "3px"


        Button6 = tk.Button(self.root)
        Button6["bg"] = "black"
        ft = tkFont.Font(family='Times', size=12)
        Button6["font"] = ft
        Button6["fg"] = "white"
        Button6["justify"] = "center"
        Button6["text"] = "To JSON"
        Button6.place(x=360, y=370, width=85, height=25)
        Button6["command"] = self.convert_to_json
        Button6["borderwidth"] = "3px"

        input_text = tk.Text(self.root)
        input_text["borderwidth"] = "3px"
        ft = tkFont.Font(family='Times', size=10)
        input_text["font"] = ft
        input_text["fg"] = "black"
        input_text.place(x=50, y=150, width=300, height=400)
        input_bar = Scrollbar(input_text)
        input_bar.pack(side=RIGHT, fill=Y)
        input_bar.config(command=input_text.yview)
        input_text.config(yscrollcommand=input_bar.set)


        output_text = tk.Text(self.root, state='disabled')
        # Insert the string into the Text widget
        output_text.insert('1.0', 'This is a read-only string')
        output_text["borderwidth"] = "3px"
        ft = tkFont.Font(family='Times', size=10)
        output_text["font"] = ft
        output_text["fg"] = "black"
        output_text.place(x=450, y=150, width=300, height=400)
        output_bar = Scrollbar(output_text)
        output_bar.pack(side=RIGHT, fill=Y)
        output_bar.config(command=output_text.yview)
        output_text.config(yscrollcommand=output_bar.set)



        

        welcome_label = tk.Label(self.root)
        ft = tkFont.Font(family='Arial', size=14)
        welcome_label["font"] = ft
        welcome_label["fg"] = "white"
        welcome_label["bg"] = "black"
        welcome_label["justify"] = "center"
        welcome_label["text"] = "Welcome to XML editor"
        welcome_label.place(x=280, y=50, width=234, height=41)

        # adding the main manu
        main_manu = Menu(self.root, background='blue', fg="#DCDC14")
        self.root.config(menu=main_manu)
        File_manu = Menu(main_manu)
        main_manu.add_cascade(label="File", menu=File_manu)
        File_manu.add_command(label="Open New File", command=self.load_file)
        File_manu.add_separator()
        File_manu.add_command(label="Save...", command=self.save_file)
        File_manu.add_separator()
        File_manu.add_command(label="Exit", command=self.root.quit)


        self.root.mainloop()

    def check_valid(self):
        pass

    def fix_errors(self):
        pass

    def prettify(self):
        pass

    def minify(self):
        pass

    def compress(self):
        pass

    def convert_to_json(self):
        pass

    def prettify(self):
        pass

    def load_file(self):
        self.root.PATH = filedialog.askopenfilename(initialdir='../', title='Open New File',
                                                        filetypes=(('xml files', '*.xml'), ('all files', '*.*')))

    def save_file(self):
        pass


if __name__ == "__main__":
    app = App()