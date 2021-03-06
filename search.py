# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    closedSet = set()
    
    #Stack for processing nodes
    fringe = util.Stack()
        
    #start state
    start = problem.getStartState()
  
    #push first node onto the stack
    fringe.push(start)
    
    #path to goal
    path, finalPath = [], []
    
    #dictionary of expanded states
    expanded = {}
    
    #dfs algorithm
    while not(fringe.isEmpty()): 
        currState = fringe.pop()
                    
        if currState == start:
            currState = (currState, None, None )
        
        state = currState[0]
        
        if state != start:
            path.append(currState)
            
        closedSet.add(state)
        
        if problem.isGoalState(state):
            for elem in path:
                finalPath.append(elem[1])
            break
                     
        successors = problem.getSuccessors(state)
        expanded[state] = successors  
        successorAdded = False     
    
        for s in successors:     
            if s[0] not in closedSet:
                fringe.push(s)
                successorAdded = True    
        
        if not successorAdded:
            while(True):
                donePopping = False
                try:
                    poppedState = path.pop()
                except IndexError:
                    break
                sList = expanded.get(poppedState[0])
                for s in sList:
                    if s[0] not in closedSet:
                        donePopping = True
                        path.append(poppedState)
                        break
                if donePopping:
                    break          
    return finalPath

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    closedSet = set()
    
    #Queue for processing nodes
    fringe = util.Queue()
        
    #start state
    start = problem.getStartState()
  
    #push first node onto the queue with a list how to get to that node
    fringe.push((start, []))
    
    #path to goal
    finalPath = []
        
    #bfs algorithm
    while not(fringe.isEmpty()):
        data = fringe.pop()
        currState = data[0]
                    
        if currState == start:
            currState = (currState, None, None )
        
        state = currState[0]
            
        if problem.isGoalState(state):
            finalPath = data[1]
            break
        
        if state not in closedSet:             
            successors = problem.getSuccessors(state)  
            closedSet.add(state) 
    
            for s in successors:     
                nextAction = s[1]
                fringe.push((s, data[1] + [nextAction]))           
    return finalPath

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    closedSet = set()
    
    #Priority queue for processing nodes
    fringe = util.PriorityQueue()
        
    #start state
    start = problem.getStartState()
  
    #push first node onto the queue with a list how to get to that node
    totalCost, priority = 0, 0
    startTuple = (start, None, 0)
    fringe.push((startTuple, [], totalCost) , priority)
    
    #path to goal
    finalPath = []
    
    #ucs algorithm
    while not(fringe.isEmpty()):
        data = fringe.pop()    
        state = data[0][0]
        path = data[1]
            
        if problem.isGoalState(state):
            finalPath = path
            break
        
        if state not in closedSet:             
            successors = problem.getSuccessors(state) 
            closedSet.add(state) 
        
            for s in successors: 
                nextAction = s[1]
                actionList = path + [nextAction]
                priorityAndCost = data[2] + s[2]
                fringe.push((s, actionList, priorityAndCost), priorityAndCost)           
    return finalPath

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    closedSet = set()
    
    #Priority queue for processing nodes
    fringe = util.PriorityQueue()
        
    #start state
    start = problem.getStartState()
  
    #push first node onto the queue with a list how to get to that node
    totalCost = priority = 0
    startTuple = (start, None, 0)
    fringe.push((startTuple, [], totalCost) , priority + heuristic(start, problem))
    
    #astar algorithm
    while not(fringe.isEmpty()):
        data = fringe.pop()    
        state = data[0][0]
        path = data[1]
            
        if problem.isGoalState(state):
            break
        
        if state not in closedSet:             
            successors = problem.getSuccessors(state)
            closedSet.add(state) 
    
            for s in successors: 
                position = s[0]
                nextAction = s[1]
                actionList = path + [nextAction]
                priorityAndCost = data[2] + s[2]
                fringe.push((s, actionList, priorityAndCost), priorityAndCost + heuristic(position, problem))         
    return path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
