import numpy as np
import math
import pandas as pd
from sklearn.metrics import roc_auc_score

def grad(X, y, w, C=0, k = 0.1, max_step = 10000):
    eps = 1e-5
    s1 = 0
    s2 = 0
    l = X.shape[0]
    for _ in range(max_step):
        w0 = np.copy(w)
        s1 = 0
        s2 = 0
        for i in range(l):
            s1 += y[i] * X[i,0] * (1 - (1 + np.exp(-y[i]*(w[0]*X[i,0] + w[1]*X[i,1])))**(-1))
            s2 += y[i] * X[i,1] * (1 - (1 + np.exp(-y[i]*(w[0]*X[i,0] + w[1]*X[i,1])))**(-1))
        w[0] += k * s1 / l - k * C * w[0]
        w[1] += k * s2 / l - k * C * w[1]
        if math.sqrt((w0[0] - w[0])**2 + (w0[1] - w[1])**2) < eps:
            break
    return w

def sigmoda(X, w):
    return 1 / (1 + np.exp(-w[0] * X[:, 0] - w[1] * X[:, 1]))


df = pd.read_csv('data.csv', header=None)
x = np.array(df.iloc[:,1:3])
y = np.array(df.iloc[:,0])
w = np.array([0.0, 0.0])
print(grad(x, y, w, C=10))
a = sigmoda(x, w)
print(roc_auc_score(y, a))