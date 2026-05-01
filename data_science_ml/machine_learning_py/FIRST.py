#Machine learning python book

import numpy as np, pandas as pd, matplotlib.pylab as plt
#pip install numpy
#import numpy as np

X = np.arange(10) # CREATE some data
Y = X + np.random.randn(10) #linear w noise

# we next import and create an instance of the linear regression class from scikit-learn

from sklearn.linear_model import LinearRegression
lr = LinearRegression() # Create Model

X,Y = X.reshape((-1,1)), Y.reshape((-1,1))
lr.fit(X,Y)
#LinearRegression(copy_X=True, fit_intercept=True, normalize=False)

lr.coef_
#array([[0.94211853]])

# Programming Tip = the negative one in the reshape ((-1, 1))
# call above is for the truly lazy. Using a negative one tells
# numpy to figure out what that dimension should be given the
# other dimension and number of array elements.

# The model has a score method that computes the R^2 value for the regression

lr.score(X,Y)
#0.9059042979442371

# Now that we have this fitted

xi = np.linspace(0,10,15) # More points to draw
xi = xi.reshape((-1,1)) # reshape as column
print(xi)
yp = lr.predict(xi)

# y = a0x0 + a1x1 + a2x2 + ... + anxn

#plt.plot(yp)
#plt.plot(xi)

#plt.show()


plt.plot(yp, marker="o", markersize=20, markeredgecolor="red", markerfacecolor="green")
plt.ylabel('Y')
plt.xlabel('X')
plt.xlim(0, 15)
plt.ylim(0, 15)
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True
plt.grid()
plt.show()
