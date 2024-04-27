class EntityManager:
    def __init__(self):
        self.next_entity_id = 0
        self.entities = {}  # Maps entity ID to a list of components
        self.components_by_class = {}

    def create_entity(self, components):
        entity_id = self.next_entity_id
        self.next_entity_id += 1
        self.entities[entity_id] = components
        for component in components:
            if type(component) not in self.components_by_class:
                self.components_by_class[type(component)] = {}
            self.components_by_class[type(component)][entity_id] = component
        return entity_id

    def get_components(self, component_type):
        return self.components_by_class[component_type]
