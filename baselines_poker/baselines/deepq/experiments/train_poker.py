import gym_poker_history
import gym


from baselines import deepq


# def callback(lcl, glb):
#     # stop training if reward exceeds 199
#     is_solved = lcl['t'] > 100 and sum(lcl['episode_rewards'][-101:-1]) / 100 >= 199
#     return is_solved

# def conv_hwSize_out(length, filter_width, padding, stride):
#     return (length - filter_width + 2*padding)/stride + 1

def main():

    env = gym.make('PokerHistory-v0')

    print(env)
    
    ###
    #conv net hacked towards by skimming: https://arxiv.org/ftp/arxiv/papers/1608/1608.06037.pdf
    # and https://kaggle2.blob.core.windows.net/forum-message-attachments/69182/2287/A%20practical%20theory%20for%20designing%20very%20deep%20convolutional%20neural%20networks.pdf 
    ###
    #for hiddens: https://stats.stackexchange.com/questions/181/how-to-choose-the-number-of-hidden-layers-and-nodes-in-a-feedforward-neural-netw
    #

    model_test = deepq.models.cnn_to_mlp(
    convs=[(32, 3, 1), (32, 3,1), (32, 2, 1), (64,3,2), (64, 3, 1), (64,3,1), (128, 3,2)], #[(32, 8, 4), (64, 4, 2), (64, 3, 1)]
    hiddens=[256],
    dueling=True, #bool(args.dueling)
    layer_norm= False,
    )

    act = deepq.pok_learn(
        env,
        q_func=model_test,
        lr=1e-4,
        max_timesteps= 25000001, #60000000
        buffer_size=50000,
        exploration_fraction=0.1,
        exploration_final_eps=0.02,
        train_freq=8,
        print_freq=5000,
        callback=None,

    )
    print("Saving model to poker_model.pkl")
    act.save("poker_model.pkl")


if __name__ == '__main__':
    main()
