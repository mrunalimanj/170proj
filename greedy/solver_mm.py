# code for cs 170
import numpy as np
from parse import read_input_file, write_output_file


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
        
        valid_igloos = [i for i in range(count) if i not in igloos_chosen and tasks[i].duration + time_now > 1440] 
        profits_at_this_time = []
        for ig_i in valid_igloos:
            ig = tasks[ig_i]
            if ig.deadline >= ig.duration + time_now:
                exp_profit = ig.profit
            else:
                exceeded = ig.duration + time_now - ig.deadline
                exp_profit = ig.profit * np.exp(-0.0170 * exceeded) 

            profits_at_this_time.append((ig_i, exp_profit))

        next_i, profit_next_i = max(profits_at_this_time, key = lambda ig: ig[1])
        
        # operate using this igloo.
        igloos_chosen.append(next_i)
        next_ig = tasks[ig_i]
        profit += profit_next_i

        time_now += next_ig.duration
    

    return profit, igloos_chosen


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
        
        valid_igloos = [(i, tasks[i]) for i in range(count) if i not in igloos_chosen and data['duration'][i] + time_now > 1440] 
        
        next_i, next_ig = min(valid_igloos, key = lambda elem: elem[1].deadline) 
        # TODO: what if we want to just skip a task with a super early deadline, though?

    
        # operate using this igloo.
        igloos_chosen.append(next_i)

        if next_ig.deadline >= next_ig.duration + time_now:
            # good- just add profit.
            profit += next_ig.profit

        else:
            exceeded = (next_ig.duration + time_now - next_ig.deadline)
            profit += next_ig.profit * np.exp(-0.0170 * exceeded) 

        time_now += next_ig.duration

    return profit, igloos_chosen


def main():
    for input_folder in os.listdir('../project-fa21-skeleton/inputs/'):
        for file in os.listdir(f'../project-fa21-skeleton/inputs/{input_folder}'):
            input_path = '../project-fa21-skeleton/inputs/{input_folder}' + "/" + file
            tasks = read_input_file(input_path) # this is a list of tasks. 

            for solver, name in [(run_alg_greedy_best_profit, 'profit'), (run_alg_greedy_nearest_deadline, 'deadline')]:
                output_path = name + '/outputs/' + input_path[:-3] + '.out'
                output = solver(tasks)
                write_output_file(output_path, output)