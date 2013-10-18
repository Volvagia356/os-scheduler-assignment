import cpuschedule
import misc
import operator

name="Priority-based pre-emptive Shortest Job First"

class Algorithm(cpuschedule.Algorithm):
    def start_process(self):
        cpuschedule.Algorithm.start_process(self)
        #See if any process in queue has shorter busrst time than current, if so, replace current
        if self.process_queue:
            priority_sorted=sorted(self.process_queue,key=operator.attrgetter('priority'))
            shortest=sorted(priority_sorted,key=operator.attrgetter('burst_time'))[0]
            if self.current_process==None or shortest.burst_time<self.current_process.burst_time:
                if self.current_process!=None:
                    self.process_queue.append(self.current_process)
                self.current_process=shortest
                self.process_queue.remove(shortest) 
    
    def stop_process(self):
        cpuschedule.Algorithm.stop_process(self)