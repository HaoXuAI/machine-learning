import sys
sys.stdout.write("%i\n" % 2**4)
sys.stdout.write("%i\n" % 2**(2**4))


f1 = open('4Cat-Train.labeled', 'r')
file1 = f1.read()
f1.close()

train1 = []
train = []
file1 = file1.split()
for i in range(1,len(file1),2):
    train.append(file1[i])
while train != []:
    train1.append(train[:5])
    train = train[5:]

Con = []

for i in range(2**(2**4)):
    st = bin(i)[2:]
    length = len(st)
    while length < len(bin(2**(2**4)-1)[2:]):
	    st = '0' + st
	    length =length +1
    Con.append(st)
    Con[i] = list(Con[i])

train2 = [[0 for i in xrange(5)] for j in xrange(len(train1))]
for i in range(len(train1)):
    for j in range(5):
        if train1[i][j] == 'Male': 
            train2[i][j] = 1
        if train1[i][j] == 'Female': 
            train2[i][j] = 0
        if train1[i][j] == 'Young': 
            train2[i][j] = 1
        if train1[i][j] == 'Old': 
            train2[i][j] = 0
        if train1[i][j] == 'Yes': 
            train2[i][j] = 1
        if train1[i][j] == 'No': 
            train2[i][j] = 0
        if train1[i][j] == 'high': 
            train2[i][j] = 1
        if train1[i][j] == 'low': 
            train2[i][j] = 0
st2 = ''
train3 = []
for i in range(len(train1)):
    for j in range(4):
        st2 = st2 + str(train2[i][j])
    train3.append(int(st2,2))
    train3.append(train2[i][4])
    del st2
    st2 = ''

number = 0
m = 0
for i in range(0, len(train3), 2):
    if train3[i+1] == 0:
        for j in range(len(Con)):
            if Con[j][train3[i]] == '1':
                Con[j][train3[i]] = 'NA'
    else:
        for j in range(len(Con)):
            if Con[j][train3[i]] == '0':
                Con[j][train3[i]] = 'NA'
finalCon = []
for i in range(len(Con)):
    for j in range(2**4):
        if Con[i][j] != 'NA':
            m += 1
    if m == 16:
        number +=1
        finalCon.append(Con[i])
    m = 0
sys.stdout.write("%i\n" %len(finalCon))

filename = sys.argv[1]
f2 = open(filename, 'r')
file2 = f2.read()
f2.close

trainnew1 = []
trainnew = []
file2 = file2.split()
for i in range(1,len(file2),2):
    trainnew.append(file2[i])
while trainnew != []:
    trainnew1.append(trainnew[:5])
    trainnew = trainnew[5:]

trainnew2 = [[0 for i in xrange(5)] for j in xrange(len(trainnew1))]
for i in range(len(trainnew1)):
    for j in range(5):
        if trainnew1[i][j] == 'Male': 
            trainnew2[i][j] = 1
        if trainnew1[i][j] == 'Female': 
            trainnew2[i][j] = 0
        if trainnew1[i][j] == 'Young': 
            trainnew2[i][j] = 1
        if trainnew1[i][j] == 'Old': 
            trainnew2[i][j] = 0
        if trainnew1[i][j] == 'Yes': 
            trainnew2[i][j] = 1
        if trainnew1[i][j] == 'No': 
            trainnew2[i][j] = 0
        if trainnew1[i][j] == 'high': 
            trainnew2[i][j] = 1
        if trainnew1[i][j] == 'low': 
            trainnew2[i][j] = 0

st2 = ''
trainnew3 = []
for i in range(len(trainnew1)):
    for j in range(4):
        st2 = st2 + str(trainnew2[i][j])
    trainnew3.append(int(st2,2))
    trainnew3.append(trainnew2[i][4])
    del st2
    st2 = ''

high = 0
low = 0
for i in range(0,len(trainnew3), 2):
    for j in range(len(finalCon)):
        if finalCon[j][trainnew3[i]] == '1':
            high +=1
        if finalCon[j][trainnew3[i]] == '0':
            low +=1
    sys.stdout.write("%i" %high)
    sys.stdout.write(" ")
    sys.stdout.write("%i\n" %low)
    high = 0
    low = 0
        
