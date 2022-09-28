from matplotlib import pyplot as plt
import numpy as np

#tracer la fonction x^2-2ln(x) en loglog

x = np.linspace(0,10,100)
y = x**2-2*np.log(x)
#mettre les axes entre 1 et 10
plt.axis([1,10,1,10])
plt.loglog(x,y)
plt.show()