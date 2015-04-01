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

from os import listdir,getcwd
from os.path import isfile, join
from Tkinter import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys
import numpy


class TkinterGraph(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.figure = Figure(figsize=(10,10), dpi=50)
        self.graph_a = self.figure.add_subplot(111)
        self.graph_a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])



        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.show()
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

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
            if fparts[-1] == 'txt':
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

class PrintThis(object):
    def __init__(self,a_path,gph):
        self.f_path = a_path
        self.gph = gph
    
    def print_this(self,selection):
        (ind , filename) = selection
        file = join(self.f_path,filename)
        rawy = numpy.loadtxt(file, skiprows=1)
        rawx = [i for i in range(len(rawy))]
        self.gph.change_data(rawx,rawy)
        #print 'You so selected this:', lbl, "from ",ind[0]


def main():
    print len(sys.argv)
    if len(sys.argv)==2:
        mypath = sys.argv[1]
    else:
        mypath = getcwd()
        
    files = []
    for filename in listdir(mypath):
        # just get the files
        # note that it has to have the compleate path and name
        if isfile(join(mypath,filename)):
            # split the file name in to parts 
            files.append(filename)
            #parts = filename.split('.')
            #print parts[-1]

    window  = Tk()
    f1 = TkinterGraph(window)
    prnt = PrintThis(mypath,f1)
    scrld = ScrolledList(window,files,lambda x: prnt.print_this(x))
    scrld.pack(side=LEFT,expand=YES, fill=Y) 
    f1.pack(side=LEFT,expand=YES, fill=Y) 
    window.mainloop()
    
    return 0

if __name__ == '__main__':
	main()

