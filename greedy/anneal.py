from os import curdir
import numpy as np
import sys

TEMP = 60

# run on command line with anneal.py path/to/input.in path/to/soln.out
def parse_input(input_file):
    with open(input_file, 'r') as f:
        num_igloos = int(f.readline()[:-1])
        igloos = f.readlines()
    
    return num_igloos, igloo_data 


def parse_soln(initial_output_path):

    # "unpickle" greedy solution:
    with open(greedy_soln, 'r') as g:
        initial_task_order = list(g.readlines()) # not sure what format this will appear in
        # also, make sure there is no bottom /new line, that could get improperly parsed


    return initial_task_order

def calc_profit(order, igloo_data):
    total_profit = 0
    timestep = 0
    for ig in order:
        prof_ig, duration_ig, deadline_ig = igloo_data["profit"][ig], igloo_data["duration"][ig], igloo_data["deadline"][ig]:

        if timestep + duration_ig >= deadline_ig:
            # good- just add profit.
            total_profit += prof_ig

        else:
            exceeded = (duration_ig + time_now - deadline_ig)
            total_profit += prof_ig * np.exp(-0.0170 * exceeded) 
    
    return total_profit

def get_new_order(order, i, j):
    if i in order and j in order:
        # clean swap
        ind_i, ind_j = order.index(i), order.index(j)
        order[ind_i], order[ind_j] = j, i
        return order


    elif i in order or j in order:
        # how to swap? if one of the tasks wasnt even able to be scheduled?
        # let's just try a swap out for right now
        
        if i in order:
            ind_i = order.index(i)
            order[ind_i] = j
            
        else:
            ind_j = order.index(j)
            order[ind_j] = i
        
        return order

    else:
        return order # no point in switching, need to resample 

def validate_order(order):
    total_time = 0 
    for ig in order:
        total_time += igloo_data["duration"][ig]
    return total_time < 1440
    


def anneal(input_file, initial_output_path):
    num_igloos, igloo_data = parse_input(input_file)

    # get number of tasks - helps to have this number to properly greedily sample

    initial_task_order = parse_soln(initial_output_path)
    task_order = initial_task_order = [int(t[:-1]) for t in initial_task_order]
    # okay, now we have numbers and they are ordered.
    tasks_currently_scheduled = len(initial_task_order)
    curr_prof = total_profit = calc_profit(initial_task_order, igloo_data)

    iters = 0
    while curr_prof < total_profit * 3 or iters < 250:
        #simulated annealing: pick two to swap
        i, j = np.random.choice(num_igloos, 2, replace=False)
        new_order = get_new_order(task_order, i, j)
        if not validate_order(new_order): # total duration cannot exceed 1440.
            continue # need to resample 
        new_prof = calc_profit(new_order, igloo_data)
        if curr_prof == new_prof:
            continue # need to resample

        elif curr_prof > new_prof:
            task_order = new_order
            continue


        elif new_prof > curr_prof:
            iters += 1
            # something with TEMP - needs to be more continuous of an aggregaration than just +1 for each bad overextension
            task_order = new_order
            continue

    return task_order

def save_output(order, initial_output_path):
    # will overwrite first set of outputs we passed in to optimize 
    with open(initial_output_path, "w") as f:
        f.write(order)


def main():
    input_file = sys.argv[1]
    initial_output_path = sys.argv[2]
    new_order = anneal(input_file, initial_output_path)
    save_output(new_order)

    

    







