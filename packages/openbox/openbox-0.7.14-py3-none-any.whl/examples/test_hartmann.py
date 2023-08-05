import numpy as np
from collections import OrderedDict


class Hartmann6():
    """
    Hartmann 6-Dimensional function
    https://www.sfu.ca/~ssurjano/hart6.html
    """

    def __init__(self, noise=0.0):
        self.noise = noise
        self.bounds = OrderedDict([("x{i}".format(i=i), [0.0, 1.0]) for i in range(6)])
        self.min = np.array([0.20169, 0.150011, 0.476874, 0.275332, 0.311652, 0.6573])
        self.fmin = -3.32237
        self.name = "hart6"

    def f(self, params):
        assert len(params) == 6
        alpha = np.array([1.0, 1.2, 3.0, 3.2])
        A = np.array(
            [[10, 3, 17, 3.5, 1.7, 8], [0.05, 10, 17, 0.1, 8, 14], [3, 3.5, 1.7, 10, 17, 8], [17, 8, 0.05, 10, 0.1, 14]]
        )
        P = 1e-4 * np.array(
            [
                [1312, 1696, 5569, 124, 8283, 5886],
                [2329, 4135, 8307, 3736, 1004, 9991],
                [2348, 1451, 3522, 2883, 3047, 6650],
                [4047, 8828, 8732, 5743, 1091, 381],
            ]
        )
        outer = 0

        for i in range(4):
            inner = 0
            for j in range(6):
                xj = params[j]
                Aij = A[i, j]
                Pij = P[i, j]
                inner = inner + Aij * (xj - Pij) ** 2
            new = alpha[i] * np.exp(-inner)
            outer += new

        return float(-outer + self.noise * np.random.normal(0, 1))

    def evaluate_config(self, config):
        params = [0] * 6
        for i in range(6):
            params[i] = config['x%d' % i]
        return self.f(params)

    def get_configspace(self):
        from ConfigSpace import ConfigurationSpace, UniformFloatHyperparameter
        cs = ConfigurationSpace()
        for i in range(6):
            xi = UniformFloatHyperparameter("x%d" % i, 0, 1)
            cs.add_hyperparameter(xi)
        return cs

noise = 0.0
problem = Hartmann6(noise=noise)
cs = problem.get_configspace()
from ConfigSpace import Configuration
arr = [0.5] * 6
config = Configuration(cs, vector=arr)
print(problem.evaluate_config(config))
print(problem.f(arr))

