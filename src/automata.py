from src.universe import Universe
from enum import Enum, auto, unique

class Automata:
    '''Base class for cellular automata.'''
    def __init__(self, initial_state: dict = {}, max_storage: int = -1) -> None:
        self.universe = Universe(initial_state, max_storage)
        
    def update(self):
        raise NotImplementedError()
    
    def view_raw_state(self):
        print(self.universe.current_state)
        return self.view_count
    
    def state_input_from_file(self, file_name: str, format) -> dict:
        '''
        The file file_name should be a text file, possibly with a .rle extension. 
        The format is an element of the Automata.FileFormat enum.
        '''
        with open(file_name) as file:
            if format == self.FileFormat.BIN:
                return self._binary_state_input(file)
            elif format == self.FileFormat.RLE:
                return self._rle_state_input(file)
            elif format == self.FileFormat.CRD:
                return self._coords_state_input(file)
            
    def _binary_state_input(self, file):
        y = 0
        state = {}
        for line in file:
            for x, ch in enumerate(line.rstrip()):
                if ch != '0':
                    state[(x,y)] = int(ch)
            y += 1
        return state
    
    def _rle_state_input(self, file):
        def to_int(a): 
            if a == "": return 1 
            return int(a)

        state = {}
        self.y = 5
        self.x = 10    
        
        digits = [str(i) for i in range(10)]
        cells = ["b","o","$"]
        allowed = digits + cells      
        
        def parse(rle):
            current_num = ""
            for c in rle:
                if c == "!":
                    return True
                elif c == "$":
                    for _ in range(to_int(current_num)):
                        self.y += 1
                    self.x = 10
                    current_num = ""
                    
                elif c not in allowed:
                    err = f"parsing error: \"{c}\" is not in the list of allowed characters"
                    raise ValueError(err)
                elif c in digits:
                    current_num += c
                elif c in cells:
                    if c == "b":
                        self.x += to_int(current_num)
                        current_num = ""
                    elif c == "o":
                        for _ in range(to_int(current_num)):
                            state[(self.x,self.y)] = 1
                            self.x += 1
                        current_num = ""

        rle = ""
        for line in file:
            # ignore header info for now
            if line[0] not in allowed:
                continue
            rle += line.rstrip()
            
        if parse(rle):
            return state
        else:
            raise EOFError("Didn't find RLE ending. (Missing a \'!\'?)")
                
    def _coords_state_input(file):
        state = {}
        for line in file:
            coord, val = line.rstrip().split(":")
            coord = coord[1:-1].split(',')
            coord = [int(elt) for elt in coord]
            state[tuple(coord)] = int(val)
        return state
    
    @unique
    class FileFormat(Enum):
        BIN = auto() # 1 for alive 0 for dead
        RLE = auto() # Run Length Encoded format
        CRD = auto() # coordinates of living cells, 1 per line eg (1,3):1