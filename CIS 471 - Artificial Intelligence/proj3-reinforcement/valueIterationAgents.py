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
import collections

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
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for _ in range(self.iterations):
            counter = util.Counter()

            for state in self.mdp.getStates():  

                if not self.mdp.isTerminal(state):
                    max_val = float("-inf")

                    for action in self.mdp.getPossibleActions(state):
                        q_val = self.getQValue(state, action)
                        max_val = max([max_val, q_val])

                    counter[state] = max_val # vk+1

            self.values = counter

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
        value = 0
        for new_state, probability in self.mdp.getTransitionStatesAndProbs(state, action):
            reward = self.mdp.getReward(state, action, new_state) 
            value += probability * (reward + (self.discount * self.values[new_state]))
        
        return value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        max_act = None
        max_val = float("-inf")

        for action in self.mdp.getPossibleActions(state):
            q_val = self.getQValue(state, action)
                        
            if q_val > max_val:
                max_act = action
                max_val = q_val

        return max_act

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()

        for i in range(self.iterations):
            index = i % len(states)
            cur_state = states[index]

            if self.mdp.isTerminal(cur_state):
                continue

            max_val = max([self.computeQValueFromValues(cur_state, action) for action in self.mdp.getPossibleActions(cur_state)])
            self.values[cur_state] = max_val

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def getPredecessors(self):
        # Compute predecessors of all states
        predecessors = {}

        for s in self.mdp.getStates():
            if not self.mdp.isTerminal(s):
                for action in self.mdp.getPossibleActions(s):
                    for new_state, _ in self.mdp.getTransitionStatesAndProbs(s, action):

                        if new_state in predecessors:
                            predecessors[new_state].add(s)
                        else:
                            predecessors[new_state] = {s}

        return predecessors

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        pq = util.PriorityQueue()
        predecessors = self.getPredecessors()
        
        for s in self.mdp.getStates():
            if not self.mdp.isTerminal(s):
                max_val = max([self.computeQValueFromValues(s, action) for action in self.mdp.getPossibleActions(s)])
                diff = abs(max_val - self.values[s])
                pq.update(s, - diff)    # prioritize updating states that have a higher error

        for _ in range(self.iterations):
            if pq.isEmpty():    # terminate
                break

            s = pq.pop()

            # Update s's value (if it is not a terminal state)
            if not self.mdp.isTerminal(s):
                max_val = max([self.computeQValueFromValues(s, action) for action in self.mdp.getPossibleActions(s)])
                self.values[s] = max_val

            for p in predecessors[s]:
                if not self.mdp.isTerminal(p):
                    # Find the absolute value of the difference between the current value 
                    # of p in self.values and the highest Q-value across all possible actions from p
                    max_val = max([self.computeQValueFromValues(p, action) for action in self.mdp.getPossibleActions(p)])
                    diff = abs(max_val - self.values[p])
                    if diff > self.theta:
                        pq.update(p, -diff)

