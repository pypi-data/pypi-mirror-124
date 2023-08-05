import gym
from gym import spaces

import numpy as np
from dm_gym.rewards.ClassificationEnv_0_reward import Reward_Function
from sklearn.utils import shuffle
from copy import deepcopy

from dm_gym.env_conf import assign_env_config


class ClassificationEnv_0(gym.Env):

    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, *args, **kwargs):
        super(ClassificationEnv_0, self).__init__()

        assign_env_config(self, kwargs)
        self.current_step = 0

        self.total_data_size = len(self.data.index)

        self.R = Reward_Function()

        self.reward_range = (-1, 1)

        min_val = self.data.min().tolist()
        max_val = self.data.max().tolist()

        min_val = [x-1 for x in min_val]
        max_val = [x+1 for x in max_val]

        self.action_space = spaces.Discrete(self.num_classes)

        self.observation_space = spaces.Box(low=np.array(
            min_val), high=np.array(max_val), dtype=np.float64)

    def reset(self):
        self.current_step = 0

        self.data_env = deepcopy(self.data)
        self.target_env = deepcopy(self.target)

        self.data_env['target'] = self.target_env
        self.data_env = shuffle(self.data_env)
        self.data_env.reset_index(inplace=True, drop=True)

        self.target_env = self.data_env['target'].tolist()
        self.data_env = self.data_env.drop(columns=['target'])

        self.prev_obs = self.data_env.iloc[self.current_step].tolist()

        return self.prev_obs

    def step(self, action):

        action = int(action)
        expected_class = self.target_env[self.current_step]

        self.current_step += 1

        if self.current_step >= self.total_data_size - 1:
            done = True
        else:
            done = False

        reward = self.R.reward_function(action, expected_class)

        obs = self.data_env.iloc[self.current_step].tolist()
        self.prev_obs = obs

        return obs, reward, done, {"last timestep": (self.current_step-1), "action": action, "expected action": expected_class}

    def render(self, mode='human', close=False):
        print('Step: ', self.current_step)
