"""This is a module of the file operations used by the file tool."""
import tkMessageBox, tkFileDialog
from Tkinter import *
import mimetypes
from hashlib import md5
from functools import partial
import os
import zipfile
import tarfile

class File():
    def __init__(self):
        self.fhandle = None
        self.fname = None
        
    def openFile(self):
        #close previous file handle and set it to None
        if self.fhandle != None:
            self.fhandle.close()
            self.fhandle = None
            
        self.fname = tkFileDialog.askopenfilename()
        if self.fname:
            try:
                self.fhandle = open(self.fname, 'r')
            except IOError as ioe:
                print ioe
        
    def showContents(self, console):
        console.delete(1.0, END) 
        if self.fhandle == None:
            text = "Please open a file for reading."
        else:
            lines = self.fhandle.readlines()
            text = "".join(lines)
            self.fhandle.seek(0)
            
        console.insert(INSERT, text)
    
    def showProperties(self, console):
        if self.fhandle == None:
            text = "Cannot calculate properties until you open a file"
        else:
            ftype = str(mimetypes.guess_type(self.fname)[0])
            text = "The file type is: " + ftype
            
            fsize = os.path.getsize(self.fname)
            text = text + "\nThe file size is: " + str(fsize)
            
            data = md5()
            for buf in iter(partial(self.fhandle.read, 128), b''):
                data.update(buf)
            self.fhandle.seek(0)
            text = text + "\nThe md5 of the file is: " + data.hexdigest()
            
        console.delete(1.0, END) 
        console.insert(INSERT, text)
        
    def unzip(self, console):
        console.delete(1.0, END) 
        try:
            zfile = zipfile.ZipFile(self.fhandle)
            flist = zfile.namelist()
        except zipfile.error as zfe:
            message = str(zfe) + "\nPlease try again."
            console.insert(INSERT, message)
            return False
        
        #if there is a single file, unzip it and reassign the file handle to the unzipped file
        #otherwise, unzip all files and let the user know the names
        if len(flist) == 1:
            text =  "Unzipping file..." +str(flist[0]) +"\n"
            console.insert(INSERT, text)
            zipfile.ZipFile.extractall(zfile)
            console.insert(INSERT, "Done\n")
            self.fhandle.close()
            text =  "Opening file..." +str(flist[0]) +"\n"
            console.insert(INSERT, text)
            self.fname = flist[0]
            try:
                self.fhandle = open(self.fname)
            except IOError as ioe:
                print ioe
        else:
            #multi unzip
            text =  "Unzipping files..." 
            text += "\n"
            text += " ".join(flist)
            text += "\n"
            console.insert(INSERT, text)
            zipfile.ZipFile.extractall(zfile)
            console.insert(INSERT, "done\n")
            self.fhandle.close()
                
            #reset attributes
            self.fname = None
            self.fhandle = None
                
    def untar(self, console):
        console.delete(1.0, END) 
        try:
            tfile = tarfile.open(self.fname, 'r')
            flist = tfile.getnames()
        except tarfile.ReadError as tre:
            message = str(tre) + "\nPlease try again."
            console.insert(INSERT, message)
            return False
        
        text =  "Untaring files..." 
        text += "\n"
        text += " ".join(flist)
        text += "\n"
        console.insert(INSERT, text)
        try:
            tfile.extractall()
        except tfile.ExtractError as ee:
            print ee
        console.insert(INSERT, "done\n")
                
        #reset attributes
        self.fname = None
        self.fhandle = None

    def deCompress(self, console):
        console.delete(1.0, END) 
        if self.fhandle == None:
            text = "Please open a zip file for me to decompress."
            console.insert(INSERT, text)
        elif str(mimetypes.guess_type(self.fname)[0]) =="application/zip":
            self.unzip(console)
        elif str(mimetypes.guess_type(self.fname)[0]) =="application/x-tar":
            self.untar(console)
        else:
            console.insert(INSERT, "It looks as if the file is not a zip file. Please try again.\n")
