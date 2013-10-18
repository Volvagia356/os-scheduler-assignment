from __future__ import division
import sys
import cpuschedule #Implementation
import misc
from copy import copy
from prettytable import PrettyTable #This external library provides nice ASCII tables

#This file is the interface, separated (mostly) from the implementation (cpuschedule)

cpuschedule.load_algorithms()

#Main menu
def main_menu():
    options=[
        ("Intialize process list",get_processes),
        ("Run a single simulation",single_simulation),
        ("Compare algorithms",compare_algorithms),
        ("Quit",sys.exit)
    ]
    print "Main Menu:"
    selection=misc.show_menu([option[0] for option in options],"Selection: ","Invalid selection!")
    misc.clear_screen()
    options[selection][1]()

#Get processes from the user
def get_processes():
    cpuschedule.processes=[]
    process_count=misc.get_int("Enter process count: ",1)
    for i in range(process_count):
        print "\nEnter details for process {}".format(i+1)
        process=cpuschedule.Process()
        process.id=i+1
        cpuschedule.processes.append(process)

#Run a simulation of a single algorithm
def single_simulation():
    if not verify_processes(): return False
    module=select_algorithm()
    scheduler=module.Algorithm()
    for process in cpuschedule.processes:
        scheduler.add_process(copy(process))
    simulation(scheduler,True)
    print_end_result(scheduler)

#Run all algorithms and output summary only
def compare_algorithms():
    if not verify_processes(): return False
    #Prepare tables
    timeline_table=PrettyTable()
    avg_table=PrettyTable(["Algorithm","Avg. Turnaround","Avg. Waiting"])
    timeline_table.add_column("Time",[i for i in range(sum([process.burst_time for process in cpuschedule.processes]))])
    timelines=[]
    #Load data
    for i in range(len(cpuschedule.algorithms)):
        scheduler=cpuschedule.algorithms[i].Algorithm()
        for process in cpuschedule.processes:
            scheduler.add_process(copy(process))
        simulation(scheduler,False)
        timeline=[time[1] for time in scheduler.timeline]
        timeline_table.add_column(str(i+1),timeline)
        timelines.append(timeline)
        avg_turnaround=sum(process.turnaround_time for process in scheduler.processes)/len(scheduler.processes)
        avg_waiting=sum(process.waiting_time for process in scheduler.processes)/len(scheduler.processes)
        avg_table.add_row([i+1,avg_turnaround,avg_waiting])
    #Print tables
    print "Timeline:"
    print timeline_table
    print "\nAlgorithm Legend:"
    for i in range(len(cpuschedule.algorithms)):
        print "{} - {}".format(i+1,cpuschedule.algorithms[i].name)
    print "\nAverages:"
    print avg_table
    try:
        output_html(timelines,timeline_table,avg_table)
        print "\nWritten summary.html"
    except IOError, e:
        print "\nError writing summary.html"
        print e
    raw_input("Press ENTER to return...")

def output_html(timeline,timeline_table,avg_table):
    f=open("summary.html","w")
    
    #Write headers
    f.write("<html><head><title>Scheduler Simulation</title>")
    f.write("<style>table {border-collapse:collapse} table,td {border: 1px solid;}</style></head>")
    f.write("<body><h1>Scheduler Simulation</h1>")
    f.write("<h2>Algorithm Legend</h2><ol>")
    
    #Write legend
    for algorithm in cpuschedule.algorithms:
        f.write("<li>{}</li>".format(algorithm.name))
    f.write("</ol><h2>Timeline</h2>")
    f.write(timeline_table.get_html_string())
    
    #Write gantt chart
    f.write("<h2>Gantt Charts</h2>")
    for i in range(len(cpuschedule.algorithms)):
        prev_id=None
        width=30
        f.write('{}<table><tr>'.format(cpuschedule.algorithms[i].name))
        for id in timeline[i]:
            if prev_id!=None and id!=prev_id:
                f.write('<td width="{}px">{}</td>'.format(width,prev_id))
                width=30
            elif id==prev_id:
                width+=30
            prev_id=id
        f.write('<td width="{}px">{}</td>'.format(width,prev_id))
        f.write("</tr></table>")
    
    #Write averages
    f.write("<h2>Averages</h2>")
    f.write(avg_table.get_html_string())
    f.write("</body></html>")
    f.close()

#Verifies that there's enough processes before running
def verify_processes():
    if len(cpuschedule.processes)<1:
        print "You need to add at least 1 process!"
        raw_input ("Press ENTER to return...")
        return False
    else: return True

#Shows menu to select an algorithm
def select_algorithm():
    print "Select a scheduling algorithm:"
    selection=misc.show_menu([algorithm.name for algorithm in cpuschedule.algorithms],"Algorithm selection: ","Invalid selection!")
    return cpuschedule.algorithms[selection]

#Shows currently running process and queue
def show_status(scheduler):
    misc.clear_screen()
    columns=["Status","Process","R.Burst","Turnaround","Waiting"]
    print "Current time:",scheduler.time
    process_table=PrettyTable(columns)
    current=scheduler.current_process
    process_table.add_row(["Current",current.id,current.burst_time,current.turnaround_time,current.waiting_time])
    for process in scheduler.process_queue:
        process_table.add_row(["Queue",process.id,process.burst_time,process.turnaround_time,process.waiting_time])
    print process_table
    raw_input("Press ENTER to continue...")

#Prints end result of simulation
def print_end_result(scheduler):
    misc.clear_screen()
    print "End result:"
    columns=["Process","Burst","Arrival","1st Response","Completion","Turnaround","Waiting"]
    table=PrettyTable(columns)
    for process in scheduler.processes:
        table.add_row([process.id,process.orig_burst_time,process.arrival_time,process.first_response,process.completion_time,process.turnaround_time,process.waiting_time])
    print table
    print "Average turnaround:", sum(process.turnaround_time for process in scheduler.processes)/len(scheduler.processes)
    print "Average waiting:", sum(process.waiting_time for process in scheduler.processes)/len(scheduler.processes)
    raw_input("Press ENTER to continue...")
    timeline_columns=["Time","Process","Burst","Turnaround","Waiting"]
    timeline_table=PrettyTable(timeline_columns)
    for row in scheduler.timeline:
        timeline_table.add_row(row)
    print "Timeline:"
    print timeline_table
    raw_input("Press ENTER to return...")

#Simulation loop
def simulation(scheduler,interactive=True):
    while True:
        scheduler.start_process()
        if interactive: show_status(scheduler)
        scheduler.stop_process()
        if len(scheduler.process_queue)==0 and len(scheduler.new_processes)==0 and scheduler.current_process==None: break;

#Main
def main():
    misc.clear_screen()
    print "OS Scheduler Simulator"
    print "(C) Raymond Choo Juan Yong (1112700769) 2013\n"
    raw_input("Press ENTER to continue...")
    while True:
        misc.clear_screen()
        main_menu()

#Only run if file is run directly, and not imported
if __name__=="__main__":
    try:
        main()
    except (KeyboardInterrupt,EOFError):
        print "\nInterrupted by user. Exiting."