from components.components import (
    PositionComponent, HealthComponent, HomeComponent,
    FoodComponent, AntTypeComponent, RenderComponent, TaskComponent
)

from components.EggComponent import EggComponent

def create_ant(manager, x, y, ant_type='worker'):
    components = [
        PositionComponent(x, y),
        HealthComponent(),
        FoodComponent(),
        HomeComponent(home_id=0),
        AntTypeComponent(type=ant_type)
    ]
    
    if ant_type == 'queen':
        components.append(EggComponent())
        components.append( RenderComponent(color='purple', size=2) )
        components.append( TaskComponent( "create_brood", x, y ) )
    elif ant_type == 'worker':
        components.append( RenderComponent(color='black', size=1) )
        components.append( TaskComponent( "explore", x, y ) )
    elif ant_type == 'baby':
        components.append( RenderComponent(color='gray', size=0.5) )
        components.append( TaskComponent( "grow", x, y ) )
                
    return manager.create_entity(components)