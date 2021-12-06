from parse import read_input_file, write_output_file
import os

def solve(tasks, name):
    n = len(tasks)
    total_time = 1440
    profits_so_far = [[0] * (total_time+1) for i in range(n+1)]
    used_tasks = [0] * (n+1)
    
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
                used_tasks[i-1] += 1
            else:
                minutes_late = time + duration - task.get_deadline()
                profit = task.get_late_benefit(minutes_late)

                # Same as max(profits_so_far[i-1][time], profit + profits_so_far[i-1][time-duration])
                # Done for the sake of keeping track of the tasks
                using_profit = profit + profits_so_far[i-1][time-duration]
                not_profit = profits_so_far[i-1][time]

                if(using_profit > not_profit):
                    profits_so_far[i][time] = using_profit
                    used_tasks[i] += 1
                else:
                    profits_so_far[i][time] = not_profit
                    used_tasks[i-1] += 1
                

    total_profit = profits_so_far[n][total_time]

    
    return used_tasks



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