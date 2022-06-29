# Originally, the whole program was going to be a basic terminal interface that would redraw the board every time you made a move
# instead of selecting a point visually, you would have had to type where you wanted it. ex: (0,0), (2,1), etc.
# Now this class holds an internal board that keeps track of what is being displayed to the terminal.
# Kind of like an internal server for the game, though really, really simple.

class Game():

    def __init__(self):
        self.grid = [["","",""],
                    ["",""," "],
                    ["","",""]]
        self.turn = True
    # True means X turn
    # False means O turn

    def drawGrid(self):
        #print(f"{self.grid[0][0]} | {self.grid[0][1]} | {self.grid[0][2]}")
        print(f"\033[4m{self.grid[0][0]}|{self.grid[0][1]}|{self.grid[0][2]}\033[0m")
        #print(f"—————————")
        print(f"\033[4m{self.grid[1][0]}|{self.grid[1][1]}|{self.grid[1][2]}\033[0m")
        #print(f"—————————")
        print(f"{self.grid[2][0]}|{self.grid[2][1]}|{self.grid[2][2]}")

    def play(self,x,y):
        match self.turn:
            case True: self.grid[y][x] = "X";
            case False: self.grid[y][x] = "O"
            case _: pass
        self.turn = not self.turn

    def checkRow(self, r):
        rc = 0
        for i in r:
            if i: rc+=1
        return rc

    def checkWinner(self, line, col):

        Xc = [False, False, False]
        Oc = [False, False, False]
        N = False

        pos = 0
        for i in self.grid:                     #Checks:
            if i[col] == "X": Xc[pos] = True    #X |   |  
            if i[col] == "O": Oc[pos] = True    #X |   |  
            pos+=1                              #X |   |  
        if self.checkRow(Xc) == 3: return "X"
        if self.checkRow(Oc) == 3: return "O"

        Xc = [False, False, False]
        Oc = [False, False, False]
        pos = 0
        for i in self.grid[line]:               #Checks:
            if i == "X": Xc[pos] = True         #  |   |  
            if i == "O": Oc[pos] = True         #X | X | X
            pos+=1                              #  |   |  
        if self.checkRow(Xc) == 3: return "X"
        if self.checkRow(Oc) == 3: return "O"


        if line==col:
            Xc = [False, False, False]
            Oc = [False, False, False]
            pos = 0
            for i in range(3):                              #Checks:
                if self.grid[i][i] == "X": Xc[pos] = True   #X |   |  
                if self.grid[i][i] == "O": Oc[pos] = True   #  | X |  
                pos+=1                                      #  |   | X
            if self.checkRow(Xc) == 3: return "X"
            if self.checkRow(Oc) == 3: return "O"

        if line+col == 2:
            Xc = [False, False, False]
            Oc = [False, False, False]
            pos = 0
            for i,j in zip(range(3), range(3).__reversed__()):  #Checks:
                if self.grid[i][j] == "X": Xc[pos] = True       #  |   | X
                if self.grid[i][j] == "O": Oc[pos] = True       #  | X |  
                pos += 1                                        #X |   |  
            if self.checkRow(Xc) == 3: return "X"
            if self.checkRow(Oc) == 3: return "O"

        for i in self.grid:
            for j in i:
                if j == "":
                    N =True
        if N: return "N"
        return "T"

    def newGame(self):
        self.grid = [["","",""],["","",""],["","",""]]
        self.turn = True