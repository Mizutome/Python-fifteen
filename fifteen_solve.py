"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            for col in range(self._width):  
                ans += " %2d "%(self._grid[row][col])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        target_value = target_col + self._width * target_row
        #print "target value =", target_value
        
        # Check 0 in (row, col) or not #
        if self._grid[target_row][target_col] != 0:
            print "0 is not in", (target_row, target_col)
            return False
        
        # Check (number > taget) are in position or not #
        for row in range(self._height):
            for col in range(self._width):
                if target_value < (col + self._width * row) and \
                   self._grid[row][col] != col + self._width * row:
                    print col + self._width * row,"is in" , self.current_position(row, col)
                    return False                   
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, target_col), "lower_row_invariant bad"
        assert target_row > 1, "target row <= 1"
        assert target_col != 0, "target col = 0"
        
        target_value = target_col + self._width * target_row
        current_row, current_col = self.current_position(target_row, target_col) 
        print "target value =", target_value
        print "target position =", (target_row, target_col)
        print "target is in", (current_row, current_col), "\n"
                
        
        move_string = ""
        move_row = -(current_row - target_row)
        move_col = current_col - target_col
        print "move_row=",move_row, "move_col=",move_col
        
        if move_row > 0 and move_col == 0:
            move_string += self.current_u_target(move_string, move_row)
        elif move_row == 0 and move_col < 0:
            move_string += self.current_l_target(move_string, move_col)
        elif move_row > 0 and move_col < 0:
            move_string += self.current_ul_target(move_string, move_row, move_col)
        elif move_row > 0 and move_col > 0:
            move_string += self.current_ur_target(move_string, move_row, move_col)        
        else:
            assert False, "Wrong move row or col"
        
        print "move_string=", move_string
        self.update_puzzle(move_string)
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        target_col = 0
        assert self.lower_row_invariant(target_row, target_col), "lower_row_invariant bad"
        assert target_row > 1, "target row <= 1"

        target_value = target_col + self._width * target_row
        current_row, current_col = self.current_position(target_row, target_col) 
        print "target value =", target_value
        print "target position =", (target_row, target_col)
        print "target is in", (current_row, current_col), "\n"

        move_string = ""
        move_row = -(current_row - target_row)
        move_col = current_col - target_col
        print "move_row=",move_row, "move_col=",move_col
        
        if move_row == 1 and move_col == 0:
            move_string += "ur"
        else:
            if move_row > 1 and move_col == 0:
                move_string += 'u' * move_row
                move_row -= 1
                while move_row >= 2:
                    move_string += "rddlu"
                    move_row -= 1
                move_string += "rdl" 
            else:
                move_string += 'u' * move_row
                move_string += 'r' * move_col                
                move_col -= 1
                while move_col >= 1:
                    if move_row == 1:
                        move_string += "ulldr"
                    else:
                        move_string += "dllur"
                    move_col -= 1
                if move_row == 1:
                    move_string += "l"
                else:
                    move_string += "dlu"
                    move_row -= 1
                    while move_row >= 2:
                        move_string += "rddlu"
                        move_row -= 1
                    move_string += "rdl"                    
            move_string += "ruldrdlurdluurddlur"                
        move_string += "r" * (self._width-2)
        
        print "move_string=", move_string
        self.update_puzzle(move_string)
        return move_string
    
    def current_u_target(self, move_string, move_row):
        """
        Add move string when move_row > 0, move_col = 0
        """
        
        #print "move_string bef:",move_string
        move_string += 'u' * move_row
        while move_row > 1:
            move_string += "lddru"
            move_row -= 1        
        move_string += "ld"
              
        #print "move_string aft:",move_string
        return move_string
    
    def current_l_target(self, move_string, move_col):
        """
        Add move string when move_row == 0, move_col < 0
        """
        
        #print "move_string bef:",move_string
        move_string += 'l' * (-move_col)
        while move_col < -1:
            move_string += "urrdl"
            move_col += 1        
              
        #print "move_string aft:",move_string
        return move_string    

    def current_ul_target(self, move_string, move_row, move_col):
        """
        Add move string when move_row > 0 , move_col < 0
        """
        
        #print "move_string bef:",move_string
        move_string += 'u' * move_row
        move_string += 'l' * (-move_col)
        while move_col < -1:
            move_string += "drrul"
            move_col += 1        
        move_string += "dru"
        while move_row > 1:
            move_string += "lddru"
            move_row -= 1        
        move_string += "ld"
        
        #print "move_string aft:",move_string
        return move_string   
    
    def current_ur_target(self, move_string, move_row, move_col):
        """
        Add move string when move_row > 0 , move_col > 0
        """
        
        #print "move_string bef:",move_string
        move_string += 'u' * move_row
        move_string += 'r' * move_col
        while move_col > 1:
            if move_row == 1:
                move_string += "ulldr"
            else:
                move_string += "dllur"
            move_col -= 1   
        
        if move_row == 1:
            move_string += "ul"
        else:
            move_string += "dlu" 
            move_row -= 1
            
        while move_row >= 1:        
            move_string += "lddru"
            move_row -= 1        
        move_string += "ld"
        
        #print "move_string aft:",move_string
        return move_string      
    
    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        target_row = 0
        #target_value = target_col + self._width * target_row
        #print "target value =", target_value
        
        # Check (row > 1) are in position or not #
        for row in range(self._height):
            for col in range(self._width):
                if (self._width * 2) <= (col + self._width * row) and \
                   self._grid[row][col] != col + self._width * row:
                    print col + self._width * row,"is in" , self.current_position(row, col)
                    return False
        # Check (row = 0 & col > j) (row = 1 & col >= j) are in position or not #
        for col in range(self._width):
            if col > target_col and self._grid[0][col] != col + self._width * 0:
                    print col + self._width * 0,"is in" , self.current_position(0, col)
                    return False
            if col >= target_col and self._grid[1][col] != col + self._width * 1:
                    print col + self._width * 1,"is in" , self.current_position(1, col)
                    return False                
        # Check 0 in (0, col) or not #
        if self._grid[target_row][target_col] != 0:
            print "0 is not in", (target_row, target_col)
            return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        target_row = 1
        #target_value = target_col + self._width * target_row
        #print "target value =", target_value
        
        # Check (row > 1) are in position or not #
        for row in range(self._height):
            for col in range(self._width):
                if (self._width * 2) <= (col + self._width * row) and \
                   self._grid[row][col] != col + self._width * row:
                    print col + self._width * row,"is in" , self.current_position(row, col)
                    return False
        # Check (row = 0 & col > j) (row = 1 & col >= j) are in position or not #
        for col in range(self._width):
            if col > target_col and self._grid[0][col] != col + self._width * 0:
                    print col + self._width * 0,"is in" , self.current_position(0, col)
                    return False
            if col > target_col and self._grid[1][col] != col + self._width * 1:
                    print col + self._width * 1,"is in" , self.current_position(1, col)
                    return False
        # Check 0 in (1, col) or not #
        if self._grid[target_row][target_col] != 0:
            print "0 is not in", (target_row, target_col)
            return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col), "solve_row0_tile bad"
        
        target_row = 0
        target_value = target_col + self._width * target_row
        current_row, current_col = self.current_position(target_row, target_col) 
        print "target value =", target_value
        print "target position =", (target_row, target_col)
        print "target is in", (current_row, current_col), "\n"
        
        move_string = ""
        move_row = -(current_row - target_row)
        move_col = current_col - target_col
        print "move_row=",move_row, "move_col=",move_col
        
        if move_row == 0 and move_col == -1:
            move_string += "ld"
        else:
            if move_row == -1 and move_col == -1: 
                move_string += "lld"
            else:
                move_string += "ld"
                if move_row == 0:
                    move_string += "l" * (-(move_col+1))
                    move_string += "u"
                    move_string += "r" * (-(move_col+1))
                    move_string += "d"
                    
                move_string += "l" * (-(move_col+1))
                move_col += 1
                while move_col < -1:
                    move_string += "urrdl"
                    move_col += 1
            move_string += "urdlurrdluldrruld"
        
        print "move_string=", move_string
        self.update_puzzle(move_string)
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col), "solve_row1_tile bad"
        
        target_row = 1
        target_value = target_col + self._width * target_row
        current_row, current_col = self.current_position(target_row, target_col) 
        print "target value =", target_value
        print "target position =", (target_row, target_col)
        print "target is in", (current_row, current_col), "\n"
        
        move_string = ""
        move_row = -(current_row - target_row)
        move_col = current_col - target_col
        print "move_row=",move_row, "move_col=",move_col
        
        if move_row == 1 and move_col == 0:
            move_string += "u"
        else:
            if move_row == 1:
                move_string += "l" * (-move_col)
                move_string += "u"
                move_string += "r" * (-move_col)
                move_string += "d"
            move_string += "l" * (-move_col)
            move_col += 1
            while move_col <= -1:
                move_string += "urrdl"
                move_col += 1        
            move_string += "ur"            
        
        print "move_string=", move_string
        self.update_puzzle(move_string)
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        assert self.row1_invariant(1), "solve_2x2 bad"
        move_string = "ul"
        self.update_puzzle("ul")
        while self.current_position(0, 1) != (0, 1):
            move_string += "drul"
            self.update_puzzle("drul")
        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        solution_string = ""
        for num in range((self._height*self._width-1), (self._width*2-1), -1):
            row = num/self._width
            col = num%self._width
            #print num, row, col
            #print self.__str__() 
            if self.current_position(row, col) == (row, col):
                continue
            elif self.current_position(0, 0) != (row, col):
                temp_zero_move = ""
                zero_row, zero_col = self.current_position(0, 0)
                move_row = -(zero_row - row)
                move_col = zero_col - col
                if move_col > 0: 
                    temp_zero_move += "l" * move_col
                elif move_col < 0: 
                    temp_zero_move += "r" * (-move_col)                    
                if move_row > 0: 
                    temp_zero_move += "d" * move_row 
                print "temp_zero_move=", temp_zero_move
                self.update_puzzle(temp_zero_move)
                solution_string += temp_zero_move
                
                #print self.__str__() 
           
            if row >= 2 and col == 0: 
                solution_string += self.solve_col0_tile(row)
            else: 
                solution_string += self.solve_interior_tile(row, col)  
                
        for num in range((self._width*2-1), 3, -1):
            row = num%2
            col = num/2           
            print num, row, col
            print self.__str__()
            if self.current_position(row, col) == (row, col):
                continue
            if self.current_position(0, 0) != (row, col):
                temp_zero_move = ""
                zero_row, zero_col = self.current_position(0, 0)
                move_row = -(zero_row - row)
                move_col = zero_col - col
                if move_col > 0: 
                    temp_zero_move += "l" * move_col
                elif move_col < 0: 
                    temp_zero_move += "r" * (-move_col)                    
                if move_row > 0: 
                    temp_zero_move += "d" * move_row 
                print "temp_zero_move=", temp_zero_move
                self.update_puzzle(temp_zero_move)
                solution_string += temp_zero_move
                
            if row == 0 and col >= 2:
                solution_string += self.solve_row0_tile(col)
            elif row == 1 and col >= 2:
                solution_string += self.solve_row1_tile(col)
        
        if (self.current_position(0, 1) != (0, 1)) or\
           (self.current_position(0, 0) != (0, 0)):        
            solution_string += self.solve_2x2()    
        
        return solution_string

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))

#test_grid = [[1,6,9,8],[4,5,2,7],[3,0,10,11],[12,13,14,15]]
#test_grid = [[1,6,9,8],[4,5,2,13],[3,10,7,11],[12,0,14,15]]
#test_grid = [[1,10,9,8],[4,6,5,7],[14,12,2,11],[3,13,0,15]]
#test_grid = [[1,6,9,8],[4,5,2,3],[12,10,7,11],[0,13,14,15]]
#test_grid = [[3,1,6,0],[4,5,2,7],[8,9,10,11],[12,13,14,15]]
#test_grid = [[1,5,2,3],[4,15,6,7],[8,9,10,11],[12,13,14,0]]
#puzzle_test = Puzzle(4, 4,test_grid)
#puzzle_test = Puzzle(3, 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
#puzzle_test = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#puzzle_test = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
#puzzle_test = Puzzle(3, 6, [[16, 7, 13, 17, 5, 9], [3, 0, 14, 10, 12, 6], [4, 15, 2, 11, 8, 1]])
#puzzle_test = Puzzle(2, 4, [[0, 3, 2, 7], [4, 5, 6, 1]])
#print puzzle_test

#print "current_position =", puzzle_test.current_position(2,1)
#print "lower_row_invariant =", puzzle_test.lower_row_invariant(2, 1)
#print "lower_row_invariant =", puzzle_test.lower_row_invariant(3, 1)
#print puzzle_test.solve_interior_tile(2, 1)
#print puzzle_test.solve_col0_tile(3)
#print "row0 method=", puzzle_test.row0_invariant(2)
#print "row1 method=", puzzle_test.row1_invariant(2)
#print puzzle_test.solve_row0_tile(3)
#print puzzle_test.solve_2x2()
#print puzzle_test.solve_puzzle()
#print puzzle_test

#obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#print obj
#obj.solve_interior_tile(2, 2)
