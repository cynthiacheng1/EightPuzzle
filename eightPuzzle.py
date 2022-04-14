
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

print(findCoordinates(1,initial))

def calculateManhattan(initial, goal):
    total = 0
    for i in range(1,9):
        initial_x, initial_y = findCoordinates(i,initial)
        goal_x, goal_y = findCoordinates(i,goal)
        total += abs(initial_x-goal_x) + abs(goal_y-initial_y)
    return total
print(calculateManhattan(initial, goal))


