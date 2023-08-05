import gym
from gym import spaces

import numpy as np
from dm_gym.rewards.ClusteringEnv_2_reward import Reward_Function
from sklearn.utils import shuffle
from copy import deepcopy

from dm_gym.env_conf import assign_env_config


class ClusteringEnv_2(gym.Env):

    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, *args, **kwargs):
        super(ClusteringEnv_2, self).__init__()

        assign_env_config(self, kwargs)

        self.current_step = 0

        self.total_data_size = len(self.data.index)

        try:
            self.max_steps
        except:
            self.max_steps = self.total_data_size

        self.R = Reward_Function()

        self.reward_range = (-1, 1)

        min_val = self.data.min().tolist()
        max_val = self.data.max().tolist()

        min_val = [x-1 for x in min_val]
        max_val = [x+1 for x in max_val]

        self.action_space = spaces.Discrete(self.k)

        self.observation_space = spaces.Box(low=np.array(
            min_val), high=np.array(max_val), dtype=np.float64)

        self.prototype_centroids = []
        for i in range(self.k):
            self.prototype_centroids.append(self.observation_space.sample())
        #self.prototype_centroids = self.data.sample(n=self.k).values.tolist()

        self.centroids = deepcopy(self.prototype_centroids)

    def reset(self):
        self.current_step = 0

        #self.centroids = deepcopy(self.prototype_centroids)

        self.data_env = deepcopy(self.data)
        self.data_env = shuffle(self.data_env)
        self.data_env.reset_index(inplace=True, drop=True)

        self.prev_obs = self.data_env.sample().values.tolist()[0]

        return self.prev_obs

    def _update_env(self, action, y_i, p_i):
        # Update Centroids
        self.centroids[action] = self.centroids[action] + \
            self.lr * abs(y_i - p_i) * (np.array(self.prev_obs) -
                                        np.array(self.centroids[action]))

    def step(self, action):

        action = int(action)
        self.current_step += 1

        if self.current_step >= self.max_steps:
            done = True
        else:
            done = False

        reward, y_i, p_i = self.R.reward_function(
            self.prev_obs, action, self.centroids)

        self._update_env(action, y_i, p_i)
        obs = self.data_env.sample().values.tolist()[0]

        self.prev_obs = obs

        return obs, reward, done, {'centroids': self.centroids}

    def render(self, mode='human', close=False):
        print('Step: ', self.current_step)
