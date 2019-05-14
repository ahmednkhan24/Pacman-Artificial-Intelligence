# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        # initialize values to be an empty dictionary
        all_values = util.Counter()

        # iterate the amount of times specified
        for i in range(self.iterations):

            all_states = self.mdp.getStates()

            # calculate the overall q values for each possible state
            for state in all_states:

                # array to hold the q values for each possible action in this state
                values = []

                if self.mdp.isTerminal(state):
                    values.append(0)
                else:
                    all_actions = self.mdp.getPossibleActions(state)

                    # calculate and save the q value for each possible action
                    for action in all_actions:
                        q_val = self.computeQValueFromValues(state, action)
                        values.append(q_val)

                # save the maximum possible q value from this state
                all_values[state] = max(values)

            self.values = all_values.copy()

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"

        # grab the possible transition states and the probabilities
        trans_states_probs = self.mdp.getTransitionStatesAndProbs(state, action)

        # total to keep track of the overall total per state
        total = 0

        # loop through each transition state
        for trans in trans_states_probs:

            # trans[0] = next state
            # trans[1] = probability

            next_state = trans[0]
            probability = trans[1]

            # calculate the overall reward for going to this next state
            gross_reward = self.mdp.getReward(state, action, next_state)

            # factor in the discount and previous values to obtain the net expected reward
            net_reward = probability * (gross_reward + self.discount * self.values[next_state])

            # add to the total
            total = total + net_reward

        return total

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        # check for terminal state
        if self.mdp.isTerminal(state):
            return None

        # get the possible actions from the current state
        poss_actions = self.mdp.getPossibleActions(state)

        # dictionary to keep track of the q values of each action
        actions_q_vals = util.Counter()

        for action in poss_actions:

            # calculate the q value of this action
            q_val = self.computeQValueFromValues(state, action)

            # save the value in our dictionary
            actions_q_vals[action] = q_val

        # return the action that generated the largest q value
        return actions_q_vals.argMax()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
