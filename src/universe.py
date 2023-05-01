class Universe:
    def __init__(self,
                 state: dict = {},
                 max_storage: int = -1) -> None:
        self.current_state = state
        self.queue = {}
        self.max_storage = max_storage
        self.previous = []
    
    def add_to_update_queue(self,
                            cell: tuple[int, ...], 
                            new_value: int) -> None:
        if cell not in self.queue:
            self.queue[cell] = new_value
            return
        error = f"The cell {cell} can only be updated once per queue. " + \
                       f"Its queued values are: {self.queue[cell]} and {new_value}."
        raise KeyError(error)
    
    def get_cell_states(self,
                        cells: list|dict) -> dict:
        '''
        Returns a dict containing the values of the non-zero cells of the input iterable.
        '''
        return {cell: self.current_state[cell] 
                for cell in cells if cell in self.current_state}
                
    def update_current_state(self):
        '''Updates the current state to be the queue'''
        self.previous.append(self.current_state)
        self.current_state = self.queue
        self.queue = {}
        
        if self.max_storage == -1:
            return 
        if len(self.previous) > self.max_storage: 
            self.previous =  self.previous[1:]