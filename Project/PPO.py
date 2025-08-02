import torch
import numpy as np
import torch.nn as nn
from model import Actor, Critic, VisionActor


class PPOMemory():
    """
    Memory for PPO
    """
    def  __init__(self, batch_size):
        self.states = []
        self.actions= []
        self.action_probs = []
        self.rewards = []
        self.vals = []
        self.next_vals = []
        self.dones = []
        self.batch_size = batch_size
        self.size = len(self.states)

    def generate_batches(self):
        n_states = len(self.states)
        batch_start = torch.arange(0, n_states, self.batch_size)

        indices = torch.randperm(n_states)  # shuffle 
        batches = [indices[i:i + self.batch_size] for i in batch_start]

        return (
            self.states,      # torch.Tensor
            self.actions,     # torch.Tensor
            self.action_probs,# torch.Tensor
            self.vals,        # torch.Tensor
            self.next_vals,   # torch.Tensor
            self.rewards,     # torch.Tensor
            self.dones,       # torch.Tensor
            batches           # list of torch.Tensor indices
        )
    

    def store_memory(self,state,action,action_prob,val,next_val,reward,done):
        self.states.append(state)
        self.actions.append(action)
        self.action_probs.append(action_prob)
        self.rewards.append(reward)
        self.vals.append(val)
        self.next_vals.append(next_val)
        self.dones.append(done)

    def clear_memory(self):
        self.states = []
        self.actions= []
        self.action_probs = []
        self.rewards = []
        self.vals = []
        self.next_vals = []
        self.dones = []
        self.size = len(self.dones)

class Agent():
    def __init__(self, gamma, policy_clip,lamda,
                 n_epochs, batch_size):
        
        self.device = torch.device("mps")
        self.gamma = gamma 
        self.policy_clip = policy_clip
        self.lamda  = lamda
        self.n_epochs = n_epochs
        dim, hidden, vocab_size, in_channels = 512, 512, 1949, 1
        #self.actor = Actor(dim, hidden, vocab_size).to(self.device)
        self.vactor = VisionActor(in_channels, dim, hidden, vocab_size).to(self.device)
        self.actor = self.vactor.actor
        self.critic = Critic().to(self.device)
        self.memory = PPOMemory(batch_size)
        self.actor.optimizer = torch.optim.AdamW(self.actor.parameters(), lr=3e-5)
        self.critic.optimizer = torch.optim.Adam(self.critic.parameters(), lr=1e-4)

        for param in self.actor.encoder.parameters():
            param.requires_grad = False

        for param in self.critic.encoder.parameters():
            param.requires_grad = False

    def store_data(self,state,action,action_prob,val,next_vals,reward,done):
        self.memory.store_memory(state,action,action_prob,val,next_vals,reward,done)
       

    def save_models(self):
        print('... Saving Models ......')
        torch.save(self.actor.state_dict(), "checkpoint/actor.pth")
        torch.save(self.critic.state_dict(), "checkpoint/critic.pth")


    def load_models(self):
        print('... Loading models ...')
        self.actor.load_checkpoint()
        self.critic.load_checkpoint()

    def choose_action(self, state: list[str], screenshots=None, start_token_id=1, end_token_id=2):
        # Encode l'état
        x = self.actor.encoder.encode(state, convert_to_tensor=True)
        x = self.actor.rffn(x)  # (batch_size, dim)
        if screenshots is not None:
            vision_features = self.vactor.mousenet.forward(screenshots, features_only=True) # shape: (batch_size, 128)
            vision_encoded = self.vactor.vision_rffn(vision_features) # shape: (batch_size, dim)
            vision_encoded = vision_encoded.unsqueeze(0) # shape: (1, batch_size, dim)
            memory, _ = self.vactor.fusion(x.unsqueeze(0), vision_encoded, vision_encoded) # shape (1, batch_size, dim)
        else:
            memory = x.unsqueeze(0)

        # Start token
        generated = torch.full((1, 1), start_token_id, dtype=torch.long, device=self.device)
        log_probs = []
        
        for _ in range(self.actor.max_len):
            tgt_embed = self.actor.embedding(generated).permute(1, 0, 2)
            tgt_embed = self.actor.pos_encoding(tgt_embed)
            tgt_mask = nn.Transformer.generate_square_subsequent_mask(generated.size(1)).to(self.device)
            
            output = self.actor.transformer_decoder(tgt_embed, memory, tgt_mask=tgt_mask)
            logits = self.actor.final_projection(output[-1])  # (1, vocab_size)

            # Distribution
            dist = torch.distributions.Categorical(logits=logits)
            next_token = dist.sample()  # (1,)
            log_prob = dist.log_prob(next_token)  # (1,)

            log_probs.append(log_prob)
            generated = torch.cat([generated, next_token.unsqueeze(0)], dim=1)

            if next_token.item() == end_token_id:
                break

        # Log prob total (sum over sequence)
        total_log_prob = torch.sum(torch.cat(log_probs))

        # Valeur d'état (pour PPO)
        value = self.critic(state)  # (1,)
        if screenshots is not None:
            pointer_out = self.vactor.pointer_head(vision_encoded.squeeze(0))  # (batch_size, 2)
            return generated.squeeze(0), total_log_prob, value, pointer_out
        return generated.squeeze(0), total_log_prob, value, screenshots

    
    def calculate_advanatage(self,reward_arr,value_arr, next_value_arr, dones_arr):
        time_steps = len(reward_arr)
        advantage = np.zeros(len(reward_arr), dtype=np.float32)

        for t in range(0,time_steps-1):
            discount = 1
            running_advantage = 0
            for k in range(t,time_steps-1):
                if int(dones_arr[k]) == 1:
                    running_advantage += reward_arr[k] - value_arr[k]
                else:
                
                    running_advantage += reward_arr[k] + (self.gamma*next_value_arr[k]) - value_arr[k]

                running_advantage = discount * running_advantage
                # running_advantage += discount*(reward_arr[k] + self.gamma*value_arr[k+1]*(1-int(dones_arr[k])) - value_arr[k])
                discount *= self.gamma * self.lamda
            
            advantage[t] = running_advantage
        advantage = torch.tensor(advantage).to(self.actor.device)

        return advantage
    
    def learn(self):
        for _ in range(self.n_epochs):

            ## initially all will be empty arrays
            state_arr, action_arr, old_prob_arr, value_arr, next_value_arr,\
            reward_arr, dones_arr, batches = \
                    self.memory.generate_batches()
            
            advantage_arr = self.calculate_advanatage(reward_arr,value_arr,next_value_arr,dones_arr)
            values = torch.tensor(value_arr).to(self.actor.device)

            for batch in batches[0]:
                states = state_arr[batch]
                old_probs = old_prob_arr[batch].to(self.actor.device)
                actions = action_arr[batch].to(self.actor.device)


                logits = self.actor(states, actions)
                dist = torch.distributions.Categorical(logits=logits)
                critic_value = self.critic(states)

                critic_value = torch.squeeze(critic_value)

                new_probs = dist.log_prob(actions)
                prob_ratio = new_probs.exp() / old_probs.exp()
                #prob_ratio = (new_probs - old_probs).exp()
                weighted_probs = advantage_arr[batch] * prob_ratio
                weighted_clipped_probs = torch.clamp(prob_ratio, 1-self.policy_clip,
                        1+self.policy_clip)*advantage_arr[batch]
                actor_loss = -torch.min(weighted_probs, weighted_clipped_probs).mean()

                returns = advantage_arr[batch] + values[batch]
                critic_loss = (returns-critic_value)**2
                critic_loss = critic_loss.mean()

                total_loss = actor_loss + 0.5*critic_loss
                self.actor.optimizer.zero_grad()
                self.critic.optimizer.zero_grad()
                total_loss.backward()
                self.actor.optimizer.step()
                self.critic.optimizer.step()

        self.memory.clear_memory()   