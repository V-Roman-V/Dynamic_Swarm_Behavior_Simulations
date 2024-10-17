from modules.Isystem import SystemInterface
import numpy as np

class System(SystemInterface):
    def __init__(self, N):
        self.N = N
        self.x = np.random.random((N, 2)) * 2 - 1

        # Move first point to the left part and last one to the right
        self.x[0,0] = -(self.x[0,0] + 1)/2
        self.x[-1,0] = (self.x[-1,0] + 1)/2

        self.M = self._getM(N)
        self.final_poses = np.asarray([self.x[0] + (i + 1) / (N - 1) * (self.x[-1] - self.x[0]) for i in range(N - 2)])

    def _getM(self, N):
        M = np.zeros((N,N))
        for i in range(N):
            if i > 0:
                M[i, i - 1] = 0.5
            if i < N - 1:
                M[i, i + 1] = 0.5
        M[0] = M[-1] = 0
        M[-1,-1] = M[0,0] = 1
        return M

    def update(self, dt):
        """Update the system state by a time step dt."""
        self.x = self.M @ self.x

    def get_x(self):
        """Get the current state x of the system."""
        return self.x

    def get_final_poses(self):
        """Get the final poses for plotting."""
        return self.final_poses
