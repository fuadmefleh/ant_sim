import time
from utils import *
from entity_manager import EntityManager

from components.MapComponent import MapComponent
from systems.systems import (
    MovementSystem, ForagingSystem, CombatSystem, HomeFindingSystem, EggLayingSystem, EggHatchingSystem
)

from systems.RenderingSystem import RenderingSystem
from systems.TaskSystem import TaskSystem


manager = EntityManager()

# Create game map
game_map = MapComponent(width=500, height=200)
# Add some food sources
game_map.add_food(50, 10)
game_map.add_food(20, 15)
game_map.add_food(60, 25)
game_map.add_food(130, 15)
#game_map.add_food(400, 10)

manager.create_entity([game_map])

def create_new_game():
    # Create a queen
    create_ant( manager, 80, 9, "queen" )

    # Create ants
    for i in range(5):
        create_ant( manager, 80, 9, "worker" )
        
    # Create systems
    movement_system = MovementSystem()
    foraging_system = ForagingSystem()
    combat_system = CombatSystem()
    home_finding_system = HomeFindingSystem()
    rendering_system = RenderingSystem()
    egg_laying_system = EggLayingSystem()
    egg_hatching_system = EggHatchingSystem()
    
    task_system = TaskSystem()

    update_interval = 1 / 20  # Update interval for 20 Hz
    start_time = time.time()
    run_time = int( 100 / update_interval )

    for _ in range(run_time):
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time < update_interval:
            time.sleep(update_interval - elapsed_time)  # Wait to maintain the update frequency
        start_time = time.time()  # Reset the start time for the next update

        task_system.update(manager, game_map)
        
        movement_system.update(manager, game_map)
        foraging_system.update(manager, game_map)
        egg_laying_system.update(manager)
        egg_hatching_system.update(manager)
        combat_system.update(manager)
        home_finding_system.update(manager)
        rendering_system.update(manager)
        
        
        
        #input()



create_new_game()
