from utils import *
from components.components import PositionComponent, HealthComponent, HomeComponent, FoodComponent, AntTypeComponent, RenderComponent
from components.EggComponent import EggComponent

import heapq
import random

class EggLayingSystem:
    def update(self, entities):
        for entity_id, egg_component in entities.get_components(EggComponent).items():
            # Check conditions for laying eggs, e.g., enough food or safe location
            if len(egg_component.eggs) < 10:  # Maximum eggs limit for simplicity
                egg_component.lay_egg()
                #print(f"Queen Ant {entity_id} laid an egg. Total eggs now: {egg_component.eggs}")
            

class EggHatchingSystem:
    def update(self, entities):
        # List to store tasks for new ant creation
        new_ants_tasks = []

        # Collect tasks
        for entity_id, egg_component in entities.get_components(EggComponent).items():
            position_component = entities.get_components(PositionComponent)[entity_id]
            for egg in egg_component.eggs:
                egg["timer"] -= 1
                if egg["timer"] <= 0:
                    new_ants_tasks.append((position_component.x, position_component.y))
        
        # Now process new ant creation outside the loop
        for x, y in new_ants_tasks:
            create_ant(entities, x, y)

        # Update eggs list to remove hatched eggs and avoid modifying during iteration
        for entity_id, egg_component in entities.get_components(EggComponent).items():
            egg_component.eggs = [egg for egg in egg_component.eggs if egg["timer"] > 0]

        #if new_ants_tasks:
         #   print(f"{len(new_ants_tasks)} eggs hatched at various locations.")


class MovementSystem:
    
    
    def update(self, entities, game_map):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for entity_id, position in entities.get_components(PositionComponent).items():
            task_component = entities.get_components(TaskComponent)[entity_id]
            
            if task_component != None:
                # Move towards the target location
                
            
            # Shuffle the directions to randomize the movement
            random.shuffle(directions)
            for direction in directions:
                new_x = position.x + direction[0]
                new_y = position.y + direction[1]

                # Check if out of bounds
                if 0 > new_x >= game_map.width or 0 > new_y >= game_map.height:
                    continue
                
                # If they are trying to move up, ensure they have dirt to either their left or right
                if direction == (0, -1):
                    if game_map.terrain[new_x][new_y] != 'D':
                        if game_map.terrain[new_x - 1][new_y] != 'D' and game_map.terrain[new_x + 1][new_y] != 'D':
                            continue
                    else:
                        continue
                    
                # If they are trying to move down, ensure they have dirt to either their left or right
                if direction == (0, 1):
                    if game_map.terrain[new_x][new_y] != 'D':
                        if game_map.terrain[new_x - 1][new_y] != 'D' and game_map.terrain[new_x + 1][new_y] != 'D':
                            continue
                    else:
                        continue
                    
                if direction == (1, 0) or direction == (-1, 0):
                    # Check if they have dirt below them
                    #if game_map.terrain[new_x][new_y+1] != 'D' and new_y >= game_map.above_ground:
                    #    continue
                    if game_map.terrain[new_x][new_y] == 'D':
                        continue
                    
                position.x = new_x
                position.y = new_y
                #print(f"Ant {entity_id} moved to ({position.x}, {position.y}) from ({position.x - direction[0]}, {position.y - direction[1]})")
                break  # Stop after the first valid movement




class ForagingSystem:
    def update(self, entities, game_map):
        # Ants find food and carry it back to the nest
        for entity_id, position in entities.get_components(PositionComponent).items():
            if entity_id in entities.get_components(FoodComponent):
                food = entities.get_components(FoodComponent)[entity_id]
                # Check if the ant is on a food source
                if game_map.is_food(position.x, position.y) and not food.carried:
                    food.carried = True
                    #print(f"Ant {entity_id} collected food at ({position.x}, {position.y})")
                    
class CombatSystem:
    def update(self, entities):
        # Ants fight if they meet on the same position
        positions = entities.get_components(PositionComponent)
        healths = entities.get_components(HealthComponent)
        for entity_id, position in positions.items():
            for other_id, other_position in positions.items():
                if entity_id != other_id and position.x == other_position.x and position.y == other_position.y:
                    if entity_id in healths and other_id in healths:
                        healths[entity_id].health -= 10
                        healths[other_id].health -= 10
                        #print(f"Ant {entity_id} and Ant {other_id} fought at ({position.x}, {position.y})")

class HomeFindingSystem:
    def update(self, entities):
        # Ants look for new homes
        for entity_id, position in entities.get_components(PositionComponent).items():
            if entity_id in entities.get_components(HomeComponent):
                home = entities.get_components(HomeComponent)[entity_id]
                # Dummy logic for finding a new home
                if position.x < 20 and position.y < 20:
                    home.home_id = (position.x, position.y)
                    #print(f"Ant {entity_id} found a new home at ({position.x}, {position.y})")
