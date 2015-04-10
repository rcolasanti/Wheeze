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

    def change_data(self,traces):
        self.graph_a.clear()
        for trace in traces:
            self.graph_a.plot(trace[0],trace[1])
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
            if fparts[-1] == 'dat':
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
        self.file_list =  ScrolledList(self,lambda x: self.load_pvr_data(x))
        self.file_list.grid(row=1, column=0, columnspan=3, rowspan=4, 
            padx=5, sticky=E+W+S+N)
        
        # chanel graph viewer
        self.graph_viewer = TkinterGraph(self)
        self.graph_viewer.grid(row=1, column=3, columnspan=2, rowspan=4, 
            padx=5, sticky=E+W+S+N)
        
          # frames for the classifier for the two chanels 
        self.frame_left = Frame(self, borderwidth=1)
        self.frame_right = Frame(self, borderwidth=1)
        self.frame_left.grid(row=5,column=3,columnspan=2, rowspan=1)

        
               
              
               
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
        
    def load_pvr_data(self,selection):
        (self.indx , self.filename) = selection
        d_file = join(self.mypath,self.filename)
        s_array=[]
        with open(d_file) as f:
            for line in f:
                data = line.split(',')
                if data[0]!='':
                    s_array.append(data[0])
        self.rawy = numpy.array(s_array) 
        self.rawx = [i for i in range(len(self.rawy))]
        self.plot_graph()

    def plot_graph(self):
        # choose the correct form of radio buttons
        self.frame_right.grid_forget()
        self.frame_left.grid(row=5,column=3,columnspan=2, rowspan=1)
        # change display name
        self.file_lbl.configure(text=self.filename)
        print "before"
        breaths = self.separate_breaths()
        print "Here"
        self.graph_viewer.change_data(breaths)


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
        
        
    def separate_breaths(self):
        def find_start(pos):
            flag = False
            if self.rawy[pos] < 0:
                flag = True
                for i in range(1, 4):
                    if self.rawy[pos + i] < 0:
                        flag = False
            return flag

        # seperate breaths
        breath = []
        # 4 is number of +ve value after a -ve that corresponds to crossing
        # mid point
        
        for i in range(len(self.rawx) - 4):
            if find_start(i):
                breath.append(i)

        whole_breaths = (len(breath) // 2) * 2 - 1
        breaths = []
        for i in range(whole_breaths):  # this ensures we only take whole breaths
            time = self.rawx[breath[i]:breath[i + 1] + 1]
            flow = self.rawy[breath[i]:breath[i + 1] + 1]
            abreath = [time,flow]
            breaths.append(abreath)
        print breaths
        return breaths

def main():
  
    root = Tk()
    root.geometry("850x500+500+500")
    app = Reader(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
