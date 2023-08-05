import random

import numpy as np
import scipy.interpolate as si
import matplotlib.pylab as plt

if __name__ == '__main__':
    a = [-1, 2, -3]
    print(np.abs(a))

    xi = [i for i in range(20)]
    yi = [random.randint(1, 20) for _ in range(20)]
    min_x = min(xi)
    max_x = max(xi)
    x = np.arange(min_x, max_x, (max_x - min_x) / 100)

    interpolator = si.CubicSpline(xi, yi)
    y = interpolator(x)

    plt.scatter(xi, yi)
    plt.plot(x, y)

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Interpolation Demo')
    plt.show()
