import mnist_loader
import network

import random
import numpy as np


if __name__ == "__main__":
    #training_data, validation_data, test_data = mnist_loader.load_data_wrapper()
    #net = network.Network([784, 30, 10])
    #net.SGD(training_data, 30, 10, 3.0, test_data=test_data)

    #a = [k*5 for k in range(0,10)]
    #print a
    sizes = [2,3,1]
    a = [np.random.randn(y, 1) for y in sizes[1:]]
    b = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]
    print b

    #print sizes[1:]
    #print a[0][0]
    #print a[0][0][0]
    #print np.random.randn(3, 1)
    k = np.random.randn(3, 1)
    #print k
    #print k[0]
    #print k[0][0]
