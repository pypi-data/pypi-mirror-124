import numpy as np

class Reward_Function:

    def __init__(self):
        pass

    def reward_function(self, action, expected_class):
        reward = 0

        if(action == expected_class):
            reward = 1
        else:
            reward = -1

        return reward

