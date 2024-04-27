import pygame
import random

import heapq


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0  # Cost from the start node to this node
        self.h = 0  # Estimated cost from this node to the goal node
        self.parent = None

    def f(self):
        return self.g + self.h


class MapComponent:
    def __init__(self, width, height):
        # Initializes a map with empty terrain
        self.width = width
        self.height = height
        self.terrain = [[' ' for _ in range(height)] for _ in range(width)]
        self.food_sources = []  # List of (x, y) tuples where food is available
        
        self.above_ground = 10
        
        self.generate_terrain()
        self.generate_caverns()
        
        self.has_changed = True
        
    def generate_terrain(self):
        for y in range(self.height):
            if y < self.above_ground:
                continue
            for x in range(self.width):
                self.terrain[x][y] = 'D'  # Representing dirt
                    
    def generate_caverns(self):
        # Dig out caverns using cellular automata or random walk algorithm
        for _ in range(20):  # Repeat the process a few times for larger caverns
            # Start the random walk from the surface
            x, y = random.randint(0, self.width - 1), self.above_ground
            for _ in range(1000):  # Perform 1000 random walk steps
                self.terrain[x][y] = ' '  # Dig out the rock
                dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
                x, y = max(0, min(x + dx, self.width - 1)), max(self.above_ground, min(y + dy, self.height - 1))
                
    

    def add_food(self, x, y):
        self.terrain[x][y] = 'F'  # Marking food sources on the map
        self.food_sources.append((x, y))

    def is_food(self, x, y):
        return self.terrain[x][y] == 'F'
    
    def smell_food(self, x, y, radius):
        # Smell for food sources within a certain radius
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < self.width and 0 <= new_y < self.height and self.terrain[new_x][new_y] == 'F':
                    return new_x, new_y
                
        return None, None  # Return the current position if no food is found
    
    def find_path(self, start_x, start_y, goal_x, goal_y):
        open_set = []
        closed_set = set()

        start_node = Node(start_x, start_y)
        goal_node = Node(goal_x, goal_y)

        heapq.heappush(open_set, (0, start_node))  # Add the start node to the open set

        while open_set:
            current = heapq.heappop(open_set)[1]

            if (current.x, current.y) == (goal_node.x, goal_node.y):
                path = []
                while current:
                    path.append((current.x, current.y))
                    current = current.parent
                return path[::-1]  # Return the path in reverse (from start to goal)

            closed_set.add((current.x, current.y))

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Adjacent nodes
                new_x, new_y = current.x + dx, current.y + dy
                if 0 <= new_x < self.width and 0 <= new_y < self.height and self.terrain[new_x][new_y] != 'D' and (new_x, new_y) not in closed_set:
                    neighbor = Node(new_x, new_y)
                    neighbor.g = current.g + 1  # Assuming a cost of 1 to move to an adjacent node
                    neighbor.h = abs(neighbor.x - goal_node.x) + abs(neighbor.y - goal_node.y)  # Manhattan distance heuristic
                    neighbor.parent = current
                    heapq.heappush(open_set, (neighbor.f(), neighbor))

        return None  # No path found

    def display(self, screen, zoom=1.0):
        block_size = 1  # Size of each block for displaying the map
        colors = {
            ' ': (255, 255, 255),  # Empty space color
            'F': (0, 255, 0),  # Food color
            'D': (50, 50, 50)  # Dirt color
        }

        map_surface = pygame.Surface((self.width * block_size, self.height * block_size))  # Create a surface for the map
        map_surface.fill((0, 0, 0))  # Fill the map surface with black background

        for y in range(self.height):
            for x in range(self.width):
                color = colors[self.terrain[x][y]]
                pygame.draw.rect(map_surface, color, (x * block_size, y * block_size, block_size, block_size))

        for food_source in self.food_sources:
            pygame.draw.circle(map_surface, colors['F'], (food_source[0] * block_size + block_size // 2, food_source[1] * block_size + block_size // 2), 2)

        scaled_map_surface = pygame.transform.scale(map_surface, (int(self.width * block_size * zoom), int(self.height * block_size * zoom)))  # Scale the map surface based on the zoom level
        screen.blit(scaled_map_surface, (0, 0))  # Render the scaled map surface onto the main screen

