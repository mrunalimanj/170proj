import sys

filepath = sys.argv[1]

with open(filepath, 'r') as f:
    contents = f.readlines()

igloo_num = contents[0] 
s