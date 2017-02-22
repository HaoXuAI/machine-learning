import sys
import math

filename = sys.argv[1]
f1 = open(filename, 'r')
x = f1.read().splitlines()
f1.close

y = []
for term in x:
    y.append(term.split(','))
y = y[1:]

pos = 0
neg = 0
for i in range(len(y)):
    if y[i][len(y[0])-1] == 'democrat' or y[i][len(y[0])-1] == 'A':
        pos += 1
    if y[i][len(y[0])-1] == 'republican' or y[i][len(y[0])-1] == 'notA':
        neg += 1
probS = pos/float(pos+neg)
if pos >= neg:
    error = 1 - probS
else: error = probS
if probS == 0 or probS ==1:
    gainS = 0
else: gainS = probS* math.log(1/probS,2)+(1-probS)*math.log(1/(1-probS),2)

sys.stdout.write("entropy: %f\n" % gainS)
sys.stdout.write("error: %f" % error)
