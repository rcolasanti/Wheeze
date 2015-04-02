#!/usr/bin/env python
from Tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure 
from tkFileDialog   import *
import numpy
from ScrolledText import *;
from scipy import stats
import os
from math import *
from pylab import * 
import csv
import random

class ScaleDemo(Frame):
    
    def smooth(self,x,window_len=11):
        s=numpy.r_[2*x[0]-x[window_len-1::-1],x,2*x[-1]-x[-1:-window_len:-1]]
        w=numpy.hanning(window_len)
        y=numpy.convolve(w/w.sum(),s,mode='same')
        return y[window_len:-window_len+1]

    def __init__(self):
        
        self.fileName=""
        self.rawData=""
        self.processedData=""
        
        self.file_loaded =   False
        self.f = Frame.__init__(self)
        self.pack()
        self.master.title("Wheeze")
        self.master.geometry("1020x650")
        
        self.menu = Menu(self)
        self.master.config(menu=self.menu)
        self.tkMenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.tkMenu)
        self.tkMenu.add_command(label="Open", command=self.readData)
        
        self.tkMenuData = Menu(self.menu)
        self.menu.add_cascade(label="Data", menu=self.tkMenuData)
        self.tkMenuData.add_command(label="Process", command=self.breath_stats)
        self.tkMenuData.add_command(label="Save", command=self.saveData)
        
        self.left_frame = Frame(height=150, width=50)
        self.left_frame.pack(side=LEFT, fill=BOTH, expand=1)
        self.right_frame = Frame(height=150, width=50)
        self.right_frame.pack(side=LEFT, fill=BOTH, expand=1)
        
        self.top_frame1 = Frame(self.left_frame, borderwidth=5, relief=RIDGE)
        self.top_frame1.pack(side=TOP, fill=BOTH, expand=1)
        self.bottom_frame1 = Frame(self.left_frame, borderwidth=5, relief=RIDGE,)
        self.bottom_frame1.pack(side=BOTTOM, fill=BOTH, expand=1)
        
        self.top_frame2 = Frame(self.right_frame, borderwidth=5, relief=RIDGE)
        self.top_frame2.pack(side=TOP, fill=BOTH, expand=1)
        self.bottom_frame2 = Frame(self.right_frame, borderwidth=5, relief=RIDGE,)
        self.bottom_frame2.pack(side=BOTTOM, fill=BOTH, expand=1)
        
        f = Figure(figsize=(5, 4), dpi=80)
        self.ax1 = f.add_subplot(121)
        self.ax4 = f.add_subplot(122)
        self.dataPlot = FigureCanvasTkAgg(f, master=self.top_frame2)
        self.dataPlot.get_tk_widget().pack(side=BOTTOM, fill=BOTH)
        

        f = Figure(figsize=(3, 4), dpi=65)
        self.ax2 = f.add_subplot(111)
        self.l1 = self.ax1.axvline(color='r') 
        self.l2 = self.ax1.axvline(color='r') 

        self.dataPlot2 = FigureCanvasTkAgg(f, master=self.top_frame1)
        self.dataPlot2.get_tk_widget().pack(side=TOP, fill=BOTH)
        
        f = Figure(figsize=(3, 4), dpi=65)
        self.dataPlot3 = FigureCanvasTkAgg(f, master=self.top_frame1)
        self.ax3 = f.add_subplot(111)
        self.dataPlot3.get_tk_widget().pack(side=TOP, fill=BOTH)
        
        self.scrolled_text = ScrolledText(self.bottom_frame2)
        self.scrolled_text.pack(side=TOP, fill=BOTH)
        
        self.control1 = Scale(self.bottom_frame1 , from_=0, to=100, showvalue=0, orient=HORIZONTAL, command=self.updatePlot1)
        self.control1.pack(fill=X)
        self.control1.set(0)
        self.control2 = Scale(self.bottom_frame1 , from_=0, to=100, showvalue=0, orient=HORIZONTAL, command=self.updatePlot2)
        self.control2.pack(fill=X)
        self.control2.set(100)
        self.control_smooth = Scale(self.bottom_frame1 , from_=0, to=100, showvalue=1, orient=HORIZONTAL, command=self.updatePlot3)
        self.control_smooth.pack(fill=X)
        self.control_smooth.set(4)
        self.dataPlot.show()
        self.dataPlot2.show()
        
        
    def updatePlot1(self, scaleValue):
        end = int(scaleValue)
        self.l1.set_xdata(end)
        self.dataPlot3.draw()
        self.plot_data(self.control1.get(), self.control2.get(),self.control_smooth.get())

    def updatePlot2(self, scaleValue):
        end = int(scaleValue)
        self.l2.set_xdata(end)
        self.dataPlot3.draw()
        self.plot_data(self.control1.get(), self.control2.get(),self.control_smooth.get())
    
    def updatePlot3(self,scaleValue):
        self.plot_data(self.control1.get(), self.control2.get(),self.control_smooth.get())

    def plot_data(self, start_data, end_data,smooth_val):
        if self.file_loaded == True :
            self.scrolled_text.delete(1.0, END)
            self.smooth_value = smooth_val
            self.ax1.clear()
            self.ax2.clear()
            self.ax4.clear()
            smooth_x, smooth_y = self.smooth_data(start_data, end_data,smooth_val)
            self.ax2.grid(True)
            self.ax2.plot(smooth_x, smooth_y, '-b');
            axis([0, len(self.rawy), -1, 1])
            self.dataPlot2.draw()
            self.breaths = self.separate_breaths(smooth_x, smooth_y)
            for breath in self.breaths:
                self.ax1.plot(breath[1], breath[2], '-y')
                self.ax4.plot(breath[3], breath[2], '-y')
            self.ax1.grid(True)
            self.ax4.grid(True)
            self.dataPlot.draw()

    def saveData(self):
        if self.fileName !="":
            fileName = asksaveasfilename(title="Save breath data as", filetypes=[("csv file",".csv"),("All files",".*")])
            file = open(fileName,'w')
            file.write('File Name')
            for lab in self.lables:
                file.write(","+lab)
            file.write("\n")
            for item in self.bstats:
                file.write(self.fileName)
                for d in item:
                        file.write(","+str(d))
                file.write("\n")
            file.close()
            
    def readData(self):
        self.fileName = askopenfilename(title="Open file", filetypes=[("txt file",".txt"),("All files",".*")])
        file = self.fileName
        self.file_loaded = True
        self.master.title("Wheeze-"+file)
        self.rawy = numpy.loadtxt(file, skiprows=1)
        self.rawx = [i for i in range(len(self.rawy))]
        self.ax3.clear()
        self.ax3.plot(self.rawx, self.rawy, '-b')
        self.ax3.grid(True)
        axis([0, len(self.rawy), -1, 1])
        self.l1 = self.ax3.axvline(color='r') 
        self.l2 = self.ax3.axvline(color='r') 
        self.control1.configure(to=len(self.rawy))
        self.control1.set(100)
        self.control2.configure(to=len(self.rawy))
        self.control2.set(len(self.rawy))
        self.plot_data(self.control1.get(), self.control2.get(),self.control_smooth.get())
        
    def smooth_data(self, start_data, end_data,smooth_size):
        flow = self.rawy[start_data:end_data]
        time = [i / 100.0 for i in range(len(flow))]
        length = numpy.size(time)
        smooth_data_length = length - (2 * smooth_size)
        smooth_data_value = numpy.zeros((smooth_data_length, 2))
        for i in range(smooth_size, length - smooth_size):
            smooth_data_value[i - smooth_size] = [time[i], numpy.average(flow[i - smooth_size:i + smooth_size])]
        smooth_time = smooth_data_value[:, 0]
        smooth_flow = smooth_data_value[:, 1]
        zeroed = numpy.average(smooth_flow)
        for i in range(len(smooth_flow)):
            smooth_flow[i]-=zeroed
        return smooth_time, smooth_flow
        
    def separate_breaths(self, smooth_time, smooth_flow):
        def find_start(pos):
            flag = False
            if smooth_flow[pos] < 0:
                flag = True
                for i in range(1, 4):
                    if smooth_flow[pos + i] < 0:
                        flag = False
            return flag

        # seperate breaths
        breath = []
        # 4 is number of +ve value after a -ve that corresponds to crossing
        # mid point
        
        for i in range(len(smooth_time) - 4):
            if find_start(i):
                breath.append(i)

        whole_breaths = (len(breath) // 2) * 2 - 1
        breaths = []
        for i in range(whole_breaths):  # this ensures we only take whole breaths
            time = smooth_time[breath[i]:breath[i + 1] + 1]
            flow = smooth_flow[breath[i]:breath[i + 1] + 1]
            v=0
            volume=[]
            ztime=[0]
            flow_dif =[0]
            for i in range(len(flow)):
                v+=(0.5*(flow[i-1]+flow[i])*(time[i]-time[i-1]))
                volume.append(v)
                flow_dif.append(volume[i]-volume[i-1])
            for i in range(1,len(time)):
                ztime.append(time[i] - time[0])
            abreath = [time,ztime, flow,volume,flow_dif]
            breaths.append(abreath)
        return breaths

    def breath_stats(self):
        
        def binary_search(n_list, value_to_find, lo, hi):
            while lo < hi:
                mid = (lo+hi)//2
                midval = n_list[mid]
                if midval > value_to_find:
                    lo = mid+1
                elif midval < value_to_find: 
                    hi = mid
            return mid
         
        def binary_search_neg(n_list, value_to_find, lo, hi):
            while lo < hi:
                mid = (lo+hi)//2
                midval = n_list[mid]
                if midval > value_to_find:
                    lo = mid+1
                elif midval < value_to_find: 
                    hi = mid
            return mid

        def find_crossover(aflow):
            xpoint = 0
            flag = False
            for pos in range(len(aflow)):
                if aflow[pos]>0 :
                    flag = True
                    for i in range(1,4):
                        if aflow[pos+i] >0:
                            flag = False
                    if flag:
                        xpoint = pos
            return xpoint
        
        def find_volume(start_at,finish_at,time,aflow):
            volume = 0.0
            for i in range((start_at+1),finish_at):
                volume += ((aflow[i]+aflow[i-1])/2.0)*(time[i]-time[i-1])
            return volume
            
        def find_cog(start_at,midpoint,aflow):
            i=start_at
            sumVol=0.0
            while sumVol+(-aflow[i]*0.01)<midpoint:
                sumVol+=(-aflow[i]*0.01)
                i+=1
            return i


        def find_centroid(tag,start_at,finish_at,volume,aflow):
            max_volume = max(volume[start_at:finish_at])
            min_volume = min(volume[start_at:finish_at])
            volume_range = max_volume-min_volume
            max_flow = max(aflow[start_at:finish_at])
            min_flow = min(aflow[start_at:finish_at])
            flow_range = max_flow-min_flow
            v_count = 0.0
            f_count = 0.0
            s_count = 0
            count =0
            sa = finish_at-start_at
            for i in range(10000):
                c = int(random.random()*sa+start_at)
                f = random.random()*flow_range+min_flow
                if (tag and f>= aflow[c]) or  ((tag==False) and f<= aflow[c]):
                    v = volume[c]
                    v_count+=v
                    f_count+=f
                    s_count+=1
            v_est = v_count/s_count
            f_est = f_count/s_count
            return volume_range, flow_range,v_est , f_est


        def find_FVG_TNG(tag,start_at,finish_at,volume,aflow):
            max_volume = max(volume[start_at:finish_at])
            min_volume = min(volume[start_at:finish_at])
            volume_range = max_volume-min_volume
            max_flow = max(aflow[start_at:finish_at])
            min_flow = min(aflow[start_at:finish_at])
            flow_range = max_flow-min_flow
            v_count = 0.0
            f_count = 0.0
            s_count = 0
            count =0
            for i in range(10000):
                f = random.random()*flow_range+min_flow
                v = random.random()*volume_range+min_volume
                if tag:
                    count = binary_search(volume,v,start_at,finish_at)
                else:
                    count = binary_search_neg(volume,v,start_at,finish_at)
                if (tag and f>= aflow[count]) or  ((tag==False) and f>= aflow[count]):
                    v_count+=v
                    f_count+=f
                    s_count+=1
            v_est = v_count/s_count
            f_est = f_count/s_count
            return volume_range, flow_range,v_est , f_est

        def get_Slope(start_at,finish_at,sample,aflow):
            length = len(aflow[start_at:finish_at])
            length20 = int(length*0.2)+start_at
            length80 = int(length*0.8)+start_at

            x2 = sample[start_at:length20]
            y2 = aflow[start_at:length20]
            # call liner regression for that data set
            slope, intercept, r_value, p_value, std_err = stats.linregress(x2,y2)
            angle_1 = math.degrees(math.atan(slope))
            self.ax1.plot(x2,y2,'.' '-r')
     
            
            x2 = sample[length20:length80]
            y2 = aflow[length20:length80]
            self.ax1.plot(x2,y2,'.' '-g')
            # call liner regression for that data set
            slope, intercept, r_value, p_value, std_err = stats.linregress(x2,y2)
            angle_2 = math.degrees(math.atan(slope))

            x2 = sample[length80:finish_at]
            y2 = aflow[length80:finish_at]
            self.ax1.plot(x2,y2,'.' '-b')
            # call liner regression for that data set
            slope, intercept, r_value, p_value, std_err = stats.linregress(x2,y2)
            angle_3 = math.degrees(math.atan(slope))
            return angle_1, angle_2, angle_3
            
     
        self.scrolled_text.delete(1.0, END)
        self.bstats=list()
        self.lables = ['Ttot','Ti','Pif','Tpif','Te','Pef','Tepf','Vt-in','Vt-out','Fvg_v','Fvg_f','vrange','frange','Fvg_v_in','fvg_f_in','vrange_in','frange_in','Cit','cif','trange','frange','Cit_in','cif_in','trange_in','frange_n','Tppef20','Tppef80']
        for seperate_breath in self.breaths:
            sample_time,breath_time, flow,volume,flow_dif = seperate_breath
            breathstat=list()
            sTtot = breath_time[-1] # total breath length
            x_over = find_crossover(flow)
            Ti = breath_time[x_over]
            sPif = max(flow)
            sTpif = breath_time[numpy.argmax(flow)]
            Te = breath_time[-1]-breath_time[x_over]
            sPef = min(flow[x_over:len(flow)])
            sTepf = breath_time[numpy.argmin(flow)] - breath_time[x_over]
            in_Vol = find_volume(0,x_over,breath_time,flow)
            out_Vol = -find_volume(x_over,len(flow),breath_time,flow)
            vrange, flowrange, fvgtng_v, fvgtng_f = find_FVG_TNG(True,x_over,len(volume),volume,flow)
            vrangea, flowrangea, fvgtng_va, fvgtng_fa = find_centroid(False,1,x_over,volume,flow)
            calc1 = fvgtng_v/vrange
            calc2 = fvgtng_f/flowrange
            trange, frange,Ci_t, Ci_f = find_centroid(True,x_over,len(breath_time),breath_time,flow)
            trangea, frangea,Ci_ta, Ci_fa = find_centroid(False,1,x_over,breath_time,flow)
            a1,a2,a3 = get_Slope(numpy.argmin(flow),len(flow),breath_time,flow)
            Tppef20 = 180.0-a1+a2
            Tppef80 = 180.0-a3+a2
            
            breathstat.append(sTtot)
            breathstat.append(Ti),
            breathstat.append(sPif)
            breathstat.append(sTpif)
            breathstat.append(Te)
            breathstat.append(sPef)
            breathstat.append(sTepf)
            breathstat.append(in_Vol)
            breathstat.append(out_Vol)
            breathstat.append(fvgtng_v)
            breathstat.append(fvgtng_f)
            breathstat.append(vrange)
            breathstat.append(flowrange)
            breathstat.append(fvgtng_va)
            breathstat.append(fvgtng_fa)
            breathstat.append(vrangea)
            breathstat.append(flowrangea)
            breathstat.append(Ci_t)
            breathstat.append(Ci_f)
            breathstat.append(trange)
            breathstat.append(frange)
            breathstat.append(Ci_ta)
            breathstat.append(Ci_fa)
            breathstat.append(trangea)
            breathstat.append(frangea)
            breathstat.append(Tppef20)
            breathstat.append(Tppef80)
            self.bstats.append(breathstat)

            self.ax1.plot(Ci_t, Ci_f ,'o' '-r')
            self.ax4.plot(fvgtng_v, fvgtng_f ,'o' '-r')
            self.ax1.plot(Ci_ta, Ci_fa ,'o' '-r')
            self.ax4.plot(fvgtng_va, fvgtng_fa ,'o' '-r')
        
        self.dataPlot.draw()
        data_array = numpy.zeros((len(self.bstats),len(breathstat)))
        for indx, breath in enumerate(self.bstats):
            for indy, item in enumerate(breath):
                data_array[indx][indy] = item
        means = np.mean(data_array, axis=0)
        stdvs = np.std(data_array, axis=0)
        
        line = ("Number of breaths: %.2f \n" %  len(self.bstats))
        self.scrolled_text.insert(END, line)    
        line = ("Smoothed: %.2f \n" %  self.smooth_value)
        self.scrolled_text.insert(END, line)    
        line = ("Start at: %.2f \n" % self.control1.get())
        self.scrolled_text.insert(END, line)    
        line = ("End at: %.2f \n" % self.control2.get())
        self.scrolled_text.insert(END, line) 
        for i, val in enumerate(means):
            line = " "+self.lables[i]+"\t \t"+("%.2f \t" %  val)+(" %.2f \n" %  stdvs[i])
            self.scrolled_text.insert(END, line)    

        



def main():
    ScaleDemo().mainloop()  
    sys.exit()
    
if __name__ == "__main__":
    main()
