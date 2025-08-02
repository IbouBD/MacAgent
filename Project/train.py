from utils import mean_episode_length, mean_reward, succes_rate, translate, preprocess_image
from training_data import phase1 as instruction_list1 # instruction explicites, ex: "Ouvre Safari"
from training_data import phase2 as instruction_list2 # instruction plus implicites, ex: "J'aimerai faire une recherche"
from training_data import phase3 as instruction_list3 # idem en plus complexe
import matplotlib.pyplot as plt
from validator import Validator
from PPO import Agent
from env import Env
import numpy as np
import random
import torch
import time
import os

# phase1 seed = 42 (& 73)
#sd = 42
# phase2 seed = 92
#sd = 92
# phase3 seed = 77380
# phase5 seed = 2048

sd = 42

def set_seed(seed=sd):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

sr_list = []
mel_list = []
mr_list = []

os.environ["TOKENIZERS_PARALLELISM"] = "false"
batch_size = 5
n_epochs = 4
alpha = 0.0003
policy_clip = 0.2
gamma=0.99
lamda=0.95 

def train(os:str):
    set_seed()
    random.shuffle(instruction_list1)
    random.shuffle(instruction_list2)
    random.shuffle(instruction_list3)
    #instruction_list = instruction_list1[:int(0.3*len(instruction_list1))] + instruction_list3[:int(0.9*len(instruction_list3))] + instruction_list2[:int(0.7*len(instruction_list2))]
    instruction_list = instruction_list1
    #random.shuffle(instruction_list)
    num_episodes = len(instruction_list)
    env = Env(os)
    val = Validator()
    agent = Agent(gamma=gamma, 
                policy_clip=policy_clip, 
                lamda=lamda, 
                n_epochs=n_epochs, 
                batch_size=batch_size
            )
    attemps_list = []
    num_succes = 0
    reward_list = []
    for i in range(num_episodes):
            instruction, target_app, acceptable_apps_list = instruction_list[i]
            print("######################################################")
            print("Instruction :",instruction)
            print("target :",target_app)
            current_info, state_img = env.reset()
            current_img_arr = preprocess_image(state_img)
            episode = i+1
            reward = 0.0
            next_obs = None
            done = False
            n_attempt = 0
            task_completed = False
            max_attemps_per_episode = 5
            score = 0
            action_history = []
            # enlever le contexte de temps en temps pendant l'entrainement
            if episode % 4 == 0:
                state = [instruction]
            else:
                #state = [instruction + f"{current_info}"]
                state = [{
                    "instruction": instruction,
                    "active_app": current_info['open_apps'],
                    "focused_element": current_info['focused_app'],
                    "recent_actions": action_history[-3:]
                }]
            while not done:
                
                obs = [instruction] + [current_info]
                action_tensor, prob, value, mousse_pos = agent.choose_action(state, current_img_arr)
                action = translate(action_tensor)
                action_ids = action_tensor.tolist()[0]  # batch_size = 1
                action_history.append(action_ids)
                print(f"Action: {action}, Mousse Positions: ({'%.2f' % mousse_pos[0][0] if mousse_pos is not None else 'No input img'}, {'%.2f' % mousse_pos[0][1] if mousse_pos is not None else 'No input img'})")
                # gérér maintenant l'exécution de l'action dans la VM
                next_info, next_state_img = env.step(action)
                next_img_arr = preprocess_image(next_state_img)
                next_state = [{
                    "instruction": instruction,
                    "active_app": next_info['open_apps'],
                    "focused_element": next_info['focused_app'],
                    "recent_actions": action_history[-3:]
                }]
                next_obs = [instruction] + [next_info]
                
                change = env.is_action_valid(obs, next_obs)
                print("modification", change)
                reward, task_completed = val.compute_reward(obs,next_obs,target_app,acceptable_apps_list,reward,agent.actor.encoder,action, step=n_attempt)

                if task_completed:
                    done = True
                    
                elif n_attempt >= max_attemps_per_episode:
                    reward -= 1.0
                    done = True
                
                    
                if len(action_history) > 1 and action_ids == action_history[-2]:
                    reward -= 2.0

                if done == True:
                    with torch.no_grad():
                        next_value = (
                            torch.tensor([0.0], device=agent.actor.device)
                            if done else
                            agent.critic(next_state)
                        )
                else:
                    next_value = agent.critic(next_state)
                
                print("current reward:", reward)
                score += reward
                agent.store_data(state, action_tensor.detach(), prob.detach(), value.detach(), next_value.detach(), reward, done)
                n_attempt += 1
                # à décommenter lorque state prendra le context en plus
                state = next_state
                current_img_arr = next_img_arr
                reward = 0.0 
                len_buffer = len(agent.memory.actions)
                if len_buffer >= batch_size:
                    print("*************** learning ***************")
                    agent.learn()
                    agent.memory.clear_memory()
                time.sleep(1)

            if task_completed:
                num_succes += 1
            if episode % 10 == 0:
                agent.save_models()
            
            attemps_list.append(n_attempt)
            reward_list.append(score)
            
            print(f"Episode: {episode}/{num_episodes}, Score: {score}, Attempt: {n_attempt}")
            print()
            sr = succes_rate(num_succes, episode)
            mel = mean_episode_length(episode, attemps_list)
            mr = mean_reward(episode, reward_list)
            sr_list.append(sr)
            mel_list.append(mel)
            mr_list.append(mr)
if __name__=="__main__":
    train(os="macos")
    # Plotting
    plt.figure(figsize=(12, 8))

    plt.subplot(3, 1, 1)
    plt.plot(np.array(sr_list), label='Success Rate')
    plt.ylabel('Success Rate')
    plt.title('Training Metrics Over Episodes')
    plt.grid(True)
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(np.array(mr_list), label='Mean Reward', color='orange')
    plt.ylabel('Mean Reward')
    plt.grid(True)
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(np.array(mel_list), label='Episode Length', color='green')
    plt.xlabel('Episode')
    plt.ylabel('Length')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.savefig("Plots/training_metrics")
    plt.show()