import sys
import math

def fileload(filename):
    f1 = open(filename, 'r')
    x = f1.read().splitlines()
    f1.close

    y = []
    z = []
    for term in x:
        y.append(term.split(','))
        z.append(term.split(','))
    y1 = y[0]
    y = y[1:]
    tot = len(y)
    length = len(y[0])
    for i in range(tot):
        for j in range(length):
            if (y[i][j] == 'y' or y[i][j] == 'democrat' or y[i][j] == 'A'
                or y[i][j] == 'yes' or y[i][j] == 'before1950' or y[i][j] == 'morethan3min'
                or y[i][j] == 'fast' or y[i][j] == 'expensive' or y[i][j] == 'high'
                or y[i][j] == 'Two' or y[i][j] == 'large'): y[i][j] = 1
            else: y[i][j] = 0
    return (y1, y, z[1:])

def entropy(pos, neg):
    if (pos + neg) != 0:
        probS = pos/float(pos+neg)
        if probS != 0 and probS != 1:
            gain1 = probS * math.log(1/probS,2)
            gain2 = (1-probS) * math.log(1/(1-probS),2)
        else: gain1 = gain2 = 0 
        gainS = gain1 + gain2
    else: gainS = 0
    return gainS       

def mutual(a1, a2, a3, a4, a5, a6):
    entropyS = entropy(a1, a2)
    gainS1 = entropy(a3, a4)
    gainS2 = entropy(a5, a6)
    prob1 = float(a3+a4)/(a3+a4+a5+a6)
    gain0 = entropyS -  prob1 * gainS1 - (1 - prob1) * gainS2
    return gain0

def tree(y):
    pos = 0
    neg = 0
    tot = len(y)
    length = len(y[0])
    for i in range(tot):
        if y[i][length-1] == 1:
            pos += 1
        if y[i][length-1] == 0:
            neg += 1
    gainS = entropy(pos, neg)

    attr1 = [0]*length
    for j in range(length):
        for i in range(tot):
            if y[i][j] == 1:
                if y[i][length-1] == 1:
                    attr1[j] += 1
    attr2 = [0]*length
    for j in range(length):
        for i in range(tot):
            if y[i][j] == 1:
                if y[i][length-1] == 0:
                    attr2[j] += 1
    attr3 =[0]*length
    for j in range(length):
        for i in range(tot):
            if y[i][j] == 0:
                if y[i][length-1] == 1:
                    attr3[j] += 1
    attr4 =[0]*length
    for j in range(length):
        for i in range(tot):
            if y[i][j] == 0:
                if y[i][length-1] == 0:
                    attr4[j] += 1
    return(pos, neg, attr1, attr2, attr3, attr4)

def decision(y, z):
    tot = len(y)
    length = len(y[0])
    pos, neg, attr1, attr2, attr3, attr4 = tree(y)
    gain1 = [0]*(length-1)
    for j in range(length-1):
        gain1[j] = mutual(pos, neg, attr1[j], attr2[j], attr3[j], attr4[j])    
    root = gain1.index(max(gain1))
    index = [i for i,n in enumerate(gain1) if (n != gain1[root])]
    z=[]
    for i in range(tot):
        if y[i][root] == 1:
                z.append(y[i])
    pos1, neg1, attr11, attr12, attr13, attr14 = tree(z)
    gain2 = [0]*(length-1)
    max0 = 0
    nodeleft = root
    noderight = root
    for j in index:
        gain2[j] = mutual(pos1, neg1, attr11[j], attr12[j], attr13[j], attr14[j])
        if gain2[j] >= max0 and gain2[j] >=0.1:
            nodeleft = j
            max0 = gain2[j]
            
    k = []
    for i in range(tot):
        if y[i][root] == 0:
                k.append(y[i])
    pos2, neg2, attr21, attr22, attr23, attr24 = tree(k)
    gain3 = [0]*(length-1)
    max0 = 0
    for j in index:
        gain3[j] = mutual(pos2, neg2, attr21[j], attr22[j], attr23[j], attr24[j])
        if gain3[j] >= max0 and gain3[j] >=0.1:
            noderight = j
            max0 = gain3[j]
    
    return (pos, neg, pos1, neg1, attr11, attr12, attr13, attr14, pos2,
            neg2, attr21, attr22, attr23, attr24, root, nodeleft, noderight)

def error(tot, root, nodeleft, noderight, pos1, neg1, attr11, attr12, attr13, attr14,
          pos2, neg2, attr21, attr22, attr23, attr24):
    num = 0
    if nodeleft != root:
        if attr11[nodeleft] >= attr12[nodeleft]: num += attr12[nodeleft]
        else: num += attr11[nodeleft]
        if attr13[nodeleft] >= attr14[nodeleft]: num += attr14[nodeleft]
        else: num += attr13[nodeleft]
    else:
        if pos1 >= neg1: num += neg1
        else: num += pos1
    if noderight != root:
        if attr21[nodeleft] >= attr22[nodeleft]: num += attr22[nodeleft]
        else: num += attr21[nodeleft]
        if attr23[nodeleft] >= attr24[nodeleft]: num += attr24[nodeleft]
        else: num += attr23[nodeleft]
    else:
        if pos2 >= neg2: num += neg2
        else: num += pos2
    error = float(num)/tot
    return error

filename1 = sys.argv[1]
x, y, z = fileload(filename1)

(pos, neg, pos1, neg1, attr11, attr12, attr13, attr14, pos2, neg2,
 attr21, attr22, attr23, attr24, root, nodeleft, noderight) = decision(y, z)

tot = len(y)
m = 0
for i in range(tot):
    if y[i][root] == 1: tar1 = z[i][root]
    else: tar2 = z[i][root]
for i in range(tot):
    if y[i][nodeleft] == 1: tar3 = z[i][nodeleft]
    else: tar4 = z[i][nodeleft]
for i in range(tot):
    if y[i][noderight] == 1: tar5 = z[i][noderight]
    else: tar6 = z[i][noderight]
   
sys.stdout.write("[%s+/" % pos)
sys.stdout.write("%s-]\n" % neg)
               
sys.stdout.write("%s" % x[root])
sys.stdout.write(" = %s" % tar1)
sys.stdout.write(": [%s+/" % pos1)
sys.stdout.write("%s-]\n" % neg1)
if nodeleft != root:
    sys.stdout.write("| %s" % x[nodeleft])
    sys.stdout.write(" = %s" % tar3)
    sys.stdout.write(": [%s+/" % attr11[nodeleft])
    sys.stdout.write("%s-]\n" % attr12[nodeleft])
    sys.stdout.write("| %s" % x[nodeleft])
    sys.stdout.write(" = %s" % tar4)
    sys.stdout.write(": [%s+/" % attr13[nodeleft])
    sys.stdout.write("%s-]\n" % attr14[nodeleft])
sys.stdout.write("%s" % x[root])
sys.stdout.write(" = %s" % tar2)
sys.stdout.write(": [%s+/" % pos2)
sys.stdout.write("%s-]\n" % neg2)
if noderight != root:
    sys.stdout.write("| %s" % x[noderight])
    sys.stdout.write(" = %s" % tar5)
    sys.stdout.write(": [%s+/" % attr21[noderight])
    sys.stdout.write("%s-]\n" % attr22[noderight])
    sys.stdout.write("| %s" % x[noderight])
    sys.stdout.write(" = %s" % tar6)
    sys.stdout.write(": [%s+/" % attr23[noderight])
    sys.stdout.write("%s-]\n" % attr24[noderight])

errortrain = error(tot, root, nodeleft, noderight, pos1, neg1, attr11, attr12, attr13, attr14,
          pos2, neg2, attr21, attr22, attr23, attr24) 
sys.stdout.write("error(train): %s\n" % errortrain)

filename2 =sys.argv[2]
x2, y2, z2 = fileload(filename2)
testtot = len(y2)
testlen = len(y2[0])
testnum = 0

if nodeleft != root:
    if attr11[nodeleft] >= attr12[nodeleft]: p1 = 1
    else: p1 = 0
    if attr13[nodeleft] >= attr14[nodeleft]: p2 = 1
    else: p2 = 0    
else:
    if pos1 >=neg1: pL = 1
    else: pL = 0
if noderight != root:
    if attr21[noderight] >= attr22[noderight]: p3 = 1
    else: p3 = 0
    if attr23[noderight] >= attr24[noderight]: p4 = 1
    else: p4 = 0
else:
    if pos2 >= neg2: pR = 1
    else: pR = 0
  
for i in range(testtot):
    if y2[i][root] == 1:
        if nodeleft != root:
            if y2[i][nodeleft] == 1:
                if y2[i][testlen-1] != p1: testnum +=1
            else:
                if y2[i][testlen-1] != p2: testnum +=1
        else:
            if y2[i][testlen-1] != pL: testnum +=1
    else:
        if noderight != root:
            if y2[i][noderight] == 1:
                if y2[i][testlen-1] != p3: testnum +=1
            else:
                if y2[i][testlen-1] != p4: testnum +=1
        else:
            if y2[i][testlen-1] != pR: testnum +=1
errortest = float(testnum)/testtot    
    
sys.stdout.write("error(test): %s" % errortest)

