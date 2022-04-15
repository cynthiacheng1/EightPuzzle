# open input file 
with open("Input3.txt") as file:
    lines = [line.rstrip() for line in file]

# global vars
initial = []
goalBoard = []
clockwiseOrder = [[0,0],[0,1],[0,2],[1,2],[2,2],[2,1],[2,0],[1,0]]

# load in initial and goal states
for i in range(len(lines)):
    if (i < 3):
        # for x in lines[i].split():
        #     initial.append(int(x))
        initial.append([int(x) for x in lines[i].split()])
    elif (i > 3):
        # for x in lines[i].split():
        #     goal.append(int(x))
        goalBoard.append([int(x) for x in lines[i].split()])

class Node:
    def __init__(self, board, level, fval):
        self.board = board
        self.level = level
        self.fval = fval
        
    def generate_child(self):
        x, y = self.find(self.board, 0)
        val_list = [[x, y - 1],[x, y + 1], [x - 1, y], [x + 1, y]]
        children = []
        for i in val_list:
            child = self.shuffle(self.board, x, y, i[0], i[1])
            if child is not None:
                child_node = Node(child, self.level + 1, 0)
                children.append(child_node)
        return children
    
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
            

    def copy(self, root):
        temp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp    
            
    def find(self, puz, x):
        for i in range(0,len(self.board)):
            for j in range(0,len(self.board)):
                if puz[i][j] == x:
                    return i,j


class Puzzle:
    def __init__(self):
        self.open = []
        self.closed = []

    def findCoordinates(self, num, board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if (num == board[i][j]):
                    return i,j

    def calculateManhattan(self, initial, goal):
        total = 0
        for i in range(1,9):
            initial_x, initial_y = self.findCoordinates(i,initial)
            goal_x, goal_y = self.findCoordinates(i,goal)
            total += abs(initial_x-goal_x) + abs(goal_y-initial_y)
        return total

    def findNext(self, num, board):
        num_x, num_y = findCoordinates(num,board)
        if (num_x == 1 and num_y == 0):
            return board[0][0]
        else:
            for j in range(len(clockwiseOrder)):
                if (clockwiseOrder[j][0] == num_x and clockwiseOrder[j][1] == num_y):
                    coords = clockwiseOrder[j+1]
                    xcord = coords[0]
                    ycord = coords[1]
                    return board[xcord][ycord]

    def clockWise(self, initial, goal):
        total = 0
        for c in range(len(clockwiseOrder)):
            num = initial[clockwiseOrder[c][0]][clockwiseOrder[c][1]]
            if (num != 0):
                nextIntialNum = findNext(num, initial)
                nextGoalNum = findNext(num, goal)
                if (nextIntialNum != nextGoalNum):
                    total += 2
        if (initial[1][1] != goal[1][1]):
            total += 1
        return total

    def h1(self, initial, goal):
        return self.calculateManhattan(initial, goal)

    def h2(self, intial, goal):
        return 3*clockWise(initial, goal) + calculateManhattan(intial, goal)

    def f(self, start, goal):
        return self.h1(start.board, goal) + start.level   

    def process(self):
        start = initial
        goal = goalBoard
        
        start = Node(start, 0, 0)
        start.fval = self.f(start, goal)
        
        self.open.append(start)
        print("\n\n")
        while True:
            cur = self.open[0]
            print("")
            print("  | ")
            print("  | ")
            print(" \\\'/ \n")
            for i in cur.board:
                for j in i:
                    print(j,end=" ")
                print("")
            """ If the difference between current and goal node is 0 we have reached the goal node"""
            if(self.h1(cur.board,goal) == 0):
                break
            for i in cur.generate_child():
                i.fval = self.f(i,goal)
                self.open.append(i)
            self.closed.append(cur)
            del self.open[0]

            """ sort the opne list based on f value """
            self.open.sort(key = lambda x:x.fval,reverse=False)


puz = Puzzle()
puz.process()
        

