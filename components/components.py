class TaskComponent:
    def __init__(self, task_type, target_x, target_y):
        self.task_type = task_type  # Example: "explore", "gather_food", "build_tunnel", etc.
        self.target_x = target_x  # X coordinate of the target location
        self.target_y = target_y  # Y coordinate of the target location

class PositionComponent:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class HealthComponent:
    def __init__(self, health=100):
        self.health = health

class HomeComponent:
    def __init__(self, home_id):
        self.home_id = home_id

class FoodComponent:
    def __init__(self):
        self.carried = False

class AntTypeComponent:
    def __init__(self, type):
        # Types could be 'worker', 'soldier', etc.
        self.type = type

class RenderComponent:
    def __init__(self, color='black', size=5):
        self.color = color
        self.size = size
   