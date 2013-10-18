import cpuschedule
import misc
import random

name="Lottery"

ticket_assignment={
    1: 5,
    2: 4,
    3: 3,
    4: 2,
    5: 1,
}

class Algorithm(cpuschedule.Algorithm):
    def add_process(self,process):
        cpuschedule.Algorithm.add_process(self,process)
        process.tickets=ticket_assignment[process.priority]
    
    def start_process(self):
        cpuschedule.Algorithm.start_process(self)
        #Randomly get process from queue as current if no process is running
        if self.current_process==None:
            lottery=[]
            for process in self.process_queue:
                for i in range(process.tickets):
                    lottery.append(process)
            selected=random.choice(lottery)
            self.current_process=selected
            self.process_queue.remove(selected)
    
    def stop_process(self):
        cpuschedule.Algorithm.stop_process(self)