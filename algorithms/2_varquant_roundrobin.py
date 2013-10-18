import cpuschedule
import misc
from collections import deque

name="Variable Quantum Round Robin"

quantum_assignment={
    1: 5,
    2: 4,
    3: 3,
    4: 2,
    5: 1,
}

class Algorithm(cpuschedule.Algorithm):
    def __init__(self):
        cpuschedule.Algorithm.__init__(self)
        self.current_quantum=0
        self.process_queue=deque()
    
    def add_process(self,process):
        cpuschedule.Algorithm.add_process(self,process)
        process.quantum=quantum_assignment[process.priority]
        
    
    def start_process(self):
        cpuschedule.Algorithm.start_process(self)
        #Replace current process with next in queue if time quantum is up
        if self.current_quantum==0 and self.current_process!=None:
            self.process_queue.append(self.current_process)
            self.current_process=None
        if self.current_process==None:
            self.current_process=self.process_queue.popleft()
            self.current_quantum=self.current_process.quantum
    
    def stop_process(self):
        cpuschedule.Algorithm.stop_process(self)
        self.current_quantum-=1