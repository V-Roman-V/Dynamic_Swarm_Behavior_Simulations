import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from modules.Isystem import SystemInterface

class SimulationAnimation:
    def __init__(self, system: SystemInterface, dt, limits=(0,1), showLines=True):
        self.system = system
        self.limits = limits
        self.showLines = showLines
        self.N = system.get_x().shape[0]
        self.dt = dt
        self.trace_data = [np.empty((0, 2)) for _ in range(self.N)]
        self.final_poses = system.get_final_poses()
        
        self.fig, self.ax = plt.subplots()
        self.scat, self.traces, self.text_labels = self.setup_plot()

    def setup_plot(self):
        size = 100
        colors = ['yellow'] + ['lightgreen'] * (self.N - 2) + ['yellow']
        sizes = [2 * size] + [size] * (self.N - 2) + [2 * size]

        x = self.system.get_x()
        if self.showLines:
            self.ax.plot([x[0, 0], x[-1, 0]], [x[0, 1], x[-1, 1]], 'r--', lw=2, zorder=0)
        self.ax.scatter(self.final_poses[:, 0], self.final_poses[:, 1], color='k', s=size / 4, alpha=0.5, zorder=1)
        scat = self.ax.scatter(x[:, 0], x[:, 1], color=colors, s=sizes, zorder=2)
        traces = [self.ax.plot([], [], 'b-', lw=1, zorder=1)[0] for _ in range(self.N)]
        text_labels = [self.ax.text(x[i, 0], x[i, 1], str(i), fontsize=12, ha='center', va='center', zorder=3) for i in range(self.N)]
        
        self.ax.set_title(f"Simulation Time: 0.00 seconds")
        self.ax.set_xlim(self.limits)
        self.ax.set_ylim(self.limits)
        self.fig.tight_layout()

        return scat, traces, text_labels

    def update(self, frame):
        self.system.update(self.dt)
        x = self.system.get_x()
        self.scat.set_offsets(x)

        for i in range(self.N):
            self.trace_data[i] = np.vstack([self.trace_data[i], x[i]])
            self.traces[i].set_data(self.trace_data[i][:, 0], self.trace_data[i][:, 1])

        for i, text in enumerate(self.text_labels):
            text.set_position((x[i, 0], x[i, 1]))

        self.ax.set_title(f"Simulation Time: {frame * self.dt:.2f} seconds")
        return self.scat, *self.text_labels, *self.traces

    def run_animation(self, frames, interval):
        ani = FuncAnimation(self.fig, self.update, frames=np.arange(0, frames), interval=interval, blit=True)
        return ani
