import tkMessageBox, tkFileDialog

def onExit():
    quit()
    
def aboutFileTool():
    aboutMessage = """File Tool was created by Graziano. It's free software, so use it at your own peril"""
    tkMessageBox.showinfo("About File Tool", aboutMessage) 