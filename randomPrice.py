import numpy as np
import matplotlib.pyplot as plt

N=250
percentage = 10 #+=%

X = np.arange(1,N+1)
Y = np.random.uniform(1-percentage/100,1+percentage/100,N)
Y2 = [0.0]*N

for i in range(1,N+1):
    Y2[i-1] = np.prod(Y[:i])

plt.plot(X,Y2)
plt.show()