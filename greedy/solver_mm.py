# code for cs 170
import numpy as np
from parse import read_input_file, write_output_file
import os

def decide_profit(ig, time_now):
    if ig.deadline >= ig.duration + time_now:
        exp_profit = ig.perfect_benefit
    else:
        exceeded = ig.duration + time_now - ig.deadline
        exp_profit = ig.perfect_benefit * np.exp(-0.0170 * exceeded) 
    
    return exp_profit

def run_alg_greedy_best_profit(tasks):
    count = len(tasks)
    time_now = 0
    profit = 0
    igloos_chosen = [] # this list will be 0-indexed. 
    # this approach: best profit available at this time. 
    # need to remember I can't reuse an igloo

    while time_now < 1440 or len(igloos_chosen) >= count:

        # select igloo:

        # deciding to only go through igloos that are:
        # * not chosen yet in a previous iteration of while loop
        # * duration makes it a valid igloo
        # haven't thought about something re: deadlines
        

        valid_igloos = [i for i in range(count) if i not in igloos_chosen and tasks[i].duration + time_now < 1440] 
        if len(valid_igloos) == 0:
            break
        profits_at_this_time = []
        for ig_i in valid_igloos:
            ig = tasks[ig_i]
            profits_at_this_time.append((ig_i, decide_profit(ig, time_now)))
        
        next_i, profit_next_i = max(profits_at_this_time, key = lambda ig: ig[1])
        

        # operate using this igloo.
        igloos_chosen.append(next_i)
        next_ig = tasks[next_i]
        #print(next_i, next_ig)
        profit += decide_profit(next_ig, time_now)

        time_now += next_ig.duration
    

    return igloos_chosen, profit, time_now


def run_alg_greedy_nearest_deadline(tasks):
    count = len(tasks)
    time_now = 0
    profit = 0
    igloos_chosen = [] # this list will be 0-indexed. 
    # this approach: best profit available at this time. 
    # need to remember I can't reuse an igloo
    

    while time_now < 1440 or len(igloos_chosen) >= count:

        # select igloo:

        # deciding to only go through igloos that are:
        # * not chosen yet in a previous iteration of while loop
        # * duration makes it a valid igloo
        # haven't thought about something re: deadlines
        
        valid_igloos = [(i, tasks[i]) for i in range(count) if i not in igloos_chosen and tasks[i].duration + time_now < 1440] 
        if len(valid_igloos) == 0:
            break
        next_i, next_ig = min(valid_igloos, key = lambda elem: elem[1].deadline) 
        # TODO: what if we want to just skip a task with a super early deadline, though?

    
        # operate using this igloo.
        #print(next_i, next_ig)
        igloos_chosen.append(next_i)
        profit += decide_profit(next_ig, time_now)

        time_now += next_ig.duration

    return igloos_chosen, profit, time_now


def check_output(tasks, order, profit, time):
    prof = 0
    time_now = 0
    for i in order:
        
        ig = tasks[i - 1]
        prof += decide_profit(ig, time_now)

        time_now += ig.duration
    if profit != prof or time_now != time:
        raise Exception(f"profit was expected to be {profit} but was {prof} and time used was supposed to be {time} but is actually {time_now}")
    return True
    

def main():
    for input_folder in os.listdir('../project-fa21-skeleton/inputs/'):
        if ".DS_Store" in input_folder:
                continue
        for file in os.listdir(f'../project-fa21-skeleton/inputs/{input_folder}'):
            input_path = f'../project-fa21-skeleton/inputs/{input_folder}' + "/" + file
            if ".DS_Store" in input_path:
                continue
            try:
                tasks = read_input_file(input_path) # this is a list of tasks. 
                
            except:
                print(input_path)
                raise

            for solver, name in [(run_alg_greedy_best_profit, 'profit'), (run_alg_greedy_nearest_deadline, 'deadline')]:
                output_path = name + '/outputs/' + input_folder + "/" + file[:-3] + '.out'
                output, profit, time_now = solver(tasks)
                output = [o + 1 for o in output]
                # verify output:
                check_output(tasks, output, profit, time_now)
                print(len(output), profit)
                if not os.path.exists(name + '/outputs/' + input_folder + "/"):
                    os.makedirs(name + '/outputs/' + input_folder + "/")
                write_output_file(output_path, output)



if __name__ == "__main__":
    main()