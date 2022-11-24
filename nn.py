import math

import numpy as np
import random


class NeuralNetwork:

    def __init__(self, layer_sizes):
        """
        Neural Network initialization.
        Given layer_sizes as an input, you have to design a Fully Connected Neural Network architecture here.
        :param layer_sizes: A list containing neuron numbers in each layers. For example [3, 10, 2] means that there are
        3 neurons in the input layer, 10 neurons in the hidden layer, and 2 neurons in the output layer.
        """
        self.layers = layer_sizes
        np.random.seed()
        self.w = []
        self.b = []
        for i in range(len(layer_sizes) - 1):
            self.w.append(np.random.normal(0, 1, [layer_sizes[i + 1], layer_sizes[i]]))
            self.b.append(np.zeros([layer_sizes[i + 1], 1]))

    def activation(self, x):
        """
        The activation function of our neural network, e.g., Sigmoid, ReLU.
        :param x: Vector of a layer in our network.
        :return: Vector after applying activation function.
        """
        ans = 1 / (1 + np.exp(-x))
        return ans

    def batch_normalize(self, x, n):
        """

        :param x: array which want to normilize
        :param n: length of second dimension of array
        :return: return normalized array
        """
        # print(x)
        sum = 0
        for j in range(n):
            sum += x[j]
        avg = sum / n
        temp_sum = 0
        for j in range(n):
            temp_sum += (x[j] - avg) ** 2
        temp_sum /= n

        for j in range(n):
            x[j] = (x[j] - avg) / math.sqrt(temp_sum + 0.000001)
        return x

    def forward(self, x):
        """
        Receives input vector as a parameter and calculates the output vector based on weights and biases.
        :param x: Input vector which is a numpy array.
        :return: Output vector
        """
        # TODO (Implement forward function here)
        s = []
        for i in range(len(self.layers) - 1):
            if (i == 0):
                s = self.activation(self.w[i] @ x + self.b[i][0])
                s = self.batch_normalize(s, self.layers[i + 1])
            else:
                s = self.activation(self.w[i] @ s + self.b[i][0])
        return s
