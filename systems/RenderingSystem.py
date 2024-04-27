import pygame
import sys
from components.components import PositionComponent, RenderComponent
from components.MapComponent import MapComponent

class RenderingSystem:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))  # Set the screen size
        self.zoom = 1.0  # Initial zoom level

    def update(self, entities):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_EQUALS:  # Zoom in
                    self.zoom *= 1.1
                elif event.key == pygame.K_MINUS:  # Zoom out
                    self.zoom /= 1.1

        self.screen.fill((255, 255, 255))  # Clear the screen
        
        map_components = entities.get_components(MapComponent)
        for entity_id, map_component in map_components.items():
            map_component.display(self.screen, self.zoom)  # Render the map onto the screen

        positions = entities.get_components(PositionComponent)
        renders = entities.get_components(RenderComponent)

        for entity_id, position in positions.items():
            if entity_id in renders:
                render = renders[entity_id]
                pygame.draw.circle(self.screen, render.color, (int(position.x * self.zoom), int(position.y * self.zoom)), int(render.size * self.zoom))

        pygame.display.flip()  # Update the display