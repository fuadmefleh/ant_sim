import random

from components.components import ( AntTypeComponent, PositionComponent, TaskComponent )

class TaskSystem:
    def __init__(self):
        # Initialize any task-related data structures or parameters
        self.available_tasks = ["explore", "gather_food", "build_tunnel"]  # Example: List of available task types
        self.task_assignments = {}  # Dictionary to store assigned tasks for entities

    def update(self, entities, game_map):
        
        for entity_id, task_component in entities.get_components(TaskComponent).items():
            position_component = entities.get_components(PositionComponent)[entity_id]
            type_component = entities.get_components(AntTypeComponent)[entity_id]
            
            if task_component.task_type == "explore":
                # Check if they arrived, if so, smell for food
                if position_component.x == task_component.target_x and position_component.y == task_component.target_y:
                    # Look for food in the vicinity
                    target_x, target_y = game_map.smell_food(position_component.x, position_component.y, 5)
                    
                    if target_x != None and target_y != None:
                        task_component.task_type = "gather_food"
                        task_component.target_x = target_x
                        task_component.target_y = target_y
                        
            elif task_component.task_type == "gather_food":
                # Check if they arrived, if so, return to the nest
                if position_component.x == task_component.target_x and position_component.y == task_component.target_y:
                    task_component.task_type = "return_home"
                    task_component.target_x = 0
                    task_component.target_y = 0

    def assign_task(self, entity_id, task_type, target_x, target_y):
        # Assign a new task to the entity
        self.task_assignments[entity_id] = TaskComponent(task_type, target_x, target_y)

    def generate_explore_target(self, game_map):
        # Generate the target coordinates for the explore task
        # Example: Randomly generate target coordinates within the map bounds
        target_x = random.randint(0, game_map.width - 1)
        target_y = random.randint(0, game_map.height - 1)
        return target_x, target_y

    def generate_food_target(self, game_map):
        # Generate the target coordinates for the gather_food task
        # Example: Randomly generate target coordinates near food sources
        # ...
        pass

    def generate_tunnel_target(self, game_map):
        # Generate the target coordinates for the build_tunnel task
        # Example: Randomly generate target coordinates for tunnel construction
        # ...
        pass
        

    def complete_task(self, entity_id):
        # Complete the task for the entity
        if entity_id in self.task_assignments:
            del self.task_assignments[entity_id]
