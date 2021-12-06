import sys
import numpy as np
from solver_mm import decide_profit
from parse import read_input_file, read_output_file, write_output_file
import os

TEMP = 60


def calc_profit(order, tasks):
    total_profit = 0
    timestep = 0
    for ig_i in order:
        try:
            total_profit += decide_profit(tasks[ig_i - 1], timestep) 
        except:
            print(ig_i, len(tasks))
            raise

    return total_profit

def get_new_order(old_order, i, j):
    order = [i for i in old_order]
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
    curr_prof = calc_profit(initial_task_order, tasks)
    best_prof = curr_prof
    print(f"initially i had {curr_prof}")
    best_order = initial_task_order
    task_order = initial_task_order

    iters = 0
    for iter_i in range(150):
        #simulated annealing: pick two to swap
        i, j = np.random.choice(num_igloos, 2, replace=False)
        i, j = int(i), int(j)
        new_order = get_new_order(task_order, i, j)
        check = None

        new_prof = calc_profit(new_order, tasks)
        diff = new_prof - curr_prof

        update_chance = TEMP/(iter_i + 1) # should be high for early iterations, lower over time
        accept = np.exp(- diff / update_chance)
        if diff < 0 or np.random.choice(1) < accept:
            curr_prof = new_prof
            task_order = new_order


        if not validate_order(new_order, tasks): # total duration cannot exceed 1440.
            continue # need to resample

        if new_prof > best_prof and validate_order(new_order, tasks):
            # update best
            

            best_prof = new_prof
            
            best_order = new_order



    return best_order, best_prof

def check_output(tasks, order, profit):
    time_now = 0
    prof = calc_profit(order, tasks)
    for i in order:
        ig = tasks[i - 1]
        time_now += ig.duration

    print(f"I now have {prof}")
    # something up with the profit?
    if time_now >= 1440:
        raise Exception(f"profit was expected to be {profit} but was {prof} and time used was {time_now}")
    return True    

def main():
    
    for input_folder in os.listdir('../project-fa21-skeleton/inputs/'):

        if not input_folder.startswith('.'):
            for file in os.listdir(f'../project-fa21-skeleton/inputs/{input_folder}'):
                input_path = f'../project-fa21-skeleton/inputs/{input_folder}' + "/" + file

                if ".DS_Store" not in input_path:
                    print("here")
                    try:
                        tasks = read_input_file(input_path) # this is a list of tasks. 
                    except:
                        print(input_path)
                        raise
                    for output_name in 'profit', 'deadline':
                        output_path = output_name + '/outputs/' + input_folder + "/" + file[:-3] + '.out'
                        initial_order = read_output_file(output_path)
                        initial_order_c = [o - 1 for o in initial_order]
                        output, prof = anneal(tasks, initial_order_c)
                        output = [o + 1 for o in output]
                        check_output(tasks, output, prof)

                        new_output_path = output_name + "_anneal" + '/outputs/' + input_folder + "/" + file[:-3] + '.out'
                        if not os.path.exists(output_name + "_anneal" + '/outputs/' + input_folder + "/"):
                            os.makedirs(output_name + "_anneal" + '/outputs/' + input_folder + "/")
                        
                        try:
                            write_output_file(new_output_path, output)
                        except:
                            print(len(tasks))
                            raise



if __name__ == "__main__":
    main()