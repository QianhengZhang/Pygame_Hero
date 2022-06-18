#! /usr/bin/env python3
''' Run cool maze generating algorithms. '''
from calendar import c
import random
import this
from tracemalloc import start
from sympy import true

class Cell:
    ''' Represents a single cell of a maze.  Cells know their neighbors
        and know if they are linked (connected) to each.  Cells have
        four potential neighbors, in NSEW directions.
    '''  
    def __init__(self, row, column):
        assert row >= 0
        assert column >= 0
        self.row = row
        self.column = column
        self.links = {}
        self.north = None
        self.south = None
        self.east  = None
        self.west  = None
        
    def link(self, cell, bidirectional=True):
        ''' Carve a connection to another cell (i.e. the maze connects them)'''
        assert isinstance(cell, Cell)
        self.links[cell] = True
        if bidirectional:
            cell.link(self, bidirectional=False)
        
    def unlink(self, cell, bidirectional=True):
        ''' Remove a connection to another cell (i.e. the maze 
            does not connect the two cells)
            
            Argument bidirectional is here so that I can call unlink on either
            of the two cells and both will be unlinked.
        '''
        assert isinstance(cell, Cell)
        del self.links[cell]
        if bidirectional:
            cell.unlink(self, bidirectional=False)
            
    def is_linked(self, cell):
        ''' Test if this cell is connected to another cell.
            
            Returns: True or False
        '''
        assert isinstance(cell, Cell)
        if (cell in self.links):
            return True
        return False
        
    def all_links(self):
        ''' Return a list of all cells that we are connected to.'''
        return self.links
        
    def link_count(self):
        ''' Return the number of cells that we are connected to.'''
        return len(self.links)
        
    def neighbors(self):
        ''' Return a list of all geographical neighboring cells, regardless
            of any connections.  Only returns actual cells, never a None.
        '''
        neighbors = [self.north, self.south, self.west, self.east]
        return neighbors
                
    def __str__(self):
        return f'Cell at {self.row}, {self.column}'
        

class Grid:
    ''' A container to hold all the cells in a maze. The grid is a 
        rectangular collection, with equal numbers of columns in each
        row and vice versa.
    '''
    
    def __init__(self, num_rows, num_columns):
        assert num_rows > 0
        assert num_columns > 0
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.grid = self.create_cells()
        self.connect_cells()
        
    def create_cells(self):
        ''' Call the cells into being.  Keep track of them in a list
            for each row and a list of all rows (i.e. a 2d list-of-lists).
            
            Do not connect the cells, as their neighbors may not yet have
            been created.
        '''
        grid = list()
        for i in range(self.num_rows):
            row = list()
            for j in range(self.num_columns):
                cell = Cell(i, j)
                row.append(cell)
            grid.append(row)
        return grid
            
    def connect_cells(self):
        ''' Now that all the cells have been created, connect them to 
            each other. 
        '''
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                # If in the first row, then the cells don't have a north neighbor
                if (i == 0):
                    # If it is the cell at the upper-left corner, then it dooesn't have a west neighbor
                    if (j == 0):    
                        self.grid[i][j].south = self.grid[i+1][j]
                        self.grid[i][j].east = self.grid[i][j+1]
                        continue
                    # If it is the cell at the upper-right corner, then it doesn't have an east neighbor
                    elif (j == self.num_columns - 1):
                        self.grid[i][j].south = self.grid[i+1][j]
                        self.grid[i][j].west = self.grid[i][j-1]
                        continue
                    # Otherwise, it is a normal cell on the first line.
                    else:
                        self.grid[i][j].south = self.grid[i+1][j]
                        self.grid[i][j].west = self.grid[i][j-1]
                        self.grid[i][j].east = self.grid[i][j+1]
                        continue
                
                # If in the last row, then the cells don't have a south neighbor
                if (i == self.num_rows - 1):
                    # If it is the cell at the lower-left corner, then it dooesn't have a west neighbor
                    if (j == 0):
                        self.grid[i][j].north = self.grid[i-1][j]
                        self.grid[i][j].east = self.grid[i][j+1]
                        continue
                    
                    # If it is the cell at the lower-right corner, then it doesn't have an east neighbor
                    elif (j == self.num_columns - 1):
                        self.grid[i][j].north= self.grid[i-1][j]
                        self.grid[i][j].west = self.grid[i][j-1]
                        continue

                    # Otherwise, it is a normal cell on the last line.
                    else:
                        self.grid[i][j].north = self.grid[i-1][j]
                        self.grid[i][j].west = self.grid[i][j-1]
                        self.grid[i][j].east = self.grid[i][j+1]
                        continue
                
                # If in the first column, then the cells don't have a west neighbor
                # We have ensured it isn't the upper-left nor the lower-left cell
                if (j == 0):
                    self.grid[i][j].north = self.grid[i-1][j]
                    self.grid[i][j].south = self.grid[i+1][j]
                    self.grid[i][j].east = self.grid[i][j+1]
                    continue

                # If in the last column, then the cells don't have a east neighbor
                # We have ensured it isn't the upper-right nor the lower-right cell
                if (j == self.num_columns - 1):
                    self.grid[i][j].north = self.grid[i-1][j]
                    self.grid[i][j].south = self.grid[i+1][j]
                    self.grid[i][j].west = self.grid[i][j-1]
                    continue

                # Finally we're left with normal cells in the grid
                self.grid[i][j].north = self.grid[i-1][j]
                self.grid[i][j].south = self.grid[i+1][j]
                self.grid[i][j].west = self.grid[i][j-1]
                self.grid[i][j].east = self.grid[i][j+1]
                
                        
                    
    def cell_at(self, row, column):
        ''' Retrieve the cell at a particular row/column index.'''
        return self.grid[row][column]
        
    def deadends(self):
        ''' Return a list of all cells that are deadends (i.e. only link to
            one other cell).
        '''
        deadends = list()
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                if self.grid[i][j].link_count() == 1:
                    deadends.append(self.grid[i][j])
        return deadends
                            
    def each_cell(self):
        ''' A generator.  Each time it is called, it will return one of 
            the cells in the grid.
        '''
        for row in range(self.num_rows):
            for col in range(self.num_columns):
                c = self.cell_at(row, col)
                yield c
                
    def each_row(self):
        ''' A row is a list of cells.'''
        for row in self.grid:
            yield row
               
    def random_cell(self):
        ''' Chose one of the cells in an independent, uniform distribution. '''
        row = random.randint(0, self.num_rows - 1)
        col = random.randint(0, self.num_columns - 1)
        return self.grid[row][col]
        
    def size(self):
        ''' How many cells are in the grid? '''
        return self.num_rows * self.num_columns
        
    def set_markup(self, markup):
        ''' Warning: this is a hack.
            Keep track of a markup, for use in representing the grid
            as a string.  It is used in the __str__ function and probably
            shouldn't be used elsewhere.
        '''
        self.markup = markup
        
    def __str__(self):
        ret_val = '+' + '---+' * self.num_columns + '\n'
        for row in self.grid:
            ret_val += '|'
            for cell in row:
                cell_value = self.markup[cell]
                ret_val += '{:^3s}'.format(str(cell_value))
                if not cell.east:
                    ret_val += '|'
                elif cell.east.is_linked(cell):
                    ret_val += ' '
                else:
                    ret_val += '|'
            ret_val += '\n+'
            for cell in row:
                if not cell.south:
                    ret_val += '---+'
                elif cell.south.is_linked(cell):
                    ret_val += '   +'
                else:
                    ret_val += '---+'
            ret_val += '\n'
        return ret_val
        
class Markup:
    ''' A Markup is a way to add data to a grid.  It is associated with
        a particular grid.
        
        In this case, each cell can have a single object associated with it.
        
        Subclasses could have other stuff, of course
    '''
    
    def __init__(self, grid, default=' '):
        self.grid = grid
        self.marks = {}  # Key: cell, Value = some object
        self.default = default
        
    def reset(self):
        self.marks = {}
        
    def __setitem__(self, cell, value):
        self.marks[cell] = value
        
    def __getitem__(self, cell):
        return self.marks.get(cell, self.default)
        
    def set_item_at(self, row, column, value):
        assert row >= 0 and row < self.grid.num_rows
        assert column >= 0 and column < self.grid.num_columns
        cell = self.grid.cell_at(row, column)
        if cell:
            self.marks[cell]=value
        else:
            raise IndexError
    
    def get_item_at(self, row, column):
        assert row >= 0 and row < self.grid.num_rows
        assert column >= 0 and column < self.grid.num_columns
        cell = self.grid.cell_at(row, column)
        if cell:
            return self.marks.get(cell)
        else:
            raise IndexError
            
    def max(self):
        ''' Return the cell with the largest markup value. '''
        return max(self.marks.keys(), key=self.__getitem__)

    def min(self):
        ''' Return the cell with the largest markup value. '''
        return min(self.marks.keys(), key=self.__getitem__)

class DijkstraMarkup(Markup):
    ''' A markup class that will run Djikstra's algorithm and keep track
        of the distance values for each cell.
    '''

    def __init__(self, grid, root_cell, default=0):
        ''' Execute the algorithm and store each cell's value in self.marks[] '''
        super().__init__(grid, default)
        queue = list()
        self.marks[root_cell] = 0
        queue.append(root_cell)
        while len(queue) > 0:
            current = queue.pop(0)
            if current.north != None:
                if current.north in current.links and current.north not in self.marks.keys():
                    queue.append(current.north)
                    self.marks.update({current.north: self.marks[current] + 1})

            if current.south != None:
                if current.south in current.links and current.south not in self.marks.keys():
                    queue.append(current.south)
                    self.marks.update({current.south: self.marks[current] + 1})

            if current.west != None:
                if current.west in current.links and current.west not in self.marks.keys():
                    queue.append(current.west)
                    self.marks.update({current.west: self.marks[current] + 1})

            if current.east != None:
                if current.east in current.links and current.east not in self.marks.keys():
                    queue.append(current.east)
                    self.marks.update({current.east: self.marks[current] + 1})  
            
    def farthest_cell(self):
        ''' Find the cell with the largest markup value, which will
            be the one farthest away from the root_call.
            
            Returns: Tuple of (cell, distance)
        '''
        distance = 0
        cell = None
        keys = list(self.marks.keys())
        for i in range(len(keys)):
            if (self.marks[keys[i]] > distance):
                cell, distance = keys[i], self.marks[keys[i]]
                distance = self.marks[keys[i]]
        return (cell, distance)

class ShortestPathMarkup(DijkstraMarkup):
    ''' Given a starting cell and a goal cell, create a Markup that will
        have the shortest path between those two cells marked.  
    '''

    def __init__(self, grid, start_cell, goal_cell, 
                 path_marker='*', non_path_marker=' '):
        super().__init__(grid, start_cell, default= non_path_marker)
        
        new_marks = {}
        cell = goal_cell
        new_marks[cell] = path_marker

        while cell != start_cell:
            step = self.marks[cell]
            links = cell.all_links()
            for cell_linked in links:
                if self.marks[cell_linked] == step - 1:
                    cell = cell_linked
                    break
            new_marks[cell] = path_marker
        
        keys = list(self.marks.keys())
        thisKey = list(new_marks.keys())
        for i in range(len(keys)):
            if keys[i] not in thisKey:
                new_marks[keys[i]] = non_path_marker
        self.marks = new_marks

class LongestPathMarkup(ShortestPathMarkup):
    ''' Create a markup with the longest path in the graph marked.
        Note: Shortest path is dependent upon the start and target cells chosen.
              This markup is the longest path to be found _anywhere_ in the maze.
    '''

    def __init__(self, grid, path_marker='*', non_path_marker=' '):
        start_cell = grid.random_cell()
        dm = DijkstraMarkup(grid, start_cell)
        farthest, _ = dm.farthest_cell()
        dm = DijkstraMarkup(grid, farthest)
        next_farthest, _ = dm.farthest_cell()   
        super().__init__(grid, farthest, next_farthest, path_marker, non_path_marker)

class ColorizedMarkup(Markup):
    ''' Markup a maze with various colors.  Each value in the markup is
        an RGB triplet.
    '''

    def __init__(self, grid, channel='R'):
        assert channel in 'RGB'
        super().__init__(grid)
        self.channel = channel
        
    def colorize_dijkstra(self, start_row = None, start_column = None):
        ''' Provide colors for the maze based on their distance from
            some cell.  By default, from the center cell.
        '''
        if not start_row:
            start_row = self.grid.num_rows // 2
        if not start_column:
            start_column = self.grid.num_columns // 2
        start_cell = self.grid.cell_at(start_row, start_column)
        dm = DijkstraMarkup(self.grid, start_cell)
        self.intensity_colorize(dm)
                
    def intensity_colorize(self, markup):
        ''' Given a markup of numeric values, colorize based on
            the relationship to the max numeric value.
        '''
        max = markup.max()
        max_value = markup[max]
        for c in self.grid.each_cell():
            cell_value = markup[c]
            intensity = (max_value - cell_value) / max_value
            dark   = round(255 * intensity)
            bright = round(127 * intensity) + 128
            if self.channel == 'R':
                self.marks[c] = [bright, dark, dark]
            elif self.channel == 'G':
                self.marks[c] = [dark, bright, dark]
            else:
                self.marks[c] = [dark, dark, bright]                             
            

def aldous_broder(grid):
    ''' The Aldous-Broder algorithm is a random-walk algorithm.
    
        Start in a random cell.  Choose a random direction.  If the cell
        in that direction has not been visited yet, link the two cells.
        Otherwise, don't link.
        Move to that randomly chosen cell, regardless of whether it was
        linked or not.
        Continue until all cells have been visited.
    '''

    iteration_count = 0
    visited = list()
    current = grid.random_cell()
    visited.append(current)
    while len(visited)!=grid.size():
        iteration_count += 1 
        direction = random.randint(0,3)
        
        if direction == 0 and current.north != None:
            if (current.north not in visited): 
                current.link(current.north)
                current = current.north
                visited.append(current)
            else:
                current = current.north
        
        if direction == 1 and current.south != None:
            if (current.south not in visited):
                current.link(current.south)
                current = current.south
                visited.append(current)
            else:
                current = current.south
        
        if direction == 2 and current.west != None:
            if (current.west not in visited):
                current.link(current.west)
                current = current.west
                visited.append(current)
            else:
                current = current.west

        if direction == 3 and current.east != None:
            if (current.east not in visited):
                current.link(current.east)
                current = current.east
                visited.append(current)
            else:
                current = current.east
