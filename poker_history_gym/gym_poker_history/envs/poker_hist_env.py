#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simulate the simplified poker hand history environment.

Each episode is selling a hand from one player's perspective.
"""


# 3rd party modules
import gym
import numpy as np
import pandas as pd
from gym import spaces
from pymongo import MongoClient
from transform_hands_for_gym import run_iteration

class PokerHistEnv(gym.Env):
    """
    Extending gym environment to show the model hands.

    The environment defines which actions can be taken at which point and
    when the agent receives which reward.
    """

    def __init__(self):
        self.__version__ = "0.1.0"
        print("PokerHistEnv - Version {}".format(self.__version__))

        # General variables defining the environment
        self.SHAPE = (13, 13, 20)

        self.curr_step = -1
        self.curr_episode = -1
        self.curr_action = -1
        self.is_hand_over = False
        self.is_hand_won = False 

        self.action_space = spaces.Discrete(12)
        # see dict: constants.act_array
        
        # Observation is the game state and prior actions
        low = np.zeros(self.SHAPE)
        high = np.ones(self.SHAPE)
        self.observation_space = spaces.Box(low, high)
        #DP, https://github.com/openai/gym/blob/master/gym/spaces/box.py
        
        self.mongodb_cursor = MongoClient('localhost', 27017).poker.parsed_handLog.find().batch_size(6000)
        #MongoClient('localhost', 27017).poker.dataframes.find()
        self.hand_db_counter = -1

        # db = client.poker
        # dfs = db.dataframes
        # count = 0
        self.two_eps = ({},{})
        self.which_ep = 0
        self.raw_hand = {}
        self.action_dict = {"fold":0, "check_call": 1, "bet 0.2":2, "bet 0.375": 3,\
        "bet 0.55": 4, "in pot 0.75": 5, "bet 1": 6,"bet 1.5":7, "bet 2":8,"bet 2.5":9,\
        "bet 3":10, "bet 5":11}
        self.action_dict = dict(zip(self.action_dict.values(), self.action_dict.keys()))
        print(self.action_dict)

        # self.hh_df = pd.read_pickle(\
        #     "C:/Users/dsp21/NYDS/Project/Capstone Ideas/Poker bot/git_things/test_episodes1000.pickle")
        #columns = ["obs", "acts", "reward", "done", "num_steps"]

    def _step(self, action):
        """
        The agent takes a step in the environment.

        Parameters
        ----------
        action : int

        Returns
        -------
        ob, reward, episode_over, info : tuple
            ob (object) :
                an environment-specific object representing your observation of
                the environment.
            reward (float) :
                amount of reward achieved by the previous action. The scale
                varies between environments, but the goal is always to increase
                your total reward.
            episode_over (bool) :
                whether it's time to reset the environment again. Most (but not
                all) tasks are divided up into well-defined episodes, and done
                being True indicates the episode has terminated. (For example,
                perhaps the pole tipped too far, or you lost your last life.)
            info (dict) :
                 diagnostic information useful for debugging. It can sometimes
                 be useful for learning (for example, it might contain the raw
                 probabilities behind the environment's last state change).
                 However, official evaluations of your agent are not allowed to
                 use this for learning.
        """
        if self.is_hand_over:
            raise RuntimeError("Episode is done")

        reward = self._get_reward()
        self._take_action(action) 
        self.curr_step += 1
        ob = self._get_state() #observation is next one

        return ob, reward, self.is_hand_over, {}

    def _get_action(self):
        self.curr_action = self.two_eps[self.which_ep]["acts"][self.curr_step]
        #self.curr_action = self.hh_df.loc[self.curr_episode,"acts"][0][self.curr_step]
        return self.curr_action

    def _take_action(self, action, check_action = False):
        self._get_action()
        if check_action:
            if self.curr_action != action:
                print("action passed not same as current act: {0:d} {0:d}".format(action, curr_action))
                #Does action meet what was next in the hand state database?

        self.is_hand_over =  self.two_eps[self.which_ep]["done"][self.curr_step] 
        #self.hh_df.loc[self.curr_episode,"done"][0][self.curr_step]


    def _get_reward(self):
        """Reward is given for a sold banana."""
        return self.two_eps[self.which_ep]["reward"][self.curr_step] #self.hh_df.loc[self.curr_episode,"reward"][0][self.curr_step]


    def _reset(self):
        """
        Reset the state of the environment and returns an initial observation.

        Returns
        -------
        observation (object): the initial observation of the space.
        """
        self.curr_episode += 1
        if self.which_ep == 1:
            self.get_two_eps_()
            self.which_ep = 0
        else:
            self.which_ep += 1

        self.curr_step = 0
        try:
            self._get_action()
        except:
            return self._reset()
        self.is_hand_over = False

        return self._get_state()

    def _get_state(self):
        """Get the observation."""
        return self.two_eps[self.which_ep]["obs"][self.curr_step] 

    def _render(self, mode='human', close=False):
        print("Tried to render, but no rendering function built")
        return

    def print_state(self):
        try:
            print("\n","$"*40)
            print("Raw Hand:")
            print(self.raw_hand)
            print("**",str(self.which_ep),"**")
            print("episode rewards and actions: ")
            print(list(self.two_eps[self.which_ep]["reward"]))
            print(list(self.two_eps[self.which_ep]["acts"]))
            print("#"*20)
            print("Player: ", str(self.which_ep))
            print("Step: ", str(self.curr_step))
            print("Reward from next act: ", str(self._get_reward()))
            print("Done: ", str(self.is_hand_over))
            print("#"*20)
            print("Action taken in hand log: ", str(self._get_action()), self.action_dict[self._get_action()], "\n")

        except Exception as e:
            print("tried to render but exception ", str(e))
        pass

    def get_two_eps_(self):
        self.hand_db_counter += 1
        self.raw_hand = self.mongodb_cursor.next()
        self.two_eps = run_iteration(self.raw_hand)
        if self.two_eps == (None, None):
            self.get_two_eps_()


