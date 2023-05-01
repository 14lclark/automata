from src.universe import Universe

class Automata:
    '''Base class for a cellular automata.'''
    def __init__(self, initial_state: dict = {}, max_storage: int = -1) -> None:
        self.universe = Universe(initial_state, max_storage)
    
    def update(self):
        raise NotImplementedError()
    
    def view_raw_state(self):
        print(self.universe.current_state)
        return self.view_count
    
    