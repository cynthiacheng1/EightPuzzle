# Eight Puzzle Problem CS 4613
# Matthew Swartz (mcs871) and Cynthia Cheng (cc5469)

# global vars
initial = []
goalBoard = []
boardsUsed = []
clockwiseOrder = [[0,0],[0,1],[0,2],[1,2],[2,2],[2,1],[2,0],[1,0]]


# load in our 8 puzzle initial and goal states from input file given filename string
def loadInputFile(filename):
    # open input file 
    with open(filename) as file:
        lines = [line.rstrip() for line in file]

    # load in initial and goal boards
    for i in range(len(lines)):
        if (i < 3):
            initial.append([int(x) for x in lines[i].split()])
        elif (i > 3):
            goalBoard.append([int(x) for x in lines[i].split()])

class Node:
    def __init__(self, board, level, fval):
        # 2D array of tile placements
        self.board = board
        # node level in tree
        self.level = level
        # f value for this tile arrangement
        self.fval = fval
        # last move direction 
        self.movement = ""
        # keeping track of all previous boards for graph search 
        boardsUsed.append(board)

    # makes and returns a copy a 2D board array
    def copy(self, board):
        temp = []
        for i in board:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp

    #returns the coordinates of a number in a puzzle
    def find(self, puz, x):
        for i in range(0,len(self.board)):
            for j in range(0,len(self.board)):
                if puz[i][j] == x:
                    return i,j

    #helper function to move in a direction on the puzzle 
    #if position val are out of limits then return None
    def shuffle(self, puz, x1, y1, x2, y2):
        if x2 >= 0 and x2 < len(self.board) and y2 >= 0 and y2 < len(self.board):
            temp_puz = []
            temp_puz = self.copy(puz)
            temp = temp_puz[x2][y2]
            temp_puz[x2][y2] = temp_puz[x1][y1]
            temp_puz[x1][y1] = temp
            return temp_puz
        else:
            return None
    
    #generating each possibility of board movement : up down right left 
    def generate_child(self):
        x, y = self.find(self.board, 0)
        #values for each movement in every direction
        val_list = [[x, y - 1, "L"],[x, y + 1, "R"], [x - 1, y, "U"], [x + 1, y, "D"]]
        children = []
        for i in val_list:
            child = self.shuffle(self.board, x, y, i[0], i[1])
            if child is not None and child not in boardsUsed:
                # then create child node 
                child_node = Node(child, self.level + 1, 0)
                child_node.movement = i[2]
                children.append(child_node)
        return children


class Puzzle:
    def __init__(self):
        self.open = []
        self.closed = []
        self.solutionN = 0
        self.solutionAVals = []
        self.solutionfVals = []

    #returns the coordinates of a number in a puzzle
    def findCoordinates(self, num, board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if (num == board[i][j]):
                    return i,j

    #calcluates manhattan distance between initial and goal boards
    def calculateManhattan(self, initial, goal):
        total = 0
        for i in range(1,9):
            initial_x, initial_y = self.findCoordinates(i,initial)
            goal_x, goal_y = self.findCoordinates(i,goal)
            total += abs(initial_x-goal_x) + abs(goal_y-initial_y)
        return total

    #finds the next number tile when traveling in a clockwise circle 
    def findNext(self, num, board):
        num_x, num_y = self.findCoordinates(num,board)
        if (num_x == 1 and num_y == 0):
            return board[0][0]
        else:
            for j in range(len(clockwiseOrder)):
                if (clockwiseOrder[j][0] == num_x and clockwiseOrder[j][1] == num_y):
                    # gets the coordintes of the next tile in a clockwise circle 
                    coords = clockwiseOrder[j+1]
                    xcord = coords[0]
                    ycord = coords[1]
                    return board[xcord][ycord]

    #calculates hueristic#2 where 2 is added for every tile out of place when traveling ina  clockwise circle and 1 for an incorrect center tile 
    def clockWise(self, initial, goal):
        total = 0
        for c in range(len(clockwiseOrder)):
            # print(clockwiseOrder[c])
            num = initial[clockwiseOrder[c][0]][clockwiseOrder[c][1]]
            # print(num)
            #doesnt calculate for blank 
            if (num != 0):
                nextIntialNum = self.findNext(num, initial)
                nextGoalNum = self.findNext(num, goal)
                if (nextIntialNum != nextGoalNum):
                    total += 2
        if (initial[1][1] != goal[1][1]):
            total += 1
        return total

    def h1(self, initial, goal):
        return self.calculateManhattan(initial, goal)

    def h2(self, initial, goal):
        return 3*self.clockWise(initial, goal) + self.calculateManhattan(initial, goal)

    def f(self, start, goal):
        #choose which heuristic to test for here 
        return self.h2(start.board, goal) + start.level   

    def process(self):
        #initializing values for search 
        start = initial
        goal = goalBoard
        start = Node(start, 0, 0)
        start.fval = self.f(start, goal)
        
        #initializing node to start 
        self.open.append(start)
        
        while True:
            cur = self.open[0]
            self.solutionfVals.append(str(cur.fval))
            if cur.movement != "":
                self.solutionAVals.append(cur.movement)
            #if heuristic is 0 reached goal state 
            if(self.h2(cur.board,goal) == 0):
                solutionBoard = cur.board
                self.solutionN += 1
                #writing to file 
                f = open("output3h2.txt", "w+")
                for i in range(3):
                    for j in range(3):
                        f.write(str(initial[i][j]) + " ")
                    f.write("\n")
                f.write("\n")
                for i in range(3):
                    for j in range(3):
                        f.write(str(cur.board[i][j]) + " ")
                    f.write("\n")
                f.write("\n" + str(cur.level) + "\n" + str(self.solutionN) + "\n" + " ".join(self.solutionAVals) + "\n" + " ".join(self.solutionfVals))
                break
            for i in cur.generate_child():
                self.solutionN += 1
                # print(self.f(i,goal))
                i.fval = self.f(i,goal)
                self.open.append(i)
            self.closed.append(cur)
            del self.open[0]

            #sorted based on fval 
            self.open.sort(key = lambda x:x.fval,reverse=False)


loadInputFile("Input3.txt")
puz = Puzzle()
puz.process()

