from parse import read_input_file, write_output_file
import os
from functools import cmp_to_key

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    return findMaxperfect_benefit(tasks, len(tasks))

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
def findMaxperfect_benefit(arr, n):
     
    # Sort tasks according to deadline time
    arr = sorted(arr, key = cmp_to_key(taskComparator))
    #arr = arr[x for x in arr if ]
    final_tasks = []
 
    # Create an array to store solutions of subproblems. table[i] stores the perfect_benefit for tasks till arr[i]
    # (including arr[i])
    table = [None] * n
    table[0] = arr[0].perfect_benefit
 
    # Fill entries in M[] using recursive property
    for i in range(1, n):
         
        # Find perfect_benefit including the current task
        inclProf = arr[i].perfect_benefit
        l = latestNonConflict(arr, i)
         
        if l != -1:
            inclProf += table[l]
            if l+1 not in final_tasks:
                final_tasks.append(l+1)
 
        # Store maximum of including and excluding
        table[i] = max(inclProf, table[i - 1])
 
    # Store result and free dynamic memory
    # allocated for table[]
    result = table[n - 1]
 
    return final_tasks



# Here's an example of how to run your solver.
if __name__ == '__main__':
    for folder in os.listdir('inputs/'):
        for filename in os.listdir('inputs/' + folder + '/'):
            input_path = 'inputs/' + folder + '/' + filename
            output_path = 'outputs/' + folder + '/' + filename[:-3] + '.out'
            tasks = read_input_file(input_path)
            output = solve(tasks)
            print("Output", output)
            write_output_file(output_path, output)