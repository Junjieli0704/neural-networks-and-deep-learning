#coding=utf-8
"""
network.py
~~~~~~~~~~

A module to implement the stochastic gradient descent learning
algorithm for a feedforward neural network.  Gradients are calculated
using backpropagation.  Note that I have focused on making the code
simple, easily readable, and easily modifiable.  It is not optimized,
and omits many desirable features.
"""

#### Libraries
# Standard library
import random

# Third-party libraries
import numpy as np

class Network(object):

    def __init__(self, sizes):
        """The list ``sizes`` contains the number of neurons in the
        respective layers of the network.  For example, if the list
        was [2, 3, 1] then it would be a three-layer network, with the
        first layer containing 2 neurons, the second layer 3 neurons,
        and the third layer 1 neuron.  The biases and weights for the
        network are initialized randomly, using a Gaussian
        distribution with mean 0, and variance 1.  Note that the first
        layer is assumed to be an input layer, and by convention we
        won't set any biases for those neurons, since biases are only
        ever used in computing the outputs from later layers."""
        self.num_layers = len(sizes)
        self.sizes = sizes

        # ------------------------------AddByJJli,2017-02-13 19 --------------------------------------------------------
        # if siezs = [2,3,1], then sizes[1:] = [3,1] 除去输入层的一个节点数目向量
        # 对于输入层 是没有 biases, 其它层每个节点都会有一个bias的值
        # np.random.randn() Return a sample (or samples) from the “standard normal” distribution.
        # --------------------------------------------------------------------------------------------------------------
        # if k = np.random.randn(3, 1)
        # print k
        #   [[-0.61339975]
        #    [ 0.08063831]
        #    [ 1.05874508]]
        # print k[0]
        #   [-0.61339975]
        # print k[0][0]
        #   -0.61339975
        # --------------------------------------------------------------------------------------------------------------
        # if sizes = [2,3,1]
        # self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        # print self.biases
        #   [array([[ 1.05544242],
        #           [-0.31905243],
        #           [ 0.09201176]]), array([[-1.91692488]])]
        # print self.biases[0]
        #   [[ 1.05544242]
        #    [-0.31905243]
        #    [ 0.09201176]]
        # print self.biases[1]
        #   [[-1.91692488]]
        # 在 sizes = [2,3,1] 这个例子中
        # self.biases是一个两维的tensor，self.biases[0]表示隐层所有节点的bias值的矩阵，self.biases[1]表示输出层所有节点的bias值的矩阵
        # --------------------------------------------------------------------------------------------------------------
        # if sizes = [2,3,1]
        # self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]
        # print self.weights
        # [array([[-0.44147523, -0.14304161],
        #          [-0.89773065,  0.34085652],
        #          [-1.28993753, -0.43829499]]), array([[-0.3248269 , -0.83480821, -0.73854788]])]
        # self.weights是一个两维的tensor，self.weights[0]表示输入层到隐层所有节点的weight值 维度为(3*2)
        # --------------------------------------------------------------------------------------------------------------
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]

    def feedforward(self, a):
        """Return the output of the network if ``a`` is input."""
        # ------------------------------AddByJJli,2017-02-13 19 --------------------------
        # zip() is a useful function, if we don't used zip(), I will program like follows:
        # for i in range(0,len(self.weights)):
        #     w = self.weights[i]
        #     b = self.biases[i]
        # it will be very tedious.
        # -----------------------------------------------------------------------------------
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a)+b)
        return a

    def SGD(self, training_data, epochs, mini_batch_size, eta,
            test_data=None):
        """Train the neural network using mini-batch stochastic
        gradient descent.  The ``training_data`` is a list of tuples
        ``(x, y)`` representing the training inputs and the desired
        outputs.  The other non-optional parameters are
        self-explanatory.  If ``test_data`` is provided then the
        network will be evaluated against the test data after each
        epoch, and partial progress printed out.  This is useful for
        tracking progress, but slows things down substantially."""
        if test_data: n_test = len(test_data)
        n = len(training_data)
        # ------------------------------AddByJJli,2017-02-13 19 --------------------------
        # xrange() Like range(), but instead of returning a list, returns an object that
        # generates the numbers in the range on demand.  For looping, this is
        # slightly faster than range() and more memory efficient.
        # 所以xrange做循环的性能比range好，尤其是返回很大的时候，尽量用xrange吧，除非你是要返回一个列表。
        # -----------------------------------------------------------------------------------
        for j in xrange(epochs):
            random.shuffle(training_data)
            # ------------------------------AddByJJli,2017-02-13 19 --------------------------
            # 这一行的python代码习惯可以学习
            # 如果不写成一行，就该这么写
            # mini_batches = []
            # for k in xrange(0,n,mini_batch_size):
            #   mini_batches.append(training_data[k:k+mini_batch_size])
            # -----------------------------------------------------------------------------------
            mini_batches = [training_data[k:k+mini_batch_size]  for k in xrange(0, n, mini_batch_size)]

            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            if test_data:
                # ------------------------------AddByJJli,2017-02-13 19 --------------------------
                # 这种格式化输出的方式也可以学习，自己写的格式化输出的方式太丑了
                # -----------------------------------------------------------------------------------
                print "Epoch {0}: {1} / {2}".format(j, self.evaluate(test_data), n_test)
            else:
                print "Epoch {0} complete".format(j)

    def update_mini_batch(self, mini_batch, eta):
        """Update the network's weights and biases by applying
        gradient descent using backpropagation to a single mini batch.
        The ``mini_batch`` is a list of tuples ``(x, y)``, and ``eta``
        is the learning rate."""
        # ------------------------------AddByJJli,2017-02-13 19 --------------------------
        # nabla_w mini_batch之后的w的梯度值，初始化为0
        # nabla_b mini_batch之后的b的梯度值，初始化为0
        # -----------------------------------------------------------------------------------
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [w-(eta/len(mini_batch))*nw for w, nw in zip(self.weights, nabla_w)]
        self.biases =  [b-(eta/len(mini_batch))*nb for b, nb in zip(self.biases, nabla_b)]

    def backprop(self, x, y):
        """Return a tuple ``(nabla_b, nabla_w)`` representing the
        gradient for the cost function C_x.  ``nabla_b`` and
        ``nabla_w`` are layer-by-layer lists of numpy arrays, similar
        to ``self.biases`` and ``self.weights``."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # feedforward
        activation = x
        activations = [x] # list to store all the activations, layer by layer
        zs = []           # list to store all the z vectors, layer by layer
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation)+b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        # backward pass
        delta = self.cost_derivative(activations[-1], y) * \
            sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        # Note that the variable l in the loop below is used a little
        # differently to the notation in Chapter 2 of the book.  Here,
        # l = 1 means the last layer of neurons, l = 2 is the
        # second-last layer, and so on.  It's a renumbering of the
        # scheme in the book, used here to take advantage of the fact
        # that Python can use negative indices in lists.
        for l in xrange(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
        return (nabla_b, nabla_w)

    def evaluate(self, test_data):
        """Return the number of test inputs for which the neural
        network outputs the correct result. Note that the neural
        network's output is assumed to be the index of whichever
        neuron in the final layer has the highest activation."""
        test_results = [(np.argmax(self.feedforward(x)), y)  for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)

    def cost_derivative(self, output_activations, y):
        """Return the vector of partial derivatives \partial C_x /
        \partial a for the output activations."""
        return (output_activations-y)

#### Miscellaneous functions
def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+np.exp(-z))

def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
    return sigmoid(z)*(1-sigmoid(z))
