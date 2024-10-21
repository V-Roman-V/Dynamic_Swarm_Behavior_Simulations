import os
from modules.animation import SimulationAnimation
from Project_week_2.system import System

def get_next_filename(folder='',prefix='simulation', ext='.gif'):
    num = len([file for file in os.listdir(folder) if file.lower().endswith(ext)])
    return os.path.join(folder,f'{prefix}{num}{ext}')

def main():
    # Configuration
    N = 15
    dt = 0.12
    alpha = 0.5  # Damping factor

    # Initialize the system
    system = System(N, alpha)
    animation = SimulationAnimation(system, dt)

    ani = animation.run_animation(frames=200, interval=100)
    ani.save(get_next_filename(folder='Project_week_2'), writer='pillow', fps=10)

if __name__ == "__main__":
    main()
