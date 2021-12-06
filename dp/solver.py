from parse import read_input_file, write_output_file
import os

def decide_profit(ig, time_now):
    if ig.deadline >= ig.duration + time_now:
        exp_profit = ig.perfect_benefit
    else:
        exceeded = ig.duration + time_now - ig.deadline
        exp_profit = ig.perfect_benefit * np.exp(-0.0170 * exceeded) 
    
    return exp_profit

    
def solve(tasks, name):
    n = len(tasks)
    total_time = 1440
    profits_so_far = [[0] * (total_time+1) for i in range(n+1)]
    profits_used = [0]* (n+1)
    
    ###########Sorting#############
    sorted_tasks = sorted(tasks, key = lambda x: x.get_deadline())

    for i in range(1, n+1):
        for time in range(1, total_time+1):
            # Accesing task i-1 since we are starting at 1 and going to n
            task = sorted_tasks[i-1]
            duration = task.get_duration()
            # Don't include task i-1 if its duration isn't as large as time so far
            if duration > time: 
                profits_so_far[i][time] = profits_so_far[i-1][time]
            else:
                minutes_late = time + duration - task.get_deadline()
                profit = task.get_late_benefit(minutes_late)
                print('minutes_late: ', minutes_late)
                print('profit: ', profit)
                #profit = task.get_max_benefit()

                # Same as max(profits_so_far[i-1][time], profit + profits_so_far[i-1][time-duration])
                # Done for the sake of keeping track of the tasks
                using_profit = profit + profits_so_far[i-1][time-duration]
                not_profit = profits_so_far[i-1][time]

                # Add the current task
                if(using_profit > not_profit):
                    profits_so_far[i][time] = using_profit
                    # if i == n:
                    #     print('task :', i)
                # Don't add the current task
                else:
                    profits_so_far[i][time] = not_profit
            
            #profits_used[i] = profit
                

    total_profit = profits_so_far[n][total_time]

    
    return 0



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