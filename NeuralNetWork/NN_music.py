import sys
import numpy as np
import math
filename1 = sys.argv[1]
f1 = open(filename1, "r")
x = f1.read().splitlines()
x = x[1:]
data1 = []
t = []
X = []
for term in x:
    data1.append(term.split(','))
for i in range(len(data1)):
    data1[i][0] = int(float(data1[i][0]))
    data1[i][1] = float(data1[i][1])
for i in range(len(data1)):
    for j in range(len(data1[0])):
        if data1[i][j] == 'yes':
            data1[i][j] = 1
        if data1[i][j] == 'no':
            data1[i][j] = 0
for i in range(len(data1)):
    t.append(data1[i][4])
for i in range(len(data1)):
    X.append(data1[i][:4])
X = np.array(X)
#regularization
mean = np.mean(X, axis=0)
std = np.std(X, axis=0)
X = (X - mean)/std

epsi = 0.12
w1 = np.random.rand(4,4)*2*epsi - epsi
w2 = np.random.rand(1,4)*2*epsi - epsi

t = np.array(t)
t = np.reshape(t, (100, 1))

a1 = []
a2 = []
error = 10000
error1 = 10000
error2 = 1
step = 0
while (error1 - error2) > 0.00000001:
    # a1 = hidden output 100*4, a2 = output 100*1
    a1 = np.dot(X, np.transpose(w1))
    a1 = 1.0 / (1 + np.exp(-a1))
    a2 = np.dot(a1, np.transpose(w2))
    a2 = 1.0 / (1 + np.exp(-a2))
    error1 = error
    error = np.sum((t-a2)**2)/float(2)
    if error < error1:
        sys.stdout.write("%s\n" % error)
    else: break
    error2 = error
    # deltk = output error, delth = hidden error
    row1 = len(a2)
    col1 = len(a2[0])
    # deltk = 100*1
    deltk = a2 * (np.ones((row1, col1)) - a2) * (t - a2)

    row2 = len(a1)
    col2 = len(a1[0])
    # delth = 100*4
    delth = a1 * (np.ones((row2, col2)) - a1) * np.dot(deltk, w2)
    # deltw2 = 1*4, deltw1 = 4*4
    deltw2 = 0.05 * np.dot(np.transpose(deltk), a1)
    deltw1 = 0.05 * np.dot(np.transpose(delth), X)
    
    # w1 = 4*4, w2 = 1*4
    w1 += deltw1
    w2 += deltw2
    step += 1
    if step > 300000: break
sys.stdout.write("TRAINING COMPLETED! NOW PREDICTING.\n")

filename2 = sys.argv[2]
f2 = open(filename2, "r")
y = f2.read().splitlines()
y = y[1:]
data2 = []
X = []
for term in y:
    data2.append(term.split(','))
for i in range(len(data2)):
    data2[i][0] = int(float(data2[i][0]))
    data2[i][1] = float(data2[i][1])
for i in range(len(data2)):
    for j in range(len(data2[0])):
        if data2[i][j] == 'yes':
            data2[i][j] = 1
        if data2[i][j] == 'no':
            data2[i][j] = 0
for i in range(len(data2)):
    X.append(data2[i][:4])
np.array(X)
mean = np.mean(X, axis=0)
std = np.std(X, axis=0)
X = (X - mean)/std

a1 = []
a2 = []
a1 = np.dot(X, np.transpose(w1))
a1 = 1.0 / (1 + np.exp(-a1))
a2 = np.dot(a1, np.transpose(w2))
a2 = 1.0 / (1 + np.exp(-a2))
for term in a2:
    if term >0.5: sys.stdout.write("yes\n")
    else: sys.stdout.write("no\n")

