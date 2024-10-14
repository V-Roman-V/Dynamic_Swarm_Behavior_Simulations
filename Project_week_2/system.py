from modules.Isystem import SystemInterface
import numpy as np

class System(SystemInterface):
    def __init__(self, N, alpha = 0.1):
        self.N = N
        self.alpha = alpha

        self.x = np.random.random((N, 2))
        self.v = np.zeros((N, 2))
        self.A = self._getA(N)
        self.B = self._getB(N)

        # move first to the left half and last to right half
        self.x[0, 0] /= 2
        self.x[-1, 0] = self.x[-1, 0] / 2 + 0.5
        self.final_poses = np.asarray([self.x[0] + (i + 1) / (N - 1) * (self.x[-1] - self.x[0]) for i in range(N - 2)])

    def _getA(self, N):
        A = np.zeros((N, N))
        for i in range(N):
            A[i, i] = -2
            if i > 0:
                A[i, i - 1] = 1
            if i < N - 1:
                A[i, i + 1] = 1
        A /= 2  # normilize
        A[0] = 0
        A[-1] = 0
        return A

    def _getB(self, N):
        B = np.eye(N)
        B[0,0] = 0
        B[-1,-1] = 0
        return B

    def update(self, dt):
        """Update the system state by a time step dt."""
        # Control law
        u = self.A @ self.x - self.alpha * self.B @ self.v

        # Euler update
        self.x = self.x + dt * self.v
        self.v = self.v + dt * u

    def get_x(self):
        """Get the current state x of the system."""
        return self.x

    def get_final_poses(self):
        """Get the final poses for plotting."""
        return self.final_poses
