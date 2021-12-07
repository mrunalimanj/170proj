from parse import read_input_file, write_output_file
import os
import numpy as np

def decide_profit(ig, time_now):
    if ig.deadline >= ig.duration + time_now:
        exp_profit = ig.perfect_benefit
    else:
        exceeded = ig.duration + time_now - ig.deadline
        exp_profit = ig.perfect_benefit * np.exp(-0.0170 * exceeded) 
    
    return exp_profit

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

def solve(tasks, name):
    n = len(tasks)
    total_time = 1440
    profits_so_far = [[0] * (total_time+1) for i in range(n+1)]
    profits_used = [[0] * (total_time+1) for i in range(n+1)]
    final_tasks = []
    
    ###########Sorting#############
    #valid_tasks = [task for task in tasks if task.get_deadline() <= 1440 and (x.get_deadline()-x.get_duration()) < 1440]
    sorted_tasks = sorted(tasks, key = lambda x: x.get_deadline())


    for i in range(1, n+1):
        for time in range(1, total_time+1):
            # Accessing task i-1 since we are starting at 1 and going to n
            task = sorted_tasks[i-1]
            duration = task.get_duration()
            # Don't include task i-1 if its duration isn't as large as time so far
            if duration > time: 
                profits_so_far[i][time] = profits_so_far[i-1][time]
            else:
                minutes_late = time + duration - task.get_deadline()
                profit = task.get_late_benefit(minutes_late)
                # print('minutes_late: ', minutes_late)
                # print('profit: ', profit)
                #profit = task.get_max_benefit()

                # Same as max(profits_so_far[i-1][time], profit + profits_so_far[i-1][time-duration])
                # Done for the sake of keeping track of the tasks
                using_profit = profit + profits_so_far[i-1][time-duration]
                not_profit = profits_so_far[i-1][time]

                # Add the current task
                if(using_profit > not_profit):
                    profits_so_far[i][time] = using_profit
                    profits_used[i][time] = 1;
                    
                # Don't add the current task
                else:
                    profits_so_far[i][time] = not_profit
                

    total_profit = profits_so_far[n][total_time]

    t = total_time
    final_time = 0
    for i in range(n, 0, -1):
        if (profits_used[i][t] == 1):
            task = sorted_tasks[i-1]
            task_id = task.get_task_id()
            final_tasks.append(task_id)
            final_time += task.get_duration()

            t -= task.get_duration()

    final_tasks.reverse()

    return final_tasks



# Here's an example of how to run your solver.
if __name__ == '__main__':
    for folder in os.listdir('inputs/'):
        for filename in os.listdir('inputs/' + folder + '/'):
            input_path = 'inputs/' + folder + '/' + filename
            output_path = 'outputs/' + folder + '/' + filename[:-3] + '.out'
            tasks = read_input_file(input_path)
            output = solve(tasks, filename[:-3])
            #print(check_output(tasks, output[0], output[1], 1440))
            #print("Output", output)
            write_output_file(output_path, output)