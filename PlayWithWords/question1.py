import sys

filename = sys.argv[1]

f1 = open(filename, 'r')
x = f1.read()
y = x.lower().split()
z = list(set(y))
z.sort(reverse = True)
sys.stdout.write(",".join(z))
