import sys
import numpy as np
from solver import decide_profit
from parse import read_input_file, read_output_file, write_output_file
import os



def calc_profit(order, tasks): # 1-indexed
    total_profit = 0
    timestep = 0
    for ig_i in order:
        try:
            total_profit += decide_profit(tasks[ig_i - 1], timestep) 
        except:
            print(ig_i, len(tasks))
            raise

    return total_profit

def calc_time_used(order, tasks): # 0-indexed
    total_time = 0
    for ig in order:
        total_time += tasks[ig].duration
    return total_time


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
            order.append(i)
            
        else:
            ind_j = order.index(j)
            order[ind_j] = i
            order.append(j)
        
        return order

    else:
        return order # no point in switching, need to resample 

def validate_order(order, tasks):
    total_time = calc_time_used(order, tasks)
    return total_time <= 1440
    

def anneal(tasks, initial_task_order):
    num_igloos = len(tasks)

    # get number of tasks - helps to have this number to properly greedily sample
    # okay, now we have numbers and they are ordered.
    # tasks_currently_scheduled = len(initial_task_order)
    curr_prof = calc_profit([o + 1 for o in initial_task_order], tasks)
    best_prof = curr_prof
    # print(f"initially i had {curr_prof}")
    best_order = [j for j in initial_task_order]
    task_order = [j for j in initial_task_order]

    temp = 200
    t_current = temp
    t_min = 30
    iter_i = 0
    total_iters = 800
    curr_time = calc_time_used(initial_task_order, tasks)
    best_time =  calc_time_used(initial_task_order, tasks)

    while iter_i < total_iters and t_current > t_min:
        
        i, j = np.random.choice(num_igloos, 2, replace=False)
        i, j = int(i), int(j)
        new_order = get_new_order(task_order, i, j)
        
        new_prof = calc_profit([p + 1 for p in new_order], tasks)
        diff = new_prof - curr_prof
        new_time = calc_time_used(new_order, tasks)

        accept = np.exp(diff / t_current)
        
        if np.random.uniform(0, 1) < accept and validate_order(new_order, tasks): # or diff < 0?
            curr_prof = new_prof
            curr_time = new_time
            task_order = [o for o in new_order]


        if not validate_order(new_order, tasks): # total duration cannot exceed 1440.
            continue # need to resample


        elif new_prof > best_prof and validate_order(new_order, tasks):
            # update best
            best_prof = new_prof
            best_time = new_time
            best_order = [o for o in new_order]

        t_current = t_min + (temp - t_min) * (total_iters - iter_i)/total_iters
        iter_i += 1

    return best_order, best_prof

def check_output(tasks, order, profit): # tasks are now 1-indexed
    time_now = calc_time_used([o - 1 for o in order], tasks)
    prof = calc_profit(order, tasks)

    # print(f"I now have {prof}")
    # something up with the profit?
    if time_now > 1440:
        raise Exception(f"profit was expected to be {profit} but was {prof} and time used was {time_now}")
    return order    

def main():
    reverts = 0
    improvements = 0
    for input_folder in os.listdir('inputs/'):

        if not input_folder.startswith('.'):
            for file in os.listdir(f'inputs/{input_folder}'):
                input_path = f'inputs/{input_folder}' + "/" + file

                if ".DS_Store" not in input_path:
                    try:
                        tasks = read_input_file(input_path) # this is a list of tasks. 
                    except:
                        print(input_path)
                        raise
                    
                    output_path = 'outputs/' + input_folder + "/" + file[:-3] + '.out'
                    initial_order = read_output_file(output_path)

                    initial_order_c = [o - 1 for o in initial_order]
                    output, prof = anneal(tasks, initial_order_c)
                    output = [o + 1 for o in output]
                    output_fix = check_output(tasks, output, prof)
                    
                    if calc_profit(output_fix, tasks) < calc_profit(initial_order, tasks): # double check: if not good, don't bother using
                        output_fix = initial_order
                        reverts +=1
                    else:
                        print(calc_profit(output_fix, tasks) - calc_profit(initial_order, tasks) > 1)
                        improvements += 1

                    new_output_path = "anneal/outputs/" + input_folder + "/" + file[:-3] + '.out'
                    if not os.path.exists("anneal/outputs/" + input_folder + "/"):
                        os.makedirs("anneal/outputs/" + input_folder + "/")
                    
                    try:
                        write_output_file(new_output_path, output_fix)
                    except:
                        print(output)
                        print(output_fix)
                        raise

    print(reverts, improvements)



if __name__ == "__main__":
    main()