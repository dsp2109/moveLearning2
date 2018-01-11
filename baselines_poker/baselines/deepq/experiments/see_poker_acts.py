import gym_poker_history
import gym

from baselines import deepq


def main():
    env = gym.make("PokerHistory-v0")
    act = deepq.load("poker_model.pkl")
    num_steps = 0
    while num_steps < 10:
        num_steps += 1
        obs, done = env.reset(), False
        episode_rew = 0
        action = None
        while not done: #this will spit out a random number of hands bc who knows if the state is done in a random pull
            env.print_state()
            action = act(obs[None])[0]
            print("Action choice: ", str(action), ":", env.action_dict[action])
            obs, rew, done, _ = env.step(action)
            # episode_rew += rew #the hands are random so this has no meaning.
        print("Episode reward", episode_rew)


if __name__ == '__main__':
    main()
