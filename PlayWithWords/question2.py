import sys

filename = sys.argv[1]
f = open(filename, 'r')
x = f.read()
y = x.lower().split()
z = list(set(y))
z.sort(reverse = True)
m = []
for i in range(0, len(z)):
    m.append(y.count(z[i]))

for i in range(len(z)-1):
    sys.stdout.write("%s:%s," % (z[i],m[i]))
sys.stdout.write("%s:%s" %(z[-1],m[-1]))

