This repository contains a PIP package which is an OpenAI environment for
simulating an enironment in which bananas get sold. Its structure was forked from https://github.com/MartinThoma/banana-gym in case you see any "bananas" flying around in the code.
See here for the banana gym author for explanation in the second answer: https://stackoverflow.com/questions/45068568/is-it-possible-to-create-a-new-gym-environment-in-openai


## Installation

Install the [OpenAI gym](https://gym.openai.com/docs/).

Then install this package via

```
pip install -e .
```

## Usage

```
import gym
import gym_poker_history

env = gym.make('PokerHistory-v0')
```

See https://github.com/openai/baselines/blob/master/baselines/deepq/ for some
examples.


## The Environment

The "environment" is inheriting from the environment class so as to work well with open source code, like openai/baselines github. It feeds poker hands from last year's ACPC and supplies game state, action, rewards, and whether the hand is done. 

It can NOT take any action from the action state and return the resulting state/reward, because it is not a true environment, just a workaround to feed in hand logs and not disrupt the code in certain reinforcement learning solutions.

Hand logs can be found on this website: www.computerpokercompetition.org/

