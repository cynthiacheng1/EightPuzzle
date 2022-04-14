
with open("Input1.txt") as file:
    lines = [line.rstrip() for line in file]

initial = []
goal = []

for i in range(len(lines)):
    if (i < 3):
        # for x in lines[i].split():
        #     initial.append(int(x))
        initial.append([int(x) for x in lines[i].split()])
    elif (i > 3):
        # for x in lines[i].split():
        #     goal.append(int(x))
        goal.append([int(x) for x in lines[i].split()])

print(initial)
print(goal)

def findCoordinates(num,board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if (num == board[i][j]):
                return i,j

# print(findCoordinates(1,initial))

def calculateManhattan(initial, goal):
    total = 0
    for i in range(1,9):
        initial_x, initial_y = findCoordinates(i,initial)
        goal_x, goal_y = findCoordinates(i,goal)
        total += abs(initial_x-goal_x) + abs(goal_y-initial_y)
    return total
# print(calculateManhattan(initial, goal))


clockwiseOrder = [[0,0],[0,1],[0,2],[1,2],[2,2],[2,1],[2,0],[1,0]]

def findNext(num,board):
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
# print(findNext(1,initial))


def clockWise(initial, goal):
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
        
print(clockWise(initial, goal))

def h2(intial,goal):
    return 3*clockWise(initial,goal) + calculateManhattan(intial,goal)


