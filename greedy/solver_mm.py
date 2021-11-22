# code for cs 170
import numpy as np

def parse_inputs():
	
    igloo_count = list(map(int, input().split()))

    data = {
        'deadlines': [0 for _ in range(igloo_count)],
        'durations': [0 for _ in range(igloo_count)],
        'profits': [0 for _ in range(igloo_count)]
    }

    for ig_i in range(igloo_count):
        igloo_info = list(map(int, input().split()))
        data['deadlines'][ig_i] = igloo_info[1]
        data['durations'][ig_i] = igloo_info[2]
        data['profits'][ig_i] = igloo_info[3]


    # turn into numpy arrays? 
    
    data['deadlines'] = np.asarray(data['deadlines'])
    data['durations'] = np.asarray(data['durations'])
    data['profits'] = np.asarray(data['profits'])

    return igloo_count, data


def run_alg_greedy_best_profit(count, data):
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
        
        valid_igloos = [i for i in range(count) if i not in igloos_chosen and data['duration'][i] + time_now > 1440] 
        next_i = valid_igloos[np.argmax(data['profits'][valid_igloos])]
        
        # operate using this igloo.
        igloos_chosen.append(next_i)
        next_ig_info = [data['deadlines'][next_i], data['durations'][next_i], data['profits'][next_i]]
        
        if next_ig_info[0] >= next_ig_info[1] + time_now:
            # good- just add profit.
            profit += next_ig_info[2]

        else:
            exceeded = (next_ig_info[1] + time_now - next_ig_info[0])
            profit += next_ig_info[2] * np.exp(-0.0170 * exceeded) 

        time_now += next_ig_info[1]

    return profit, igloos_chosen


def run_alg_greedy_nearest_deadline(count, data):
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
        
        valid_igloos = [i for i in range(count) if i not in igloos_chosen and data['duration'][i] + time_now > 1440] 
        next_i = valid_igloos[np.argmin(data['deadline'][valid_igloos])]
        
        # operate using this igloo.
        igloos_chosen.append(next_i)
        next_ig_info = [data['deadlines'][next_i], data['durations'][next_i], data['profits'][next_i]]
        
        if next_ig_info[0] >= next_ig_info[1] + time_now:
            # good- just add profit.
            profit += next_ig_info[2]

        else:
            exceeded = (next_ig_info[1] + time_now - next_ig_info[0])
            profit += next_ig_info[2] * np.exp(-0.0170 * exceeded) 

        time_now += next_ig_info[1]

    return profit, igloos_chosen


def main():
    count, data = parse_inputs()
    profit, igloos = run_alg_greedy_best_profit(count, data)
    # profit, igloos = run_alg_greedy_nearest_deadline(count, data)
    [print(ig + 1) for ig in igloos]

