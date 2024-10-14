from abc import ABC, abstractmethod

class SystemInterface(ABC):
    @abstractmethod
    def update(self, dt):
        """Update the system state by a time step dt."""
        pass

    @abstractmethod
    def get_x(self):
        """Get the current state x of the system."""
        pass

    @abstractmethod
    def get_final_poses(self):
        """Get the final poses for plotting."""
        pass