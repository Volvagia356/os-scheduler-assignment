import os
import sys
import imp
import misc

#Implementation of CPU scheduler simulation. (Mostly) separated from interface

processes=[]

#Loads scheduler algorithms from 'algorithms' folder
def load_algorithms():
    global algorithms
    algorithms=[]

    for ext in sorted(os.listdir("algorithms")):
        if ext[-3:]==".py" and (ext[0:2]!="__" and ext[-5:]!="__.py"):
            try:
                algorithms.append(imp.load_source(ext[:-3],"algorithms/"+ext))
                #print "Module",ext,"loaded"
            except:
                print "Failed to load", ext
                print sys.exc_info()

#Parent class for algorithms
class Algorithm:
    #Constructor
    def __init__(self):
        self.time=0
        self.processes=[]
        self.new_processes=[]
        self.current_process=None
        self.process_queue=[]
        self.timeline=[]
    
    #Do this to newly added processes
    def add_process(self,process):
        self.processes.append(process)
        self.new_processes.append(process)
    
    #Do this before each time segment
    def start_process(self):
        templist=self.new_processes[:]
        #Check and see if any new processes arrived, add them to queue
        for process in templist:
            if process.arrival_time==self.time:
                self.process_queue.append(process)
                self.new_processes.remove(process)
    
    #Do this after each time segment
    def stop_process(self):
        self.timeline.append([self.time,self.current_process.id,self.current_process.burst_time, self.current_process.turnaround_time,self.current_process.waiting_time])
        #Time counting
        if self.current_process.first_response==0:
            self.current_process.first_response=self.time
        self.time+=1
        self.current_process.burst_time-=1
        self.current_process.turnaround_time+=1
        for process in self.process_queue:
            process.turnaround_time+=1
            process.waiting_time+=1
        #Remove completed processes
        if self.current_process.burst_time==0:
            self.current_process.completion_time=self.time
            self.current_process=None

#Class for processes
class Process:
    def __init__(self):
        #Get process info
        self.arrival_time=misc.get_int("Enter arrival time: ",0,None,"Invalid arrival time!")
        self.burst_time=misc.get_int("Enter burst time: ",1,None,"Invalid burst time!")
        self.orig_burst_time=self.burst_time
        priority=misc.get_int("Enter process priority (1-5, 1=Highest 5=Lowest): ",1,5,"Invalid priority!")
        self.priority=priority
        self.turnaround_time=0
        self.waiting_time=0
        self.completion_time=0
        self.first_response=0