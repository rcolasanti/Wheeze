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
from Tkinter import Tk, Text, BOTH, W, N, E, S,Y,RIGHT,LEFT,YES,Scrollbar,Listbox,IntVar
from ttk import Frame, Button, Label, Style,Radiobutton
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure 
from os import listdir,getcwd
from os.path import isfile, join
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
    def __init__(self, master,d_list,a_function):
        Frame.__init__(self,master)
        
        scrl_bar = Scrollbar(self)
        self.listbox = Listbox(self)
        
        scrl_bar.config(command=self.listbox.yview)                   
        scrl_bar.pack(side=RIGHT, fill=Y)                     
        
        self.listbox.config(yscrollcommand=scrl_bar.set)              
        self.listbox.pack(side=LEFT, expand=YES, fill=BOTH)       
        
        #load the listbox
        idx = 0
        for item in d_list:      
            fparts = item.split('.')
            # DEBUG print fparts
            if fparts[-1] == 'csv':
                self.listbox.insert(idx, item)                       
                idx += 1

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
        
class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        if len(sys.argv)==2:
            self.mypath = sys.argv[1]
        else:
            self.mypath = getcwd()
                     
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
        
        lbl = Label(self, text="Graphs")
        lbl.grid(sticky=W, pady=4, padx=5)
        
        files = self.get_files()
        area1 =  ScrolledList(self,files,lambda x: self.load_hunt_data(x))
        area1.grid(row=1, column=0, columnspan=3, rowspan=4, 
            padx=5, sticky=E+W+S+N)

        self.graph_viewer = TkinterGraph(self)
        self.graph_viewer.grid(row=1, column=3, columnspan=2, rowspan=4, 
            padx=5, sticky=E+W+S+N)
        
        btn1 = Button(self, text="Left",command = lambda: self.plot_left())
        btn1.grid(row=1, column=6)

        btn2 = Button(self, text="Right", command = lambda:self.plot_right())
        btn2.grid(row=2, column=6, pady=4)
        
        btn3 = Button(self, text="csv")
        btn3.grid(row=5, column=0, padx=5)
        
        btn5 = Button(self, text="dat")
        btn5.grid(row=5, column=2, padx=5)
        
        frame1 = Frame(self, borderwidth=1)
        frame1.grid(row=5,column=3,columnspan=2, rowspan=1)

        btn4 = Button(self, text="SAVE")
        btn4.grid(row=5, column=6) 
        
        self.classify = IntVar()
        rb1 = Radiobutton(frame1,text="Type A",variable=self.classify,value=1)
        rb1.pack(side=LEFT)
        rb1 = Radiobutton(frame1,text="Type B",variable=self.classify,value=2)
        rb1.pack(side=LEFT)
        rb1 = Radiobutton(frame1,text="Type C",variable=self.classify,value=3)
        rb1.pack(side=LEFT)
        rb1 = Radiobutton(frame1,text="Type D",variable=self.classify,value=4)
        rb1.pack(side=LEFT)
               
    def load_hunt_data(self,selection):
        (self.ind , self.filename) = selection
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
        self.classify.set(0)
        self.plot_left()

    def plot_left(self):
        self.graph_viewer.change_data(self.rawx,self.rawy_l)

    def plot_right(self):
        self.graph_viewer.change_data(self.rawx,self.rawy_r)

        
        

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
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
