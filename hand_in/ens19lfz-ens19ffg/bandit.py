# epsilon-greedy example implementation of a multi-armed bandit
import random

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import simulator
import reference_bandit

from collections import OrderedDict

# generic epsilon-greedy bandit
class Bandit:
    def __init__(self, arms, epsilon=0.5):
        self.arms = arms
        self.armsDiscarded = [0] * 6
        self.epsilon = epsilon
        self.frequencies = [0] * len(arms)
        self.sums = [0] * len(arms)
        self.expected_values = [0] * len(arms)
        self.armed = [0] * 4
        self.last_expected = [0] * len(arms)
        self.last_arm = 'Configuration a'
        self.past_rewards = [[0 for i in range(10)] for j in range(6)]
        self.counter = [0] * 6
        self.rewards = [0] * 6
        self.oldrewards = [0] * 6


    def run(self):
        index = self.arms.index(self.last_arm)
        #print(abs(self.oldrewards[index]-self.rewards[index]))
        #if (abs(self.oldrewards[index]-self.rewards[index]) > 1.7):
            #self.epsilon = 0.6
        if (self.epsilon < 0.049996802):
            self.epsilon = 0.5
        self.epsilon = self.epsilon * 0.9977
        self.oldrewards[index] = self.rewards[index]


        if min(self.frequencies) <= 9:
            self.last_arm = self.arms[self.frequencies.index(min(self.frequencies))]
            return self.arms[self.frequencies.index(min(self.frequencies))]
        
        
        
        summed_rewards = [0] * 6
        self.counter[index] += 1
        self.past_rewards[index][(self.counter[index] - 1) % 10] = self.rewards[index]
        for i in range(6):
            for j in range(10):
                summed_rewards[i] += self.past_rewards[i][j]
            self.armsDiscarded[i] = summed_rewards[i] / 10

        sorted_arms = sorted(self.armsDiscarded, reverse=True)

        if random.random() < self.epsilon: 
            rand = random.randint(0, len(arms) - 3)
            
            self.last_arm = self.arms[self.armsDiscarded.index(sorted_arms[rand])]
            
            #print(self.arms[rand])
            return self.arms[self.armsDiscarded.index(sorted_arms[rand])]
        self.last_arm = self.arms[self.expected_values.index(max(self.expected_values))]
        #print(self.arms[self.expected_values.index(max(self.expected_values))])
        return self.arms[self.expected_values.index(max(self.expected_values))]

    def give_feedback(self, arm, reward):
        
        arm_index = self.arms.index(arm)
        self.rewards[arm_index] = reward
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

