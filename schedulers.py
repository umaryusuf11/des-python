#Authors:
#Ishita Narsiker - GUID: 2579990N - Lab 1
#Umar Yusuf - GUID: 2613065Y - Lab 6

#importing the required modules
import math
from des import SchedulerDES
import event
from process import Process, ProcessStates 
from queue import Queue

# First Come First Serve Scheduler, inherits from SchedulerDES class 
class FCFS(SchedulerDES):
    def scheduler_func(self, cur_event):
        # If the event is new or requesting access to the CPU
        if cur_event.event_type==event.EventTypes.PROC_ARRIVES or cur_event.event_type == event.EventTypes.PROC_CPU_REQ:
            return self.processes[cur_event.process_id]
 
    # Chooses the first item in the list and exectues it.
    def dispatcher_func(self, cur_process):
        # Sets process state to running
        cur_process.process_state = ProcessStates.RUNNING
        # Increments current time by process run time
        self.time += cur_process.run_for(cur_process.remaining_time, self.time)
        time = self.time
        # Terminates the process if it is completed
        if cur_process.remaining_time == 0:
            cur_process.process_state = ProcessStates.TERMINATED
        return event.Event(process_id = (cur_process.process_id), event_time = time, event_type = event.EventTypes.PROC_CPU_DONE)
         
# Shortest job first, this is the same as FCFS, but it sorts the list by the remaining time of the process
class SJF(SchedulerDES):
    def scheduler_func(self, cur_event):
        #If the event is new or requesting access to the CPU
        if cur_event.event_type==event.EventTypes.PROC_ARRIVES or cur_event.event_type == event.EventTypes.PROC_CPU_REQ:
            # Sorts the list of processes by service time.
            self.processes = sorted(self.processes, key=lambda x: x.service_time, reverse=False)
        # Returns the first ready process in the list of processes
        for process in self.processes:
            if process.process_state == ProcessStates.READY:
                    return process
    #Same dispatcher as FCFS but with the difference that it is sorted by remaining time instead of service time
    def dispatcher_func(self, cur_process):
        cur_process.process_state = ProcessStates.RUNNING
        self.time = self.time + cur_process.run_for(cur_process.remaining_time, self.time)
        time = self.time
        cur_process.process_state = ProcessStates.TERMINATED
        return event.Event(process_id = (cur_process.process_id), event_time = time, event_type = event.EventTypes.PROC_CPU_DONE)

# Round - Robin: a preemptive version of FCFS, where the dispatcher preempts the process that is currently running
class RR(SchedulerDES):
    def scheduler_func(self, cur_event):
        # Checks If the event is new or requesting access to the CPU, if so, sorts the list of processes by service time
        if cur_event.event_type==event.EventTypes.PROC_ARRIVES or cur_event.event_type == event.EventTypes.PROC_CPU_REQ:
            return self.processes[cur_event.process_id]

    def dispatcher_func(self, cur_process):
        cur_process.process_state = ProcessStates.RUNNING
        time = cur_process.run_for(self.quantum, self.time) + self.time
        # Adds it back to queue if there is time remaining, else terminate it, and return the event for the CPU to be done
        if cur_process.remaining_time!= 0:
            cur_process.process_state = ProcessStates.READY 

            return event.Event(process_id = (cur_process.process_id), event_time = time, event_type = event.EventTypes.PROC_CPU_REQ)
        else:
            cur_process.process_state = ProcessStates.TERMINATED
            return event.Event(process_id = (cur_process.process_id), event_time = time, event_type = event.EventTypes.PROC_CPU_DONE)

# Shortest Remaining Time First, this is the same as FCFS, but it sorts the list by the remaining time of the process
class SRTF(SchedulerDES):
    # Scheduler called every time a new process arrive 
    def scheduler_func(self, cur_event):
        # Basically SJF scheduler but with remaining time instead of service time
        if cur_event.event_type==event.EventTypes.PROC_ARRIVES or cur_event.event_type == event.EventTypes.PROC_CPU_REQ:
            self.processes = sorted(self.processes, key=lambda x: x.remaining_time, reverse=False)
            for process in self.processes:
                if process.process_state == ProcessStates.READY:
                    return process

    
    def dispatcher_func(self, cur_process):
        time = 0    
        cur_process.process_state = ProcessStates.RUNNING
        #calculate the time until the next process
        time = cur_process.run_for(self.next_event_time()-self.time,self.time) + self.time
        if cur_process.remaining_time != 0:
            cur_process.process_state = ProcessStates.READY
            return event.Event(process_id = (cur_process.process_id), event_time = time, event_type = event.EventTypes.PROC_CPU_REQ)
        else:
            cur_process.process_state = ProcessStates.TERMINATED
            return event.Event(process_id = (cur_process.process_id), event_time = time, event_type = event.EventTypes.PROC_CPU_DONE)
