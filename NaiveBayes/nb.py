import sys
import math
filename1 = sys.argv[1]
f1 = open(filename1, 'r')
trainsplit = f1.read().split()

dict_train = {}
for i in range(len(trainsplit)):
    f = open(trainsplit[i], 'r')
    train = f.read().lower().split()
    dict_train[trainsplit[i]] = train

vocabulary = {}
text_c = {}
text_l = {}
docs_c = []
docs_l = []
for i in range(len(trainsplit)):
    for word in dict_train[trainsplit[i]]:
        if word not in vocabulary:
            vocabulary[word] = 1
        else:
            vocabulary[word] += 1
        if trainsplit[i][0] == 'c':
            if word not in text_c:
                text_c[word] = 1
            else:
                text_c[word] += 1
        else:
            if word not in text_l:
                text_l[word] = 1
            else:
                text_l[word] += 1
    if trainsplit[i][0] == 'c':
        docs_c.append(trainsplit[i])
    else:
        docs_l.append(trainsplit[i])

n_c = sum(text_c.values())
n_l = sum(text_l.values())
P_con = float(len(docs_c))/len(trainsplit)
P_lib = float(len(docs_l))/len(trainsplit)
p_c = {}
p_l = {}
for word in vocabulary:
    if word in text_c:
        p_c[word] = float(text_c[word] + 1)/(n_c + len(vocabulary))
    else:
        p_c[word] = float(1.0/(n_c + len(vocabulary)))
    if word in text_l:
        p_l[word] = float(text_l[word] + 1)/(n_l + len(vocabulary))
    else:
        p_l[word] = float(1.0/(n_l + len(vocabulary)))

filename2 = sys.argv[2]
f3 = open(filename2, 'r')
testsplit = f3.read().split()

dict_test = {}    
for i in range(len(testsplit)):
    f = open(testsplit[i], 'r')
    test = f.read().lower().split()
    dict_test[testsplit[i]] = test

pc =0
pl =0
error = 0
for i in range(len(testsplit)):
    for word in dict_test[testsplit[i]]:
        if word in vocabulary:
            pc += math.log(p_c[word],10)
            pl += math.log(p_l[word],10)
    pc = math.log(P_con,10) + pc
    pl = math.log(P_lib,10) + pl
    if pc >= pl:
        sys.stdout.write("C\n")
        if testsplit[i][0] == 'l':
            error +=1
    else:
        sys.stdout.write("L\n")
        if testsplit[i][0] == 'c':
            error +=1
    pc = 0
    pl = 0
sys.stdout.write("Accuary: %.04f" % (1-float(error)/len(testsplit)))
    
