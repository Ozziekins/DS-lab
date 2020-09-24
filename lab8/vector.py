# get necessary libraries
from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime
from time import sleep

# prints the local Lamport timestamp
def local_time(counter):
    return ' (LAMPORT_TIME={}, LOCAL_TIME={})'.format(counter,
                                                     datetime.now())

# calculates the new timestamp when a process receives a message.
def calc_get_time_received(recv_time_stamp, counter):
    for id  in range(len(counter)):
        counter[id] = max(recv_time_stamp[id], counter[id])
    return counter

def event(pid, counter):
    # increase the counter of this process in the vector
    counter[pid] += 1
    return counter

# to send messages to another process through a pipe
def send_message(pipe, pid, counter):
    # increase the counter of this process in the vector
    counter[pid] += 1
    # send the message
    pipe.send(('Empty shell', counter))
    return counter

# to receive messages from another process through a pipe
def recv_message(pipe, pid, counter):
    # receive the message
    message, timestamp = pipe.recv()
    counter = calc_get_time_received(timestamp, counter)
    # increase the counter of this process in the vector
    counter[pid] += 1
    return counter

# process a
def process_a(pipe_ab):
    # process a with pid 0
    pid = 0
    # initialize counter to all 0
    counter = [0, 0, 0]
    counter = event(pid, counter)
    counter = send_message(pipe_ab, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe_ab, pid, counter)
    counter = event(pid, counter)
    print("Process a " + format(counter))

# process b
def process_b(pipe_ba, pipe_bc):
    # process b with pid 1
    pid = 1
    # initialize counter to all 0
    counter = [0, 0, 0]
    counter = recv_message(pipe_ba, pid, counter)
    counter = send_message(pipe_ba, pid, counter)
    counter = send_message(pipe_bc, pid, counter)
    counter = recv_message(pipe_bc, pid, counter)
    print("Process b " + format(counter))

# process c
def process_c(pipe_cb):
    # process c with pid 2
    pid = 2
    # initialize counter to all 0
    counter = [0, 0, 0]
    counter = recv_message(pipe_cb, pid, counter)
    counter = send_message(pipe_cb, pid, counter)
    print("Process c " + format(counter))


# main function that runs the three processes
if __name__ == '__main__':
    oneandtwo, twoandone = Pipe()
    twoandthree, threeandtwo = Pipe()

    # initialize the processes
    processa = Process(target=process_a, 
                       args=(oneandtwo,))
    processb = Process(target=process_b, 
                       args=(twoandone, twoandthree))
    processc = Process(target=process_c, 
                       args=(threeandtwo,))

    # start the processes
    processa.start()
    processb.start()
    processc.start()

    # ensure all processes finish before exiting
    processa.join()
    processb.join()
    processc.join()

