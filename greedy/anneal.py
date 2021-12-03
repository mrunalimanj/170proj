import sys
import numpy as np
from parse import read_input_file, read_output_file, write_output_file


TEMP = 60

# run on command line with anneal.py path/to/input.in path/to/soln.out

def calc_profit(order, tasks):
    total_profit = 0
    timestep = 0
    ## TODO: fix this 
    for ig_i in order:
        ig = tasks[ig_i]
        if ig.deadline >= ig.duration + timestep:
                total_profit += ig.profit
        else:
            exceeded = ig.duration + timestep - ig.deadline
            total_profit += ig.profit * np.exp(-0.0170 * exceeded) 

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

def validate_order(order, tasks):
    total_time = 0 
    for ig in order:
        total_time += tasks[ig].duration
    return total_time < 1440
    

def anneal(tasks, initial_task_order):
    num_igloos = len(tasks)

    # get number of tasks - helps to have this number to properly greedily sample
    # okay, now we have numbers and they are ordered.
    # tasks_currently_scheduled = len(initial_task_order)
    curr_prof = total_profit = calc_profit(initial_task_order, tasks)

    iters = 0
    while curr_prof < total_profit * 3 or iters < 250:
        #simulated annealing: pick two to swap
        i, j = np.random.choice(num_igloos, 2, replace=False)
        new_order = get_new_order(task_order, i, j)
        if not validate_order(new_order, tasks): # total duration cannot exceed 1440.
            continue # need to resample 
        new_prof = calc_profit(new_order, tasks)
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

def main():
    for input_folder in os.listdir('../project-fa21-skeleton/inputs/'):
        for file in os.listdir(f'../project-fa21-skeleton/inputs/{input_folder}'):
            input_path = '../project-fa21-skeleton/inputs/{input_folder}' + "/" + file
            tasks = read_input_file(input_path) # this is a list of tasks. 
            for output_name in 'profit', 'deadline':
                output_path = output_name + '/outputs/' + input_path[:-3] + '.out'
                initial_order = read_output_file(output_path)
                output = anneal(tasks, initial_order)
                write_output_file(output_path, output)


    

