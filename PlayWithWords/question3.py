import sys
filename1 = sys.argv[1]
f1 = open(filename1, 'r')
x = f1.read()
f1.close()

filename2 = sys.argv[2]
f2 = open(filename2, 'r')
s = f2.read()
f2.close()

y = x.lower().split()
z = list(set(y))
z.sort(reverse = True)

k=[]
s = s.split()
for word in z:
    if word not in s:
        k.append(word)

z = k
m = []
for i in range(len(z)):
    m.append(y.count(z[i]))

for i in range(len(z)-1):
    sys.stdout.write("%s:%s," % (z[i],m[i]))
sys.stdout.write("%s:%s" %(z[-1],m[-1]))

