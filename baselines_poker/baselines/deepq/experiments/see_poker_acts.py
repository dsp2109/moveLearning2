import gym_poker_history
import gym

from baselines import deepq
import numpy as np

# import zipfile
# import cloudpickle
# import baselines.common.tf_util as U
# import os

def main():
    env = gym.make("PokerHistory-v0")
    
    # td = "/tmp/tmpugaszyfi"
    # model_file = os.path.join(td, "model")
    # U.load_state(model_file)
    # act.save("poker_model_test.pkl")
    act = deepq.load("poker_model.pkl")

    rL = []
    for num_steps in range(1000):
        obs = env.reset()
        done = False
        
        episode_rew = 0
        action = None
        while not done: #this will spit out a random number of hands bc who knows if the state is done in a random pull
            env.print_state()
            action = act(obs[None])[0]
            print("Action choice: ", str(action), ":", env.action_dict[action])
            obs, rew, done, _ = env.step(action)
            # import pdb; pdb.set_trace()
            episode_rew += rew # if the hand states are random this has no meaning.
            rL.append(rew)
        print("Episode reward", episode_rew)
    print("Mean and stdev of reward is: {}, {}".format(np.mean(rL), np.std(rL)))


if __name__ == '__main__':
    main()
