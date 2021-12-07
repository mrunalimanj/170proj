from parse import read_input_file, write_output_file
import os
from functools import cmp_to_key
import math

def solve(tasks, name):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    return findMaxperfect_benefit(tasks, len(tasks), name)

# Sorting events by deadline only
def taskComparator(s1, s2):
    start_1 = s1.get_deadline() - s1.get_duration()
    start_2 = s2.get_deadline() - s2.get_duration()
    if  start_1 < 1440 and  start_2 < 1440 and s1.get_deadline() <= 1440 and s2.get_deadline() <= 1440:
        return s1.get_deadline() < s2.get_deadline()
        
        #return s1.deadline < s2.deadline and s1.deadline - s1.duration < s2.deadline - s2.duration
 
# Find the recent task (in sorted array) that doesn't conflict with the task[k] using binary search. If there
# is no compatible task, then it returns -1
def recentNonConflict(arr, k):

    i, j = 0, k - 1
    start = arr[k].get_deadline() - arr[k].get_duration()

    while i <= j:
        m = (i+j) // 2
        if arr[m].get_deadline() > start:
            j = mid - 1
        else:
            if arr[m + 1].get_deadline() <= start:
                i = m + 1
            else:
                return m
    return -1

# The main function that returns the maximum possible perfect_benefit from given array of tasks
def findMaxperfect_benefit(arr, n, name):
     
    # Sort tasks according to deadline time
    arr = sorted(arr, key = cmp_to_key(taskComparator))
    final_tasks = []

    # Create an array to store solutions of subproblems. 
    table = [None] * n
    # Setting up time (starting at minute 0)
    time_so_far = 0

    # table[i] stores the benefit (taking into account timesteps) for tasks till arr[i] (including arr[i])
    # Cannot assume we complete the first task
    #time_so_far = arr[0].get_duration()
 
    # Fill entries
    for i in range(1, n):
        # Start by finding the benefit of including the current task
        inclProfit = 0

        next_task = recentNonConflict(arr, i)

        if next_task != -1 and next_task+1 not in final_tasks:
            minutes_late = time_so_far + arr[next_task].get_duration() - arr[next_task].get_deadline()
            if minutes_late <= 0:
                inclProfit += arr[next_task].get_max_benefit()
            else:
                inclProfit += arr[next_task].get_late_benefit(minutes_late)
        
            # Deciding if we should add the task or swap it
            table[i] = max(inclProfit, table[i - 1])
            
            if max(inclProfit, table[i - 1]) == inclProfit:
                time_so_far += arr[i].get_duration()
                final_tasks.append(next_task) #should we add next_task or next_task + 1? 
 
 
    # Store result and free dynamic memory
    # allocated for table[]
    result = table[n - 1]
    #print('Result for file {}: {}'.format(name, result))
    print('Time so far', time_so_far)
    return final_tasks



# Here's an example of how to run your solver.
if __name__ == '__main__':
    for folder in os.listdir('inputs/'):
        for filename in os.listdir('inputs/' + folder + '/'):
            input_path = 'inputs/' + folder + '/' + filename
            output_path = 'outputs/' + folder + '/' + filename[:-3] + '.out'
            tasks = read_input_file(input_path)
            output = solve(tasks, filename[:-3])
            print("Output", output)
            #write_output_file(output_path, output)