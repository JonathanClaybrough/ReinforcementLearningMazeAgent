"""
Program by Jonathan Claybrough to simulate an agent walking through a
maze using Q-learning to find the optimal path
Initialize a Maze(sizex, sizey)
then maze.fill_with_proba(empty_chance)
then initalise an Agent=
"""
from random import random, randint


class Maze:
    """
    A maze contains a sizex by sizey matrix of squares and associated Q matrix
    """
    def __init__(self, sizex, sizey):
        self.sizex = sizex
        self.sizey = sizey
        self.squares = []
        self.q_matrix = Q_matrix(self)

    def visualizeMaze(self):
        """Displays in console the position of walls and empty space"""
        for y in range(self.sizey):
            line = ""
            for x in range(self.sizex):
                if self.squares[x][y].state:
                    line += "o "
                else:
                    line += "x "
            print(line)

    def visualizeReward(self):
        """Displays in console the reward associated with each square"""
        for y in range(self.sizey):
            line = ""
            for x in range(self.sizex):
                line += str(self.squares[x][y].reward) + " "
            print(line)

    def visualizePath(self):
        """Displays the action the Actor prefers for each square"""
        for y in range(self.sizey):
            line = ""
            for x in range(self.sizex):
                actionID = 0
                optValue = -10000
                idnum = self.id_from_coord(x, y)
                for i, value in enumerate(self.q_matrix.matrix[idnum]):
                    # print("i= "+ str(i)+"  value=" + str(value))
                    if value > optValue:
                        optValue = value
                        actionID = i
                line += Q_matrix.symbolFromActionID[actionID] + " "
            print(line)

    def visualizeHistory(self):
        """ What is this ??? """
        for y in range(self.sizey):
            line = ""
            for x in range(self.sizex):
                self.q_matrix.nb
                actionID = 0
                optValue = -10000
                idnum = self.id_from_coord(x, y)
                for i, value in enumerate(self.q_matrix.matrix[idnum]):
                    # print("i= "+ str(i)+"  value=" + str(value))
                    if value > optValue:
                        optValue = value
                        actionID = i
                line += Q_matrix.symbolFromActionID[actionID] + " "

    def fill_with_proba(self, empty_chance):
        """Generates the maze with proba empty_chance for each square to be empty"""
        self.squares = []
        for x in range(self.sizex):
            column = []
            for y in range(self.sizey):
                column.append(Square(x, y, random() <= empty_chance))
            self.squares.append(column)
        self.squares[0][0].state = 1
        self.squares[0][0].reward = -1
        self.squares[self.sizex-1][self.sizey-1].state = 1
        self.squares[self.sizex-1][self.sizey-1].reward = 10

    def get_square(self, x, y):
        return squares[x][y]

    def set_goal(self, x, y):
        squares[x][y].reward = 100

    def id_from_coord(self, x, y):
        return x + self.sizex * y

    def coord_from_id(self, idnum):
        return [idnum % sizex, idnum/sizex]


class Square:
    """state = true if open, false if wall"""
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state
        if self.state:
            self.reward = -1
        else:
            self.reward = -9

    def __repr__(self):
        if self.state:
            return "o"
        else:
            return "x"


class Policy:
    def __init__(self, maze):
        self.maze = maze

    def choose_action(self, idnum):
        """Returns an action taken from Q_matrix.actionFromActionID"""
        pass


class RandomPolicy(Policy):
    def choose_action(self):
        actionID = randint(0,7)
        return Q_matrix.actionFromActionID[actionID]


class GreedyPolicy(Policy):
    def choose_action(self, idnum):
        actionID = 0
        optValue = -10000
        for i,value in enumerate(self.maze.q_matrix.matrix[idnum]):
            if value > optValue :
                optValue = value
                actionID= i
        return Q_matrix.actionFromActionID[actionID]


class EpsilonGreedyPolicy(GreedyPolicy):
    """Chooses greedy action epsilon ratio of times"""
    def __init__(self, maze, epsilon):
        super().__init__(maze)
        self.epsilon = epsilon # %chance over which to be greedy

    def choose_action(self, idnum):
        if random() > self.epsilon:
            return RandomPolicy(maze).choose_action()
        else :
            return super().choose_action(idnum)

class Agent:
    """Agent has a position, maze he's in, polic and logging behaviour
    When logging == True, the Agent outputs to console its position when moving in the maze
    """
    def __init__(self, maze, policy, gamma, logging):
        self.maze = maze
        self.policy = policy
        self.gamma = gamma
        self.x = 0
        self.y = 0
        self.logging = logging

    def playTurn(self, policy=None, maze=None):
        if policy==None:
            policy = self.policy
        if maze==None:
            maze = self.maze
        action = policy.choose_action(maze.id_from_coord(self.x, self.y))
        if self.logging:
            print("x=" + str(self.x) + ", y=" + str(self.y)+ "action=" + str(action)) 
        actionID = maze.q_matrix.actionIDFromAction[action]
        newx = self.x+action[0]
        newy = self.y+action[1]
        if (newx < 0 or newy < 0 or newx >= maze.sizex or newy >= maze.sizey) or not maze.squares[newx][newy].state:
            newx = self.x
            newy = self.y
        reward = maze.squares[newx][newy].reward
        squareID = maze.id_from_coord(self.x, self.y)
        newSquareID = maze.id_from_coord(newx, newy)
        maze.q_matrix.nbTimesVisitedMatrix[squareID][actionID] += 1
        alpha = 1/maze.q_matrix.nbTimesVisitedMatrix[squareID][actionID]
        maze.q_matrix.matrix[squareID][actionID] = maze.q_matrix.matrix[squareID][actionID] + alpha*(reward +
            self.gamma*max(maze.q_matrix.matrix[newSquareID])- maze.q_matrix.matrix[squareID][actionID])
        self.x = newx
        self.y = newy

    def playGame(self, policy, maze):
        """Sets the agent to the start of the maze and has his take actions until he suceeds (limited to 100000 turns)"""
        self.x= 0
        self.y= 0
        counter = 0
        self.nbTimesVisitedMatrix=[[0,0,0,0,0,0,0,0] for i in range(maze.sizex*maze.sizey)] #matrix[squareID][action] = nb times visited
        while not(self.x == maze.sizex-1 & self.y == maze.sizey -1):
            counter += 1
            self.playTurn(policy, maze)
            if counter > 100000:
                print("The game did not finish as it is taking over 100000 turns to finish")
                break

    def playGames(self, nb_tries):
        """Sets the agent to play nb_tries games"""
        for i in range(nb_tries):
            self.playGame(self.policy, self.maze)

class Q_matrix:
    def __init__(self, maze):
        self.maze = maze
        self.matrix=[[0,0,0,0,0,0,0,0] for i in range(maze.sizex*maze.sizey)] #matrix[squareID][action] = q value for that action
        self.nbTimesVisitedMatrix=[[0,0,0,0,0,0,0,0] for i in range(maze.sizex*maze.sizey)] #matrix[squareID][action] = q value for that action

    actionFromActionID={0:(0,1),1:(1,0),2:(0,-1),3:(-1,0),4:(1,1),5:(1,-1),6:(-1,1),7:(-1,-1)}
    actionIDFromAction={(0,1):0,(1,0):1,(0,-1):2,(-1,0):3,(1,1):4,(1,-1):5,(-1,1):6,(-1,-1):7}
    symbolFromActionID={0:"D",1:"R",2:"U",3:"L",4:"3",5:"9",6:"1",7:"7"}

# This is an example setup where a 9 by 9 maze is generated and shown to console, and an agent with policy epsilonGreedy is initialized
maze = Maze(9,9)
maze.fill_with_proba(0.5)
maze.visualizeMaze()
epsilonGreedyPolicy = EpsilonGreedyPolicy(maze, 0.7)
agent = Agent(maze, epsilonGreedyPolicy, 0.9, 0)
agentWithLogging = Agent(maze, epsilonGreedyPolicy, 0.9, 1)
greedyAgent = Agent(maze, GreedyPolicy(maze), 0.9, 0)
greedyAgentWithLogging = Agent(maze, GreedyPolicy(maze), 0.9, 1)
