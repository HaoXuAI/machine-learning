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

for i in range(20):
    key = max(p_l, key = p_l.get)
    prob = p_l[key]
    del p_l[key]
    sys.stdout.write("%s" % key)
    sys.stdout.write(" %.04f\n" % prob)
sys.stdout.write("\n")
for i in range(20):
    key = max(p_c, key = p_c.get)
    prob = p_c[key]
    del p_c[key]
    sys.stdout.write("%s" % key)
    sys.stdout.write(" %.04f\n" % prob)

