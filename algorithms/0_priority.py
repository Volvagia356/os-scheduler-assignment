import cpuschedule
import misc
import operator

name="Non Pre-emptive Priority"

class Algorithm(cpuschedule.Algorithm):
    def start_process(self):
        cpuschedule.Algorithm.start_process(self)
        #Set process with top priority as current if no process is running
        if self.current_process==None:
            top=sorted(self.process_queue,key=operator.attrgetter('priority'))[0]
            self.current_process=top
            self.process_queue.remove(top)
    
    def stop_process(self):
        cpuschedule.Algorithm.stop_process(self)