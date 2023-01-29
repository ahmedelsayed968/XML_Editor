import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
import check_validation
import XMLTree
from Compression import HuffmanCode

class App:
    def __init__(self):
        # setting title
        self.root = tk.Tk()
        self.root.title("xml editor")
        self.root.PATH = None
        self.input_str = None

        # setting window size
        width = 1200 #400
        height = 700 #100

        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        xml_cover = PhotoImage(file='E:\XML_Editor\Library\photo.png')
        #Create a label to display the image
        label = Label(self.root, image=xml_cover)
        label.place(x=0, y=0)
        input_text = tk.Text(self.root)
        input_text.pack()
        input_text["borderwidth"] = "3px"
        ft = tkFont.Font(family='Times', size=10)
        input_text["font"] = ft
        input_text["fg"] = "black"
        input_text.place(x=50, y=150, width=500, height=500)
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
        output_text.place(x=650, y=150, width=500, height=500)
        output_bar = Scrollbar(output_text)
        output_bar.pack(side=RIGHT, fill=Y)
        output_bar.config(command=output_text.yview)
        output_text.config(yscrollcommand=output_bar.set) 
         # adding the main manu
        main_manu = Menu(self.root, background='blue', fg="#DCDC14")
        self.root.config(menu=main_manu)
        File_manu = Menu(main_manu)
        main_manu.add_cascade(label="File", menu=File_manu)
        File_manu.add_command(label="Open New File", command=lambda : load_file(self))
        File_manu.add_separator()
        File_manu.add_command(label="Save...", command=lambda : save_file(self),state='disabled')
        File_manu.add_separator()
        File_manu.add_command(label="Exit", command=lambda : self.root.quit())
    
        def check_valid(self):
            self.input_str=input_text.get("1.0", END)
            output_text.config(state='normal')
            output_text.delete("1.0", END)
            answer=check_validation.valid(self.input_str)
            File_manu.entryconfig(3,state=DISABLED)
            if(answer):
                output_text.insert(INSERT, "the xml is valid")
            else:
                xmlTree =  XMLTree.Tree()
                xmlTree.parser(self.input_str)
                output_text.insert(INSERT, "the xml is not valid")
                output_text.insert(INSERT, xmlTree.check_validation)
            output_text.config(state='disabled')

        
        def fix_errors(self):
            self.input_str=input_text.get("1.0", END)
            output_text.config(state='normal')
            output_text.delete("1.0", END)
            xmlTree =  XMLTree.Tree()
            xmlTree.parser(self.input_str)
            xmlTree.correter_XML()
            output_text.insert(INSERT,xmlTree.visualizeXML())
            output_text.config(state='disabled')
            File_manu.entryconfig(3,state=NORMAL)

        def prettify(self):
            self.input_str=input_text.get("1.0", END)
            output_text.config(state='normal')
            output_text.delete("1.0", END)
            if(check_validation.valid(self.input_str)):
                xmlTree =  XMLTree.Tree()
                xmlTree.parser(self.input_str)
                output_text.insert(INSERT,xmlTree.visualizeXML())
                File_manu.entryconfig(3,state=NORMAL)
            else:
                output_text.insert(INSERT, "please enter a valid xml ")

            output_text.config(state='disabled')

        def minify(self):
            self.input_str=input_text.get("1.0", END)
            output_text.config(state='normal')
            output_text.delete("1.0", END)
            xmlTree = XMLTree.Tree()
            xmlTree.parser(self.input_str)
            xmlTree.update_file_state(XMLTree.Status.minifying)
            output_text.insert(INSERT,xmlTree.file_state_xml)
            output_text.config(state='disabled')
            File_manu.entryconfig(3,state=NORMAL)

        def compress(self):
            self.input_str=input_text.get("1.0", END)
            output_text.config(state='normal')
            output_text.delete("1.0", END)
            h = HuffmanCode(self.input_str)
            compressed_data = h.compress()
            output_text.insert(INSERT, "The compressed data :\n")
            output_text.insert(INSERT, compressed_data)
            output_text.insert(INSERT, "\n------------------------------------------------\n")
            output_text.insert(INSERT, "The decompressed_data :\n")
            decompressed_data = h.decompress(compressed_data)
            output_text.insert(INSERT, decompressed_data)
            File_manu.entryconfig(3,state=NORMAL)
            output_text.config(state='disabled')

        def convert_to_json(self):
            self.input_str=input_text.get("1.0", END)
            output_text.config(state='normal')
            output_text.delete("1.0", END)
            if(check_validation.valid(self.input_str)):
                xmlTree =  XMLTree.Tree()
                xmlTree.parser(self.input_str)
                output_text.insert(INSERT, xmlTree.visualizeJSON())
                File_manu.entryconfig(3,state=NORMAL)
            else:
                output_text.insert(INSERT, "please enter a valid xml ")

            output_text.config(state='disabled')


        def load_file(self):
            try:
                input_text.delete("1.0",END)
                self.root.PATH = filedialog.askopenfilename(initialdir='../', title='Open New File',
                                                        filetypes=(('xml files', '*.xml'), ('all files', '*.*')))
                with open(self.root.PATH, 'r') as f:
                    input_text.insert(INSERT, f.read())
            except:
                pass
                     
        def save_file(self):
            try:
                self.root.PATH = filedialog.asksaveasfilename(defaultextension=".xml")
                with open(self.root.PATH, 'w') as f:
                    f.write(output_text.get("1.0", END))
            except:
                pass
            
        Button1 = tk.Button(self.root,command=lambda:check_valid(self))
        Button1["bg"] = "black"
        ft = tkFont.Font(family='Times', size=14)
        Button1["font"] = ft
        Button1["fg"] = "white"
        Button1["justify"] = "center"
        Button1["text"] = "check valid"
        Button1.place(x=554, y=220, width=95, height=25)
        Button1["borderwidth"] = "3px"

        Button2 = tk.Button(self.root,command=lambda:fix_errors(self))
        Button2["bg"] = "black"
        ft = tkFont.Font(family='Times', size=14)
        Button2["font"] = ft
        Button2["fg"] = "white"
        Button2["justify"] = "center"
        Button2["text"] = "Fix Errors"
        Button2.place(x=554, y=250, width=95, height=25)
        Button2["borderwidth"] = "3px"

        Button3 = tk.Button(self.root,command=lambda:prettify(self))
        Button3["bg"] = "black"
        ft = tkFont.Font(family='Times', size=14)
        Button3["text"] = "Prettify"
        Button3["font"] = ft
        Button3["fg"] = "white"
        Button3["justify"] = "center"
        Button3.place(x=554, y=280, width=95, height=25)
        Button3["borderwidth"] = "3px"


        Button4 = tk.Button(self.root,command=lambda:minify(self))
        Button4["bg"] = "black"
        ft = tkFont.Font(family='Times', size=14)
        Button4["font"] = ft
        Button4["fg"] = "white"
        Button4["justify"] = "center"
        Button4["text"] = "Minify"
        Button4.place(x=554, y=310, width=95, height=25)
        Button4["borderwidth"] = "3px"

        Button5 = tk.Button(self.root,command=lambda:compress(self))
        Button5["bg"] = "black"
        ft = tkFont.Font(family='Times', size=14)
        Button5["font"] = ft
        Button5["fg"] = "white"
        Button5["justify"] = "center"
        Button5["text"] = "Compress"
        Button5.place(x=554, y=340, width=95, height=25)
        Button5["borderwidth"] = "3px"


        Button6 = tk.Button(self.root,command=lambda:convert_to_json(self))
        Button6["bg"] = "black"
        ft = tkFont.Font(family='Times', size=14)
        Button6["font"] = ft
        Button6["fg"] = "white"
        Button6["justify"] = "center"
        Button6["text"] = "To JSON"
        Button6.place(x=554, y=370, width=95, height=25)
        Button6["borderwidth"] = "3px"
       
        welcome_label = tk.Label(self.root)
        ft = tkFont.Font(family='Arial', size=20)
        welcome_label["font"] = ft
        welcome_label["fg"] = "white"
        welcome_label["bg"] = "black"
        welcome_label["justify"] = "center"
        welcome_label["text"] = "Welcome to XML editor"
        welcome_label.place(x=350, y=50, width=500, height=41)

        self.root.mainloop()
if __name__ == "__main__":
    app = App()