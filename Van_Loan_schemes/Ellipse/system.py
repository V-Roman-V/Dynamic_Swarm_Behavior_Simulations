from modules.Isystem import SystemInterface
import numpy as np
import scipy as cp

class System(SystemInterface):
    def __init__(self, N):
        self.N = N

        self.x = np.random.random((N, 2)) * 2 - 1
        self.M = self._getM(N)
        self.final_poses = np.zeros((N,2)) #np.asarray([self.x[0] + (i + 1) / (N - 1) * (self.x[-1] - self.x[0]) for i in range(N - 2)])

        angles = np.linspace(0, 2*np.pi * (N-1)/N, N)
        c = np.cos(angles)
        s = np.sin(angles)

        ctx = np.dot(c, self.x[:,0])
        stx = np.dot(s, self.x[:,0])
        cty = np.dot(c, self.x[:,1])
        sty = np.dot(s, self.x[:,1])
        delim = lambda x ,y: np.sqrt(x**2 + y**2)
        self.A = np.sqrt(2 / N) * np.array([
            [ctx/delim(ctx, stx), stx/delim(ctx, stx)],
            [cty/delim(cty, sty), sty/delim(cty, sty)]
        ])
        self.S = self.A @ self.A.T # cp.linalg.sqrtm(self.A @ self.A.T)

    def _getM(self, N):
        M = np.eye(N)
        for i in range(N):
            M[i, (i+1)% N] = 1
        M /= 2  # normalize
        return M

    def check_ellipse(self):
        Sinv = np.linalg.inv(self.S)
        sum = 0
        for i in range(self.N):
            coord = self.x[i,:].T  # 2 x 1
            sum += coord.T @ Sinv @ coord
        print(f"Check ellipse: {sum / self.N:.5f} == 1" )

    def update(self, dt):
        """Update the system state by a time step dt."""
        x_transformed = self.M @ self.x
        norms = np.linalg.norm(x_transformed, axis=0)
        self.x = x_transformed / norms
        self.x -= np.mean(self.x, axis=0)
        self.check_ellipse()

    def get_x(self):
        """Get the current state x of the system."""
        return self.x

    def get_final_poses(self):
        """Get the final poses for plotting."""
        angles = np.linspace(0, 2*np.pi * (self.N-1)/self.N, self.N)
        x = np.cos(angles)
        y = np.sin(angles)
        coords = np.asarray([x,y])
        T = cp.linalg.sqrtm(self.S)
        new_coords = T @ coords
        return new_coords.T
