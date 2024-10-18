from modules.Isystem import SystemInterface
import numpy as np

class System(SystemInterface):
    def __init__(self, N, R):
        self.N = N
        self.radius = R
        self.theta = np.random.random(N) * 2*np.pi
        self.theta[0] = 0
        self.theta[-1] = 2*np.pi

        self.M = self._getM(N)
        self.final_poses = np.zeros((N, 2)) # np.asarray([self.x[0] + (i + 1) / (N - 1) * (self.x[-1] - self.x[0]) for i in range(N - 2)])

    def _getM(self, N):
        M = np.zeros((N,N))
        for i in range(N):
            M[i, (N + i - 1) % N] = 0.5
            M[i, (i + 1) % N] = 0.5
        M[0] = M[-1] = 0
        M[-1,-1] = M[0,0] = 1
        return M

    def update(self, dt):
        """Update the system state by a time step dt."""
        self.theta = self.M @ self.theta

    def get_x(self):
        """Get the current state x of the system."""
        x_pos = self.radius * np.cos(self.theta)
        y_pos = self.radius * np.sin(self.theta)
        return np.asarray([x_pos, y_pos]).T

    def get_final_poses(self):
        """Get the final poses for plotting."""
        return self.final_poses
