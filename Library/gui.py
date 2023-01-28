
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