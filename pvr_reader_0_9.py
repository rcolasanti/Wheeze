#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2015  <ric.colasanti@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
from Tkinter import Tk, Text, BOTH, W, N, E, S,Y,RIGHT,LEFT,YES,Scrollbar,Listbox,StringVar,Menu
from ttk import Frame, Button, Label, Style,Radiobutton,Scrollbar
from tkFileDialog   import askopenfilename
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure 
from os import listdir,getcwd,rename
from os.path import isfile, join,split
import sys
import numpy


class TkinterGraph(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.figure = Figure(figsize=(10,10), dpi=50)
        self.graph_a = self.figure.add_subplot(111)
       
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.show()
        self.canvas._tkcanvas.pack(fill=BOTH, expand=1)

    def change_data(self,datay,datax):
        self.graph_a.clear()
        self.graph_a.plot(datay,datax)
        self.canvas.draw()


class ScrolledList(Frame):
    def __init__(self, master,a_function):
        Frame.__init__(self,master)
        
        scrl_bar = Scrollbar(self)
        self.listbox = Listbox(self)
        
        scrl_bar.config(command=self.listbox.yview)                   
        scrl_bar.pack(side=RIGHT, fill=Y)                     
        
        self.listbox.config(yscrollcommand=scrl_bar.set)              
        self.listbox.pack(side=LEFT, expand=YES, fill=BOTH)       
        

        # link double click to the processList
        self.listbox.bind('<Double-1>', self.processList)  
        # attach a function passed form the master
        # not this si done as passd function so it could be anything       
        self.passed_function = a_function
        
    # get the index of the double clicked itenm and pass the item to
    # the passed function    
    def processList(self, event):
        index = self.listbox.curselection()               
        label = self.listbox.get(index)  
        self.passed_function((index,label))
        
    def load_data(self,d_list):
        #load the listbox
        idx = 0
        for item in d_list:      
            fparts = item.split('.')
            # DEBUG print fparts
            if fparts[-1] == 'csv':
                # only display thoes files that have not been processed
                if not(item.startswith("done-")):
                    self.listbox.insert(idx, item)                       
                    idx += 1
        
    def remove_item(self,idx):
        self.listbox.delete(idx)
        
class Reader(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.parent = parent
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("Graphs")
        self.style = Style()
        self.style.theme_use("clam")
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(6, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)
        
        menu = Menu(self.parent)
        self.parent.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Load data",command = self.load_data)
        
        # lable to show current file and chanel
        self.file_lbl = Label(self, text="")
        self.file_lbl.grid(row = 0 , column = 3, pady=4, padx=5)
        
        # list box fro data files
        self.file_list =  ScrolledList(self,lambda x: self.load_hunt_data(x))
        self.file_list.grid(row=1, column=0, columnspan=3, rowspan=4, 
            padx=5, sticky=E+W+S+N)
        
        # chanel graph viewer
        self.graph_viewer = TkinterGraph(self)
        self.graph_viewer.grid(row=1, column=3, columnspan=2, rowspan=4, 
            padx=5, sticky=E+W+S+N)
        
        btn1 = Button(self, text="Left",command = lambda: self.plot_left())
        btn1.grid(row=1, column=6)

        btn2 = Button(self, text="Right", command = lambda:self.plot_right())
        btn2.grid(row=2, column=6, pady=4)
        
        # frames for the classifier for the two chanels 
        self.frame_left = Frame(self, borderwidth=1)
        self.frame_right = Frame(self, borderwidth=1)
        self.frame_left.grid(row=5,column=3,columnspan=2, rowspan=1)

        btn4 = Button(self, text="SAVE", command = lambda:self.save_graph())
        btn4.grid(row=5, column=6) 
        
        # note manual addition of labels so that the lable will be to the right of tha radio button 
        self.classify_left = StringVar()
        Label(self.frame_left,text="Left  :").pack(side=LEFT)
        Label(self.frame_left,text="Type A").pack(side=LEFT)
        rb1 = Radiobutton(self.frame_left,variable=self.classify_left,value="TypeA")
        rb1.pack(side=LEFT)
        Label(self.frame_left,text="Type B").pack(side=LEFT)
        rb1 = Radiobutton(self.frame_left,variable=self.classify_left,value="TypeB")
        rb1.pack(side=LEFT)
        Label(self.frame_left,text="Type C").pack(side=LEFT)
        rb1 = Radiobutton(self.frame_left,variable=self.classify_left,value="TypeC")
        rb1.pack(side=LEFT)
        Label(self.frame_left,text="Type D").pack(side=LEFT)
        rb1 = Radiobutton(self.frame_left,variable=self.classify_left,value="TypeD")
        rb1.pack(side=LEFT)
       
        
               
        self.classify_right = StringVar()
        Label(self.frame_right,text="Right  :").pack(side=LEFT)
        Label(self.frame_right,text="Type A").pack(side=LEFT)
        rb1 = Radiobutton(self.frame_right,variable=self.classify_right,value="TypeA")
        rb1.pack(side=LEFT)
        Label(self.frame_right,text="Type B").pack(side=LEFT)
        rb1 = Radiobutton(self.frame_right,variable=self.classify_right,value="TypeB")
        rb1.pack(side=LEFT)
        Label(self.frame_right,text="Type C").pack(side=LEFT)
        rb1 = Radiobutton(self.frame_right,variable=self.classify_right,value="TypeC")
        rb1.pack(side=LEFT)
        Label(self.frame_right,text="Type D").pack(side=LEFT)
        rb1 = Radiobutton(self.frame_right,variable=self.classify_right,value="TypeD")
        rb1.pack(side=LEFT)
              
               
    def load_data(self):
        # calls the file dialog box
        name = askopenfilename()
        (d_path,d_name)=split(name)
        # just want to extract the path of the file
        self.mypath = d_path
        # get 'filtered' files from that path
        files = self.get_files()
        # display in the list box
        self.file_list.load_data(files)
        
    def load_hunt_data(self,selection):
        (self.indx , self.filename) = selection
        d_file = join(self.mypath,self.filename)
        l_array=[]
        r_array=[]
        with open(d_file) as f:
            for line in f:
                data = line.split(',')
                if data[5]!='':
                    r_array.append(data[5]) # RL_PVR
                    l_array.append(data[6]) # LL_PVR
        self.rawy_l = numpy.array(l_array[1:]) # form 1 romove headder
        self.rawy_r = numpy.array(r_array[1:])
        self.rawx = [i for i in range(len(self.rawy_l))]
        # reset the classification buttons
        self.classify_left.set("TypeA")
        self.classify_right.set("TypeA")
        self.plot_left()

    def plot_left(self):
        # choose th correct fram of radio buttons
        self.frame_right.grid_forget()
        self.frame_left.grid(row=5,column=3,columnspan=2, rowspan=1)
        # change display name
        self.file_lbl.configure(text=self.filename+" : Left")
        self.graph_viewer.change_data(self.rawx,self.rawy_l)

    def plot_right(self):
        self.frame_left.grid_forget()
        self.frame_right.grid(row=5,column=3,columnspan=2, rowspan=1)
        self.file_lbl.configure(text=self.filename+" : Right")
        self.graph_viewer.change_data(self.rawx,self.rawy_r)
        
    def save_graph(self):
        self.file_list.remove_item(self.indx)
        d_file = join(self.mypath,self.filename)
        # add a done prefix to the file name
        n_file = join(self.mypath,"done-"+self.filename)
        rename(d_file,n_file)
        # get the front of the filename
        fparts = self.filename.split('.')
        # save data wit the same name but with the chanel prefix and a dat postfix
        l_file = join(self.mypath,self.classify_left.get()+'-Left-'+fparts[0]+'.dat')
        # open file to write
        f = open(l_file, 'w')
        for v in self.rawy_l:
            f.write(v+'\n')
        f.close()
        r_file = join(self.mypath,self.classify_right.get()+'-Right-'+fparts[0]+'.dat')
        # open file to write
        f = open(r_file, 'w')
        for v in self.rawy_r:
            f.write(v+'\n')
        f.close()
        

    def get_files(self):
        files = []
        for filename in listdir(self.mypath):
            # just get the files
            # note that it has to have the compleate path and name
            if isfile(join(self.mypath,filename)):
                # split the file name in to parts 
                files.append(filename)
                #parts = filename.split('.')
                #print parts[-1]
        return files
def main():
  
    root = Tk()
    root.geometry("850x500+500+500")
    app = Reader(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
