from parse import read_input_file, write_output_file
import os
from functools import cmp_to_key

def solve(tasks, name):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    return findMaxperfect_benefit(tasks, len(tasks), name)

# A utility function that is used for sorting events according to deadline time
def taskComparator(s1, s2):
    if s1.deadline - s1.duration < 1440 and s2.deadline - s2.duration < 1440:
        return s1.deadline < s2.deadline and s1.deadline - s1.duration < s2.deadline - s2.duration
 
# Find the latest task (in sorted array) that doesn't conflict with the task[i]. If there
# is no compatible task, then it returns -1
def latestNonConflict(arr, i):
     
    for j in range(i - 1, -1, -1):
        if arr[j].deadline <= arr[i - 1].deadline - arr[i - 1].duration:
            return j
             
    return -1
 
# The main function that returns the maximum possible perfect_benefit from given array of tasks
def findMaxperfect_benefit(arr, n, name):
     
    # Sort tasks according to deadline time
    arr = sorted(arr, key = cmp_to_key(taskComparator))
    #arr = arr[x for x in arr if ]
    
    final_tasks = []

 
    # Create an array to store solutions of subproblems. 
    table = [None] * n
    # Setting up time (starting at minute 0)
    time_so_far = 0
    # Getting the minutes past the deadline
    minutes_late = time_so_far + arr[0].get_duration() - arr[0].get_deadline()
    
    # table[i] stores the benefit (taking into account timesteps) for tasks till arr[i] (including arr[i])
    # we'll start by assuming we complete the first task
    time_so_far = arr[0].get_duration()
    table[0] = arr[0].get_late_benefit(minutes_late)
 
    # Fill entries in M[] using recursive property
    for i in range(1, n):

        # Start by finding the benefit of including the current task
        minutes_late = time_so_far + arr[i].get_duration() - arr[i].get_deadline()
        inclProf = arr[i].get_late_benefit(minutes_late)

        
        l = latestNonConflict(arr, i)
         
        if l != -1 and l+1 not in final_tasks:
            inclProf += table[l]
            # Deciding if we should add the task or swap it
            if 
            time_so_far += arr[i].get_duration()
            final_tasks.append(l+1)
 
        # Store maximum of including and excluding
        table[i] = max(inclProf, table[i - 1])
 
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
            #print("Output", output)
            write_output_file(output_path, output)