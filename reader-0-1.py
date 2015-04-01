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
    def __init__(self):
        pass
    
    def print_this(self,selection):
        (ind , lbl) = selection
        print 'You so selected this:', lbl, "from ",ind[0]


def main():
    mypath = "/home/pi/Downloads/"
    #mypath = getcwd()
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
    prnt = PrintThis()
    scrld = ScrolledList(window,files,lambda x: prnt.print_this(x))
    scrld.pack(expand=YES, fill=BOTH) 
    window.mainloop()
    
    return 0

if __name__ == '__main__':
	main()

