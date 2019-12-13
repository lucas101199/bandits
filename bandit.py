# epsilon-greedy example implementation of a multi-armed bandit
import random

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import simulator
import reference_bandit

# generic epsilon-greedy bandit
class Bandit:
    def __init__(self, arms, epsilon=0.1):
        self.arms = arms
        self.armsDiscarded = {}
        self.epsilon = epsilon
        self.frequencies = [0] * len(arms)
        self.sums = [0] * len(arms)
        self.expected_values = [0] * len(arms)

    def run(self):
        for i in range(6):
            self.armsDiscarded[self.arms[i]] = self.sums[i]

        {k: v for k, v in sorted(self.armsDiscarded.items(), key=lambda item: item[1])}
        #self.armsSorted = sorted(self.sums)
        #for i in range(4):
        #    self.armsDiscarded[i] = self.armsSorted[i]
        if min(self.frequencies) == 0:
            return self.arms[self.frequencies.index(min(self.frequencies))]
        if random.random() < self.epsilon: 
            return self.armsDiscarded[random.randint(2, len(arms) - 1)]
        return self.arms[self.expected_values.index(max(self.expected_values))]

    def give_feedback(self, arm, reward):
        arm_index = self.arms.index(arm)
        sum = self.sums[arm_index] + reward
        self.sums[arm_index] = sum
        frequency = self.frequencies[arm_index] + 1
        self.frequencies[arm_index] = frequency
        expected_value = sum / frequency
        self.expected_values[arm_index] = expected_value

# configuration
arms = [
    'Configuration a',
    'Configuration b',
    'Configuration c',
    'Configuration d',
    'Configuration e',
    'Configuration f'
]

# instantiate bandits
bandit = Bandit(arms)
ref_bandit = reference_bandit.ReferenceBandit(arms)

