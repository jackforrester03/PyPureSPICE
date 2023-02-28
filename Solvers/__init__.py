import numpy as np

class DCsolver():
    def __init__(self, A, Z, X):
        self.A = A
        self.Z = Z
        self.X = X
    def run(self):
        self.X = np.linalg.inv(self.A) @ self.Z.T