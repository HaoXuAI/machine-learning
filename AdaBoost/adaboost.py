import numpy as np

class Example:
  # x is a vector, y in {-1,1}, D is weight
  def __init__(self, x, y, D):
    self.x, self.y, self.D = x, y, D

class DecisionStump:
  # sgn(a'x > b), a is a unit vector, b is a scalar
  def __init__(self, a, b):
    self.a, self.b = a, b
  
  def __str__(self):
    var = 'x1' if self.a[0] != 0 else 'x2'
    ineq = '>' if sum(self.a) > 0 else '<'
    b = self.b if sum(self.a) > 0 else -self.b
    return 'sgn(%2s %s %3.1f)' % (var, ineq, b)

  # prediction on x
  def predict(self, x):
    return 1 if np.inner(self.a, x) > self.b else -1

  # err rate of h on D
  def err(self, S):
    return sum([s.D * (s.y * self.predict(s.x) < 0) for s in S])

class Ensemble:
  # sgn(sum(alpha * h))
  def __init__(self):
    self.h, self.alpha = list(), list()

  # add hypothesis h with weight alpha
  def add(self, h, alpha):
    self.h.append(h)
    self.alpha.append(alpha)
   
  # prediction on x
  def predict(self, x):
    T = len(self.h)
    fx = sum([self.alpha[t] * self.h[t].predict(x) for t in range(T)])
    return 1 if fx > 0 else -1

  # err rate of ensemble on S (unweighted)
  def err(self, S):
    return sum([1.0/len(S) * (s.y * self.predict(s.x) < 0) for s in S])

# enumerate and pick the best hypothesis in C
def weaklearn(S, C):
  errs = [h.err(S) for h in C]
  index = np.argmin(errs)
  return C[index], errs[index]

# main adaboost algorithm
def adaboost(S, C, T):
  print('%12s %16s %12s %12s %70s %12s' % ('t', 'h', 'eps', 'alpha', 'D', 'err(H)'))
  H = Ensemble()
  for t in range(T):
    h, eps = weaklearn(S, C)
    alpha = 0.5 * np.log((1 - eps) / eps)
    H.add(h, alpha)
    print('%12s %16s %12.3f %12.3f %70s %12.3f' % (t+1, h, eps, alpha, ' '.join(['%6.3f' % s.D for s in S]), H.err(S)))
    # update weights
    Z = 2 * np.sqrt(eps * (1-eps))
    for s in S:
      s.D = s.D / Z * np.exp(- alpha * s.y * h.predict(s.x))

if __name__ == '__main__':
  # all decision stumps
  C = list()
  for sign in [-1, 1]:
    for a in [np.array([sign,0]), np.array([0,sign])]:
      for b in sign * np.arange(0.5, 6, 1): # [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
          C.append(DecisionStump(a, b))
  # data
  m = 9
  S = list()
  S.append(Example(np.array([1,2]),  1, 1.0/m))
  S.append(Example(np.array([2,3]),  1, 1.0/m))
  S.append(Example(np.array([3,4]), -1, 1.0/m))
  S.append(Example(np.array([3,2]), -1, 1.0/m))
  S.append(Example(np.array([3,1]), -1, 1.0/m))
  S.append(Example(np.array([4,4]), -1, 1.0/m))
  S.append(Example(np.array([5,4]), -1, 1.0/m))
  S.append(Example(np.array([5,2]),  1, 1.0/m))
  S.append(Example(np.array([5,1]),  1, 1.0/m))


  adaboost(S, C, 3)
