#Your implementation goes here
import sys
instance = 2**9
sys.stdout.write("%i\n" % instance)
concept = 2**instance
digits = len(str(concept))
sys.stdout.write("%i\n" % digits)
hypothesis = 3**9 +1
sys.stdout.write("%i\n" % hypothesis)

f1 = open('9Cat-Train.labeled', 'r')
x = f1.read()
f1.close()

x = x.split()
y = []
z = []
ConceptAll = []
for i in range(1,len(x),2):
    y.append(x[i])
while y != []:
    z.append(y[:10])
    y = y[10:]
for i in range(0,len(z)):
    ConceptAll.append(z[i][:9])

f2 = open('partA4.txt', 'w')
n = 0
Concept = []   
for i in range(0,len(ConceptAll)):
    if z[i][9] == 'high':
        for j in range(0,9):
            if Concept == []:
                for k in range(0,9):
                    Concept.append(ConceptAll[i][k])
            if Concept[j] != ConceptAll[i][j]:
                Concept[j] = '?'
    n +=1;
    if n == 30:
        for i in range(len(Concept)):
            f2.write(Concept[i]+'\t')
        f2.write('\n')
        finalConcept = Concept
        n=0
Hyp = finalConcept
f2.close()

filename3 = sys.argv[1]
f3 = open(filename3, 'r')
file3 = f3.read()
f3.close()

file3 = file3.split()
y = []
z = []
high = []
low = []
mis = 0
for i in range(1,len(file3),2):
    y.append(file3[i])
while y != []:
    z.append(y[:10])
    y = y[10:]
for i in range(0,len(z)):
    if z[i][9] == 'high':
        high.append(z[i][:9])
for i in range(0,len(z)):
    if z[i][9] == 'low':
        low.append(z[i][:9])
for i in range(0,len(high)):
    for j in range(0,9):
        if high[i][j] != Hyp[j] and Hyp[j] !='?':
            mis+=1
            break
m = 0
for i in range(0,len(low)):
    for j in range(0,9):
        if low[i][j] == Hyp[j] or Hyp[j] =='?':
            m+=1
    if m == 9: mis +=1
    m = 0
rate =float(mis)/len(z)
sys.stdout.write("%f\n" % rate)


m = 0
ConceptAll =[]
for i in range(0,len(z)):
    ConceptAll.append(z[i][:9])
for i in range(0,len(ConceptAll)):
    for j in range(0,9):
        if Hyp[j] == ConceptAll[i][j] or Hyp[j] == '?':
            m += 1
    if m == 9: sys.stdout.write("high\n")
    else: sys.stdout.write("low\n")
    m = 0

