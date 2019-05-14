# Search

## Introduction
In this project, my Pacman agent will find paths through his maze world, both to reach a particular location and to collect food efficiently. I built general search algorithms and applied them to Pacman scenarios.

This project includes an autograder for you to grade the answers on your machine. This can be run with the command:
* `python autograder.py`

## Welcome to Pacman
After downloading the code, unzipping it, and changing to the directory, you should be able to play a game of Pacman by typing the following at the command line:

python pacman.py
Pacman lives in a shiny blue world of twisting corridors and tasty round treats. Navigating this world efficiently will be Pacman's first step in mastering his domain.

The simplest agent in searchAgents.py is called the GoWestAgent, which always goes West (a trivial reflex agent). This agent can occasionally win:

* `python pacman.py --layout testMaze --pacman GoWestAgent`
But, things get ugly for this agent when turning is required:

* `python pacman.py --layout tinyMaze --pacman GoWestAgent`
If Pacman gets stuck, you can exit the game by typing CTRL-c into your terminal.

The agent will solve not only tinyMaze, but any maze you want.

Note that pacman.py supports a number of options that can each be expressed in a long way (e.g., --layout) or a short way (e.g., -l). You can see the list of all options and their default values via:

* `python pacman.py -h`
Also, all of the commands that appear in this project also appear in commands.txt, for easy copying and pasting. In UNIX/Mac OS X, you can even run all these commands in order with bash commands.txt.

## Finding a Fixed Food Dot using Depth First Search
In searchAgents.py, you'll find a fully implemented SearchAgent, which plans out a path through Pacman's world and then executes that path step-by-step.

* `python pacman.py -l tinyMaze -p SearchAgent -a fn=tinyMazeSearch`
The command above tells the SearchAgent to use tinyMazeSearch as its search algorithm, which is implemented in search.py. Pacman should navigate the maze successfully.

Important note: All of the search functions need to return a list of actions that will lead the agent from the start to the goal. These actions all have to be legal moves (valid directions, no moving through walls).

Important note: Used the Stack, Queue and PriorityQueue data structures provided in util.py! These data structure implementations have particular properties which are required for compatibility with the autograder.

Implemented the depth-first search (DFS) algorithm in the depthFirstSearch function in search.py. Wrote the graph search version of DFS, which avoids expanding any already visited states, to make the algorithm complete.

The code should quickly find a solution for:

* `python pacman.py -l tinyMaze -p SearchAgent`
* `python pacman.py -l mediumMaze -p SearchAgent`
* `python pacman.py -l bigMaze -z .5 -p SearchAgent`
The Pacman board will show an overlay of the states explored, and the order in which they were explored (brighter red means earlier exploration).I

Hint: If you use a Stack as your data structure, the solution found by your DFS algorithm for mediumMaze should have a length of 130 (provided you push successors onto the fringe in the order provided by getSuccessors; you might get 246 if you push them in the reverse order).

## Breadth First Search
Implemented the breadth-first search (BFS) algorithm in the breadthFirstSearch function in search.py. Again, wrote a graph search algorithm that avoids expanding any already visited states. Test the code the same way you did for depth-first search.

* `python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs`
* `python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5`

## Varying the Cost Function
While BFS will find a fewest-actions path to the goal, we might want to find paths that are "best" in other senses. Consider mediumDottedMaze and mediumScaryMaze.

By changing the cost function, we can encourage Pacman to find different paths. For example, we can charge more for dangerous steps in ghost-ridden areas or less for steps in food-rich areas, and a rational Pacman agent should adjust its behavior in response.

Implemented the uniform-cost graph search algorithm in the uniformCostSearch function in search.py. You should now observe successful behavior in all three of the following layouts, where the agents below are all UCS agents that differ only in the cost function they use.

* `python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs`
* `python pacman.py -l mediumDottedMaze -p StayEastSearchAgent`
* `python pacman.py -l mediumScaryMaze -p StayWestSearchAgent`
Note: You should get very low and very high path costs for the StayEastSearchAgent and StayWestSearchAgent respectively, due to their exponential cost functions (see searchAgents.py for details).

## A* search
Implemented A* graph search in the function aStarSearch in search.py. A* takes a heuristic function as an argument. Heuristics take two arguments: a state in the search problem (the main argument), and the problem itself (for reference information). The nullHeuristic heuristic function in search.py is a trivial example.

You can test your A* implementation on the original problem of finding a path through a maze to a fixed position using the Manhattan distance heuristic (implemented already as manhattanHeuristic in searchAgents.py).

* `python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic`
You should see that A* finds the optimal solution slightly faster than uniform cost search (about 549 vs. 620 search nodes expanded in our implementation, but ties in priority may make your numbers differ slightly).

## Eating All The Dots
Now we'll solve a hard search problem: eating all the Pacman food in as few steps as possible. For this, we'll need a new search problem definition which formalizes the food-clearing problem: FoodSearchProblem in searchAgents.py. A solution is defined to be a path that collects all of the food in the Pacman world. For the present project, solutions do not take into account any ghosts or power pellets; solutions only depend on the placement of walls, regular food and Pacman. (Of course ghosts can ruin the execution of a solution! We have written the general search methods correctly, so A* with a null heuristic (equivalent to uniform-cost search) should quickly find an optimal solution to testSearch with no code change on your part (total cost of 7).

* `python pacman.py -l testSearch -p AStarFoodSearchAgent`
Note: AStarFoodSearchAgent is a shortcut for `-p SearchAgent -a fn=astar,prob=FoodSearchProblem,heuristic=foodHeuristic`.

You should find that UCS starts to slow down even for the seemingly simple tinySearch. As a reference, our implementation takes 2.5 seconds to find a path of length 27 after expanding 5057 search nodes.

Filled in foodHeuristic in searchAgents.py with a consistent heuristic for the FoodSearchProblem. Try the agent on the trickySearch board:

* `python pacman.py -l trickySearch -p AStarFoodSearchAgent`
Our UCS agent finds the optimal solution in about 13 seconds, exploring over 16,000 nodes.

Any non-trivial non-negative consistent heuristic will receive 1 point. Made sure that the heuristic returns 0 at every goal state and never returns a negative value.

## Suboptimal Search
Sometimes, even with A* and a good heuristic, finding the optimal path through all the dots is hard. In these cases, we'd still like to find a reasonably good path, quickly. I write an agent that always greedily eats the closest dot.

Implemented the function findPathToClosestDot in searchAgents.py. Our agent solves this maze (suboptimally!) in under a second with a path cost of 350:

* `python pacman.py -l bigSearch -p ClosestDotSearchAgent -z .5`

The ClosestDotSearchAgent won't always find the shortest possible path through the maze.

[Link to official project description](http://ai.berkeley.edu/search.html)
