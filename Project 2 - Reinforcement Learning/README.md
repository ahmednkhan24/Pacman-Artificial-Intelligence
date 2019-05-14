# Reinforcement Learning

## Introduction
In this project, I implemented value iteration and Q-learning. I tested the agents first on Gridworld, then applied them to a simulated robot controller (Crawler) and Pacman.

This project includes an autograder for you to grade the answers on your machine. This can be run with the command:
* `python autograder.py`

It can be run for one particular question, such as q2, by:

* `python autograder.py -q q2`
It can be run for one particular test by commands of the form:

* `python autograder.py -t test_cases/q2/1-bridge-grid`

## Markov Decision Processes
To get started, run Gridworld in manual control mode, which uses the arrow keys:

* `python gridworld.py -m`
You will see a two-exit layout. The blue dot is the agent. Note that when you press up, the agent only actually moves north 80% of the time. Such is the life of a Gridworld agent!

You can control many aspects of the simulation. A full list of options is available by running:

* `python gridworld.py -h`
The default agent moves randomly

* `python gridworld.py -g MazeGrid`
You should see the random agent bounce around the grid until it happens upon an exit. Not the finest hour for an AI agent.

Note: The Gridworld MDP is such that you first must enter a pre-terminal state (the double boxes shown in the GUI) and then take the special 'exit' action before the episode actually ends (in the true terminal state called TERMINAL_STATE, which is not shown in the GUI). If you run an episode manually, your total return may be less than you expected, due to the discount rate (-d to change; 0.9 by default).

Look at the console output that accompanies the graphical output (or use -t for all text). You will be told about each transition the agent experiences (to turn this off, use -q).

As in Pacman, positions are represented by (x,y) Cartesian coordinates and any arrays are indexed by [x][y], with 'north' being the direction of increasing y, etc. By default, most transitions will receive a reward of zero, though you can change this with the living reward option (-r).

## Value Iteration
Wrote a value iteration agent in ValueIterationAgent in valueIterationAgents.py. The value iteration agent is an offline planner, not a reinforcement learning agent, and so the relevant training option is the number of iterations of value iteration it should run (option -i) in its initial planning phase. ValueIterationAgent takes an MDP on construction and runs value iteration for the specified number of iterations before the constructor returns.

Value iteration computes k-step estimates of the optimal values, Vk. In addition to running value iteration, implement the following methods for ValueIterationAgent using Vk.

computeActionFromValues(state) computes the best action according to the value function given by self.values.
computeQValueFromValues(state, action) returns the Q-value of the (state, action) pair given by the value function given by self.values.
These quantities are all displayed in the GUI: values are numbers in squares, Q-values are numbers in square quarters, and policies are arrows out from each square.

Important: Use the "batch" version of value iteration where each vector Vk is computed from a fixed vector Vk-1 (like in lecture), not the "online" version where one single weight vector is updated in place. This means that when a state's value is updated in iteration k based on the values of its successor states, the successor state values used in the value update computation should be those from iteration k-1 (even if some of the successor states had already been updated in iteration k). The difference is discussed in Sutton & Barto in the 6th paragraph of chapter 4.1.

Note: A policy synthesized from values of depth k (which reflect the next k rewards) will actually reflect the next k+1 rewards (i.e. you return πk+1). Similarly, the Q-values will also reflect one more reward than the values (i.e. you return Qk+1).

We return the synthesized policy πk+1.

Used the util.Counter class in util.py, which is a dictionary with a default value of zero. Methods such as totalCount simplify the code. However, be careful with argMax: the actual argmax you want may be a key not in the counter!

Handle the case when a state has no available actions in an MDP.

To test the implementation, run the autograder:

* `python autograder.py -q q1`
The following command loads the ValueIterationAgent, which will compute a policy and execute it 10 times. Press a key to cycle through values, Q-values, and the simulation. You should find that the value of the start state (V(start), which you can read off of the GUI) and the empirical resulting average reward (printed after the 10 rounds of execution finish) are quite close.

* `python gridworld.py -a value -i 100 -k 10`

## Bridge Crossing Analysis
BridgeGrid is a grid world map with the a low-reward terminal state and a high-reward terminal state separated by a narrow "bridge", on either side of which is a chasm of high negative reward. The agent starts near the low-reward state. With the default discount of 0.9 and the default noise of 0.2, the optimal policy does not cross the bridge. Changed only ONE of the discount and noise parameters so that the optimal policy causes the agent to attempt to cross the bridge. Answer is in question2() of analysis.py. (Noise refers to how often an agent ends up in an unintended successor state when they perform an action.)

* `python gridworld.py -a value -i 100 -g BridgeGrid --discount 0.9 --noise 0.2`
* `python autograder.py -q q2`

## Policies
Consider the DiscountGrid layout. This grid has two terminal states with positive payoff (in the middle row), a close exit with payoff +1 and a distant exit with payoff +10. The bottom row of the grid consists of terminal states with negative payoff; each state in this "cliff" region has payoff -10. We distinguish between two types of paths: 
* (1) paths that "risk the cliff" and travel near the bottom row of the grid; these paths are shorter but risk earning a large negative payoff.
* (2) paths that "avoid the cliff" and travel along the top edge of the grid. These paths are longer but are less likely to incur huge negative payoffs.

We chose settings of the discount, noise, and living reward parameters for this MDP to produce optimal policies of several different types. The setting of the parameter values for each part have the property that, if the agent followed its optimal policy without being subject to any noise, it would exhibit the given behavior. If a particular behavior is not achieved for any setting of the parameters, we asserted that the policy is impossible by returning the string 'NOT POSSIBLE'.

Here are the optimal policy types we produced:

Prefer the close exit (+1), risking the cliff (-10)
Prefer the close exit (+1), but avoiding the cliff (-10)
Prefer the distant exit (+10), risking the cliff (-10)
Prefer the distant exit (+10), avoiding the cliff (-10)
Avoid both exits and the cliff (so an episode should never terminate)
To check your answers, run the autograder:

* `python autograder.py -q q3`
question3a() through question3e() should each return a 3-item tuple of (discount, noise, living reward) in analysis.py.

You can check the policies in the GUI. For example, using a correct answer to 3(a), the arrow in (0,1) should point east, the arrow in (1,1) should also point east, and the arrow in (2,1) should point north.

Note: On some machines you may not see an arrow. In this case, press a button on the keyboard to switch to qValue display, and mentally calculate the policy by taking the arg max of the available qValues for each state.

## Q-Learning
Note that the value iteration agent does not actually learn from experience. Rather, it ponders its MDP model to arrive at a complete policy before ever interacting with a real environment. When it does interact with the environment, it simply follows the precomputed policy (e.g. it becomes a reflex agent). This distinction may be subtle in a simulated environment like a Gridword, but it's very important in the real world, where the real MDP is not available.

We wrote a Q-learning agent, which does very little on construction, but instead learns by trial and error from interactions with the environment through its update(state, action, nextState, reward) method. 

Note: For computeActionFromQValues, we break ties randomly for better behavior. The random.choice() function helped. In a particular state, actions that the agent hasn't seen before still have a Q-value, specifically a Q-value of zero, and if all of the actions that the agent has seen before have a negative Q-value, an unseen action may be optimal.

Important: Made sure that in the computeValueFromQValues and computeActionFromQValues functions, we only access Q values by calling getQValue. This abstraction will be useful for question 8 when we override getQValue to use features of state-action pairs rather than state-action pairs directly.

* `python gridworld.py -a q -k 5 -m`
Recall that -k will control the number of episodes the agent gets to learn. Watch how the agent learns about the state it was just in, not the one it moves to, and "leaves learning in its wake." Hint: to help with debugging, you can turn off noise by using the --noise 0.0 parameter (though this obviously makes Q-learning less interesting). 

## Epsilon Greedy
Completed the Q-learning agent by implementing epsilon-greedy action selection in getAction, meaning it chooses random actions an epsilon fraction of the time, and follows its current best Q-values otherwise. Note that choosing a random action may result in choosing the best action - that is, we should not choose a random sub-optimal action, but rather any random legal action.

* `python gridworld.py -a q -k 100`
The final Q-values should resemble those of the value iteration agent, especially along well-traveled paths. However, the average returns will be lower than the Q-values predict because of the random actions and the initial learning phase.

You can choose an element from a list uniformly at random by calling the random.choice function. You can simulate a binary variable with probability p of success by using util.flipCoin(p), which returns True with probability p and False with probability 1-p.

To test the implementation, run the autograder:

* `python autograder.py -q q5`
With no additional code, we should now be able to run a Q-learning crawler robot:

* `python crawler.py`

This will invoke the crawling robot using the Q-learner. Note that the step delay is a parameter of the simulation, whereas the learning rate and epsilon are parameters of the learning algorithm, and the discount factor is a property of the environment.

## Bridge Crossing Revisited
First, trained a completely random Q-learner with the default learning rate on the noiseless BridgeGrid for 50 episodes and observe whether it finds the optimal policy.

* `python gridworld.py -a q -k 50 -n 0 -g BridgeGrid -e 1`
Then tried the same experiment with an epsilon of 0. Is there an epsilon and a learning rate for which it is highly likely (greater than 99%) that the optimal policy will be learned after 50 iterations? question6() in analysis.py should return EITHER a 2-item tuple of (epsilon, learning rate) OR the string 'NOT POSSIBLE' if there is none. Epsilon is controlled by -e, learning rate by -l.

Note: The response should be not depend on the exact tie-breaking mechanism used to choose actions. This means the answer should be correct even if for instance we rotated the entire bridge grid world 90 degrees.

* `python autograder.py -q q6`

## Q-Learning and Pacman
Time to play some Pacman! Pacman will play games in two phases. In the first phase, training, Pacman will begin to learn about the values of positions and actions. Because it takes a very long time to learn accurate Q-values even for tiny grids, Pacman's training games run in quiet mode by default, with no GUI (or console) display. Once Pacman's training is complete, he will enter testing mode. When testing, Pacman's self.epsilon and self.alpha will be set to 0.0, effectively stopping Q-learning and disabling exploration, in order to allow Pacman to exploit his learned policy. Test games are shown in the GUI by default. Without any code changes you should be able to run Q-learning Pacman for very tiny grids as follows:

* `python pacman.py -p PacmanQAgent -x 2000 -n 2010 -l smallGrid`
PacmanQAgent is only different in that it has default learning parameters that are more effective for the Pacman problem (epsilon=0.05, alpha=0.2, gamma=0.8). The command above works without exceptions and the agent wins at least 80% of the time. The autograder will run 100 test games after the 2000 training games.


* `python autograder.py -q q7`
Note: If you want to experiment with learning parameters, you can use the option -a, for example -a epsilon=0.1,alpha=0.3,gamma=0.7. These values will then be accessible as self.epsilon, self.gamma and self.alpha inside the agent.

Note: While a total of 2010 games will be played, the first 2000 games will not be displayed because of the option -x 2000, which designates the first 2000 games for training (no output). Thus, you will only see Pacman play the last 10 of these games. The number of training games is also passed to the agent as the option numTraining.

Note: If you want to watch 10 training games to see what's going on, use the command:

* `python pacman.py -p PacmanQAgent -n 10 -l smallGrid -a numTraining=10`
During training, you will see output every 100 games with statistics about how Pacman is faring. Epsilon is positive during training, so Pacman will play poorly even after having learned a good policy: this is because he occasionally makes a random exploratory move into a ghost. As a benchmark, it should take between 1,000 and 1400 games before Pacman's rewards for a 100 episode segment becomes positive, reflecting that he's started winning more than losing. By the end of training, it should remain positive and be fairly high (between 100 and 350).

The MDP state is the exact board configuration facing Pacman, with the now complex transitions describing an entire ply of change to that state. The intermediate game configurations in which Pacman has moved but the ghosts have not replied are not MDP states, but are bundled in to the transitions.

Once Pacman is done training, he should win very reliably in test games (at least 90% of the time), since now he is exploiting his learned policy.

However, you will find that training the same agent on the seemingly simple mediumGrid does not work well. In our implementation, Pacman's average training rewards remain negative throughout training. At test time, he plays badly, probably losing all of his test games. Training will also take a long time, despite its ineffectiveness.

Pacman fails to win on larger layouts because each board configuration is a separate state with separate Q-values. He has no way to generalize that running into a ghost is bad for all positions. Obviously, this approach will not scale.

## Approximate Q-Learning
Implemented an approximate Q-learning agent that learns weights for features of states, where many states might share the same features. Wrote our implementation in ApproximateQAgent class in qlearningAgents.py, which is a subclass of PacmanQAgent.

Note: Approximate Q-learning assumes the existence of a feature function f(s,a) over state and action pairs, which yields a vector f1(s,a) .. fi(s,a) .. fn(s,a) of feature values. Feature vectors are util.Counter (like a dictionary) objects containing the non-zero pairs of features and values; all omitted features have value zero.

The approximate Q-function takes the following form

Q(s,a)=∑i=1nfi(s,a)wi

where each weight wi is associated with a particular feature fi(s,a). In the code, we implemented the weight vector as a dictionary mapping features (which the feature extractors will return) to weight values. We update our weight vectors similarly to how we updated Q-values:

wi←wi+α⋅difference⋅fi(s,a)
difference=(r+γmaxa′Q(s′,a′))−Q(s,a)

Note that the difference term is the same as in normal Q-learning, and r is the experienced reward.

By default, ApproximateQAgent uses the IdentityExtractor, which assigns a single feature to every (state,action) pair. With this feature extractor, the approximate Q-learning agent should work identically to PacmanQAgent. You can test this with the following command:

* `python pacman.py -p ApproximateQAgent -x 2000 -n 2010 -l smallGrid`
Important:ApproximateQAgent is a subclass of QLearningAgent, and it therefore shares several methods like getAction. Made sure that our methods in QLearningAgent call getQValue instead of accessing Q-values directly, so that when we override getQValue in our approximate agent, the new approximate q-values are used to compute actions.

Run the approximate Q-learning agent with the custom feature extractor, which can learn to win with ease:

* `python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumGrid`
Even much larger layouts should be no problem for the ApproximateQAgent. (warning: this may take a few minutes to train)

* `python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumClassic`
The approximate Q-learning agent should win almost every time with these simple features, even with only 50 training games.

* `python autograder.py -q q8`

This project was completed with a partner, Joshua Herman (joshua9663)

[Link to official project description](http://ai.berkeley.edu/reinforcement.html)
