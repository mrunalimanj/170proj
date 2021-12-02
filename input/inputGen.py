from random import *
import pandas as pd

n = 200
deadlines = []
durations = []
profits = []

seed(100)

f = open(str(n) + ".in", "w")

f.write(str(n) + "\n")

for i in range(1, n+1):
    t = randint(1, 1440)
    deadlines.append(t)

    d = randint(1, 60)
    durations.append(d)

    p = round(uniform(0.0001, 99.999), randint(0, 3))
    profits.append(p)

    # Checks
    if t < d:
        print("task" + str(i) + " has deadline < duration")

    task = str(i) + " " + str(t) + " " + str(d) + " " + str(p) + "\n"
    f.write(task)

f.close()

d = {'deadlines': deadlines, 'durations': durations, 'profits': profits}
df = pd.DataFrame(d)

#Metrics
# Median, min, max for deadlines, profits
print("No. of unique deadlines", len(pd.unique(df['deadlines'])))
print("Median of deadlines", df['deadlines'].median())
print("Min deadlines", min(deadlines))
print("Max deadlines", max(deadlines))

print("No. of unique profts", len(pd.unique(df['profits'])))
print("Median of profits", df['profits'].median())
print("Min profits", min(profits))
print("Max profits", max(profits))