# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def dfs_bfs(problem, data_structure):
    visited_set = set()

    # grab the start node
    # nodes are tuples of (x, y)
    start_node = problem.getStartState()

    # insert tuple of start node and an array containing the path it took to get there
    # the path array will be a list of directions
    # ex: ['North', 'West', 'East', 'South']
    node_tuple = (start_node, [])
    data_structure.push(node_tuple)

    # begin algorithm, continue as long as there is a node in the data structure
    while not data_structure.isEmpty():
        # grab the node and the path it took to get there from the top of the stack
        popped_tuple = data_structure.pop()
        node = popped_tuple[0]
        path = popped_tuple[1]

        # check if the node has been visited yet
        if node in visited_set:
            # skip this iteration of the loop
            continue

        # check if we've reached the end node
        if problem.isGoalState(node):
            # success, return the path it took to get here
            return path

        # mark the current node as visited
        visited_set.add(node)

        # grab the all neighbors for the current node
        neighbors = problem.getSuccessors(node)
        for neighbor in neighbors:
            # a node is in the format ((x, y), 'Direction', Cost)
            next_node = neighbor[0]
            direction = neighbor[1]

            # check if the next node has not been visited yet
            if next_node not in visited_set:
                # add the next node to the data structure plus the path it took to get to it
                next_node_tuple = (next_node, path + [direction])
                data_structure.push(next_node_tuple)


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    # DFS uses a stack
    return dfs_bfs(problem, util.Stack())


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    # BFS uses a queue
    return dfs_bfs(problem, util.Queue())


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    # initialize data structures
    priority_queue = util.PriorityQueue()
    visited_set = set()

    # dictionary to keep track of the highest priority/lowest cost of each node
    weights = {}

    # grab the start node
    # nodes are tuples of (x, y)
    start_node = problem.getStartState()

    # give the first node a weight of 0
    weights[start_node] = 0

    # create tuple of start node and an array containing the path it took to get there
    # the path array will be a list of directions
    # ex: ['North', 'West', 'East', 'South']
    node_tuple = (start_node, [])

    # push the tuple and initial weight of 0 into the priority queue
    priority_queue.push(node_tuple, 0)

    # begin algorithm, continue as long as there is a node in the priority queue
    while not priority_queue.isEmpty():
        popped_tuple = priority_queue.pop()
        node = popped_tuple[0]
        path = popped_tuple[1]

        # check if the node has been visited yet
        if node in visited_set:
            # skip this iteration of the loop
            continue

        # check if we've reached the end node
        if problem.isGoalState(node):
            # success, return the path it took to get here
            return path

        # mark the current node as visited, and grab the weight associated to it
        visited_set.add(node)
        cost = weights[node]

        # grab the all neighbors for the current node
        neighbors = problem.getSuccessors(node)
        for neighbor in neighbors:
            # a node is in the format ((x, y), 'Direction', Cost)
            next_node = neighbor[0]
            direction = neighbor[1]
            next_cost = neighbor[2]

            # create a tuple for the next node containing the node and the path it took to get to it
            next_node_tuple = (next_node, path + [direction])

            # check if the next node's weight has been previously calculated
            if next_node in weights:
                # check if this new cost for next node is better than the previously calculated one
                if weights[next_node] <= cost + next_cost:
                    continue
                else:
                    priority_queue.update(next_node_tuple, cost + next_cost)
            else:
                priority_queue.push(next_node_tuple, cost + next_cost)

            # update the weight of the next node in the dictionary if we got to this point
            weights[next_node] = cost + next_cost


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "* YOUR CODE HERE *"
    # open set
    openSet = util.PriorityQueue()

    # closed set
    closedSet = set()

    # insert initial node with lowest cost in openSet aka "fringe"
    openSet.push((problem.getStartState(), [], 0), heuristic(problem.getStartState(), problem))

    # loop until the openSet is empty (failure) or we reach the goal state and return the path
    while not (openSet.isEmpty()):
        # get the node, path, and heuristic cost of the current highest priority element in the PQ and pop it off
        node, path, cost = openSet.pop()

        # if we find the goal state pop it off and return the path to the goal state
        if (problem.isGoalState(node)):
            return path

        # if not node is not currently in our closedSet then add it to the closedSet, find the successors, and push the successor to the openSet
        if node not in closedSet:
            closedSet.add(node)
            for next in problem.getSuccessors(node):
                # same thing as node, path, and cost from above just for the successor state
                state, direction, price = next
                nextPath = path + [direction]  # get the next path which is the current path + the successor path
                nextPrice = cost + price  # get the next cost which is the current cost + successor cost
                openSet.push((state, nextPath, nextPrice),
                             heuristic(state, problem) + nextPrice)  # push the successor into the openSet
    # if we get here then the openSet is empty failure return 0
    if openSet.isEmpty():
        return 0


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
