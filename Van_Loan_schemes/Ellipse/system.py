from modules.Isystem import SystemInterface
import numpy as np

class System(SystemInterface):
    def __init__(self, N):
        self.N = N

        self.x = np.random.random((N, 2)) * 2 - 1
        self.M = self._getM(N)
        self.final_poses = np.zeros((N,2)) #np.asarray([self.x[0] + (i + 1) / (N - 1) * (self.x[-1] - self.x[0]) for i in range(N - 2)])

    def _getM(self, N):
        M = np.eye(N)
        for i in range(N):
            M[i, (i+1)% N] = 1
        M /= 2  # normalize
        return M

    def update(self, dt):
        """Update the system state by a time step dt."""
        x_transformed = self.M @ self.x
        norms = np.linalg.norm(x_transformed, axis=0)
        self.x = x_transformed / norms
        self.x -= np.mean(self.x, axis=0)

    def get_x(self):
        """Get the current state x of the system."""
        return self.x

    def get_final_poses(self):
        """Get the final poses for plotting."""
        return self.final_poses
