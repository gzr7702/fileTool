'''
This is an application that can be used to view, decompress and find the properties of files. It uses Tkinter as the interface and
python 2.7

@author: rob
'''
from Tkinter import *
from ttk import *
import tkFileDialog
import fileActions
import standardActions

class Application(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.grid()
        self.initUI()
        self.fileObj = fileActions.File()
        
        
    def initUI(self):
        
        self.general_font = ("Helvetica", 10, "bold")
        self.console_font = ("Andale Mono", 10, "bold")
    
        #menus -------------------------------------------->
        menubar = Menu(self.parent, tearoff=0)
        self.parent.config(menu=menubar)
        #File
        fileMenu = Menu(menubar)
        menubar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Open...", command=lambda: self.fileObj.openFile())
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=standardActions.onExit)
        #Tools
        toolsMenu = Menu(menubar)
        menubar.add_cascade(label="Tools", menu=toolsMenu)
        toolsMenu.add_command(label="Unzip", command=lambda: self.fileObj.deCompress(self.console))
        toolsMenu.add_command(label="Read File", command=lambda: self.fileObj.showContents(self.console))
        toolsMenu.add_command(label="Show Properties", command=lambda: self.fileObj.showProperties(self.console))
        #About
        aboutmenu = Menu(menubar)
        menubar.add_cascade(label="About", menu=aboutmenu)
        aboutmenu.add_command(label="About File Tool", command=standardActions.aboutFileTool)
        
        #main window ---------------------------------------->
        self.parent.title("File Tool")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
        self.columnconfigure(0, weight=1, pad=3)
        self.columnconfigure(1, weight=1, pad=3)
        self.columnconfigure(2, weight=1, pad=3)
        self.columnconfigure(3, weight=1, pad=3)
        self.rowconfigure(0, weight=1, pad=3)
        self.rowconfigure(1, weight=1, pad=3)
        self.rowconfigure(2, weight=1, pad=3)
        self.rowconfigure(3, weight=1, pad=3)
        self.rowconfigure(4, weight=1, pad=3)
        
        consoleText = """Please open a file...
            """
        self.console = Text(self, font=self.console_font)
        self.console.grid(row=0, column=0, columnspan=4, rowspan=4, sticky=E+W+N+S, padx=15, pady=5)
        self.console["bg"] = "black"
        self.console["fg"] = "white"
        self.console.insert(INSERT, consoleText)
        scrollbar = Scrollbar(self.console)
        self.console.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar.config(command=self.console.yview)
        
        obtn = Button(self, text="Open", command=lambda: self.fileObj.openFile())
        obtn.grid(row=4, column=0)
        
        pbtn = Button(self, text="Properties", command=lambda: self.fileObj.showProperties(self.console))
        pbtn.grid(row=4, column=1)
        
        rbtn = Button(self, text="Read", command=lambda: self.fileObj.showContents(self.console))
        rbtn.grid(row=4, column=2)

        dcbtn = Button(self, text="Unzip", command=lambda: self.fileObj.deCompress(self.console))
        dcbtn.grid(row=4, column=3)
        
        self.pack()

def main():
  
    root = Tk()
    app = Application(root)
    root.geometry("640x400+300+300")
    root.resizable(0,0)
    root.mainloop()  


if __name__ == '__main__':
    main()