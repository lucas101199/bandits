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
        self.armed = [0] * 4
        self.last_expected = [0] * len(arms)
        self.last_arm = 'Configuration a'
        self.init = True

    def run(self):
        if self.init:
            for i in range(6):
                self.armsDiscarded[self.arms[i]] = 0
                self.init = False

        self.last_expected = self.expected_values
        index = self.arms.index(self.last_arm)
        self.armsDiscarded[self.last_arm] = self.last_expected[index] - self.expected_values[index]


        if min(self.frequencies) == 0:
            self.last_arm = self.arms[self.frequencies.index(min(self.frequencies))]
            return self.arms[self.frequencies.index(min(self.frequencies))]

        
        
        {k: v for k, v in sorted(self.armsDiscarded.items(), key=lambda item: item[1])}
        
        for i in range(4):
            self.armed = list(self.armsDiscarded.keys())[i+2]
        #print(self.armed)
        if random.random() < self.epsilon: 
            rand = random.randint(0, len(arms) - 3)
            self.last_arm = self.arms[rand]
            #print(self.arms[rand])
            return self.arms[rand]
        self.last_arm = self.arms[self.expected_values.index(max(self.expected_values))]
        #print(self.arms[self.expected_values.index(max(self.expected_values))])
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

