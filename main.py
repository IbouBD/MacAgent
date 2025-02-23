from env import*
from agent import*
from rl import *

env = Env("macos")
brain = Brain()
agent = Agent(brain)
current_env = env.getOS()
instructor = Instructor(brain, agent.history, current_env)
replay_buffer = ReplayBuffer(10000)

def main():
    state = env.getState()
    msg = "Give me the meteo in Paris using Safari"

    key_sequence = agent.generate_sequence(msg, state, current_env)
    sk = agent.extract_action(key_sequence)
    print(sk)
    for i in range(agent.queue.size()):

        action = agent.queue.peek()
        agent.queue.remove()
        agent.history.append(action)
        print(action)
        print("history", agent.history)

        """Vérifier si l'action est valide avant de passer a l'action suivante avec l'environnement grace a un llm et récompenser ou punir l'agent en conséquence."""

        state = env.getState()
        agent.step_action(action)
        initial_img = env.capture_screen()
        timeout = 5  # secondes maximum
        start_time = time.time()

        while True:
            current_img = env.capture_screen()
            if env.change_on_screen(initial_img, current_img):
                print("L'écran a été modifié.")
                break
            if time.time() - start_time > timeout:
                print("Timeout : aucun changement significatif détecté.")
                break
            time.sleep(0.5)  # pause courte entre les vérifications
            
        next_state = env.getState()

        is_valide, correction, goal_proximity = instructor.evaluate(msg, state, next_state)
        
        instant_memory = str(f"[{(action, is_valide, goal_proximity, correction)}]")
        env.instant_memory = instant_memory

        if is_valide == True:
            reward = instructor.reward(action, None, goal_proximity, is_valide) # Récompensé pour sa bonne action
            print("reward :", reward)
            pass
        else:
            # Corriger l'action
            if correction is not None and correction != action:
                agent.step_action(correction)
                agent.history.append(correction)
                instructor.history.append(correction)

            if correction is not None:
                reward = instructor.reward(action, correction, goal_proximity, is_valide) # Punit pour sa mauvaise action
                print("reward :", reward)

        obs = (state, action, reward, next_state, is_valide, goal_proximity)        

        replay_buffer.store_transition(obs)

if __name__ == "__main__":
    main()