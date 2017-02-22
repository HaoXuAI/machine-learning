import sys
import math
from math import *

def log_sum(left,right):
	if right < left:
		return left + log1p(exp(right - left))
	elif left < right:
		return right + log1p(exp(left - right));
	else:
		return left + log1p(1)

filename1 = sys.argv[1]
f1 = open(filename1, 'r')
devline =f1.read().splitlines()

filename2 = sys.argv[2]
f2 = open(filename2, 'r')
trans =f2.read().split()
for i in range(len(trans)):
    trans[i] = trans[i].split(':')
    
filename3 = sys.argv[3]
f3 = open(filename3, 'r')
emit =f3.read().split()
for i in range(len(emit)):
    emit[i] = emit[i].split(':')

filename4 = sys.argv[4]
f4 = open(filename4, 'r')
prior =f4.read().split()

state = []
for i in range(0,len(prior)-1,2):
    state.append(prior[i])
dict_prior = {}
j = 0
for i in range(0,len(prior)-1,2):
    dict_prior[j] = float(prior[i+1])
    j = j+1
    
dict_emit = {}
for term in emit:
    if len(term) == 2:
        if term[0] not in dict_emit:
            dict_emit[term[0]] = [float(term[1])]
        else:
            dict_emit[term[0]].append(float(term[1]))
        
dict_trans = {}
for term in trans:
    if len(term) == 2:
        if term[0] not in dict_trans:
            dict_trans[term[0]] = [float(term[1])]
        else:
            dict_trans[term[0]].append(float(term[1]))
VP = {}
VP_state = []
interm = []
Q_star = {}
for n in range(len(devline)):
    k = 0
    dev = devline[n].split()
    for i in range(8):
        VP_state.append(math.log(dict_prior[i]) + math.log(dict_emit[dev[0]][i]))
    Q_star[0] = [0,1,2,3,4,5,6,7]
    VP[dev[0]] = VP_state
    VP_state = []
    for t in range(1,len(dev)):
        Q_star[t] = []
        for i in range(8):
            for j in range(8):
                interm.append(math.log(dict_emit[dev[t]][i]) + VP[dev[t-1]][j] + math.log(dict_trans[state[i]][j]))
                j_max = interm.index(max(interm))
            if t == 1:
                Q_star[t].append([Q_star[0][j_max]])
            else:
                Q_star[t].append(Q_star[t-1][j_max] + [j_max])
            VP_state.append(max(interm))
            interm = []
        VP[dev[t]] = VP_state
        VP_state = []
    Q_star[len(dev)-1].append(VP[dev[len(dev)-1]].index(max(VP[dev[len(dev)-1]])))
    m = VP[dev[t]].index(max(VP[dev[t]]))
    Q_star[len(dev)-1][m].append(m)
    for i in range(len(dev)):
        sys.stdout.write("%s" % dev[i])
        sys.stdout.write("_%s " % state[Q_star[t][m][i]])
    sys.stdout.write("\n")
    Q_star = {}
    VP = {}

