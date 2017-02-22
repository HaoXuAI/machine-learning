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
beta = {}
beta_state = []
sum = 0
back_total = 0
for n in range(len(devline)):
    k = 0
    dev = devline[n].split()
    for t in range(len(dev)-1,-1,-1):
        if k == 0:
            beta[dev[t]] = [0,0,0,0,0,0,0,0]
        if k != 0:
            for i in range(8):
                for j in range(8):
                    if sum == 0:
                        sum = math.log(dict_emit[dev[t+1]][j]) + beta[dev[t+1]][j] + math.log(dict_trans[state[j]][i])
                    else:
                        sum = log_sum(sum, math.log(dict_emit[dev[t+1]][j]) + beta[dev[t+1]][j] + math.log(dict_trans[state[j]][i]))
                beta_state.append(sum)
                sum = 0
            beta[dev[t]] = beta_state
            beta_state = []
        k += 1
    for i in range(8):
        if back_total == 0:
            back_total = math.log(dict_prior[i]) + math.log(dict_emit[dev[0]][i]) + beta[dev[0]][i]
        else:
            back_total = log_sum(back_total, math.log(dict_prior[i]) + math.log(dict_emit[dev[0]][i]) + beta[dev[0]][i])
    print back_total
    back_total = 0
    alpha = {}
    
