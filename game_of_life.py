from src.automata import Automata


initial = {(0,0): 1, (0,1): 1, (1,1): 1}

class GameOfLife(Automata):
    def __init__(self, initial_state = {}, max_storage = -1) -> None:
        super().__init__(initial_state, max_storage)
    
    def _neighbors(self, cell: tuple[int, int]):
        x, y = cell
        neighbors = []
        for i in [1,-1, 0]:
            for j in [1,-1, 0]:
                neighbors.append((x + i, y + j))
        neighbors.remove(cell)
        return neighbors
        
    def _candidates_for_update(self):
        candidates = []
        for cell in self.universe.current_state.keys():
            candidates.append(cell)
            candidates += self._neighbors(cell)
        return set(candidates)
                    
    def _living_neighbors_count(self, cell: tuple[int, int]):
        neighbors = self._neighbors(cell)
        return len(self.universe.get_cell_states(neighbors))
    
    def update(self):
        candidates = self._candidates_for_update()
        for cell in set(candidates):
            neighbors = self._living_neighbors_count(cell)
            alive = cell in self.universe.current_state
            if (alive and (neighbors == 2 or neighbors == 3)) or \
               (not alive and neighbors == 3):
                self.universe.add_to_update_queue(cell, 1)
        self.universe.update_current_state()
        

def main():
    from src.visualizer import Vis2DTerminal
    import os
    import time
    import curses
    
    # Initialize with a glider.
    gol = GameOfLife({(0,0): 1, (0,1): 1, (0,2): 1, (-1,2): 1, (-2,1): 1},
                     max_storage = 0)
    
    # Initialize with glider gun.
    
    # gol = GameOfLife()
    # initial = gol.state_input_from_file("gol_input.txt", Automata.FileFormat.RLE)
    # gol.universe.change_initial_state(initial)
    
    vis = Vis2DTerminal()
    while True:
        try:
            vis.update_state(gol.universe.current_state)
            vis.window_render()
        
            gol.update()
        
            if not gol.universe.current_state:
                print("Life has been extinguished.")
                break
        except Exception as e:
            vis.shutdown()
            print(e)
            break
    vis.shutdown()
    return
   
   
if __name__ == "__main__":
    main()