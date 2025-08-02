import groq
import logging
import base64
import os

class Brain:
    def __init__(self):
        self.client = groq.Groq(api_key=os.environ.get("GROQ_API_KEY"))
        

    def response(self, msg, state, correction, next_state, history, env):
        # Configurer la journalisation
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        prompt = ""
        if not correction:
            prompt = f"""
                    [CONTEXT]
                    Current state : {state}
                    [GOAL]
                    {msg}

                    [FORMAT]
                    Generate a sequence of key presses for {env} to achieve the goal in a valid json.:
                    {{
                    "reasoning": "step by step analysis",
                    "action": ["list", "of", "keys"],
                    "confidence": 0-1
                    }}
                    [EXAMPLE]
                    {{ "reasoning": "I want to open a new tab", "action": ["cmd+t"], "confidence": 0.9 }}
                    """
            # si la séquence de touches ne permet pas d'atteindre l'objectif
        else:
            # Création du prompt ayant pour but de verifier si l'action est correcte par rapport a but a l'etat a t+1 (apres l'action), si l'action n'est pas correcte, on demande a l'IA de corriger l'action
            prompt = f"""
                    [ROLE]
                    You are an expert in macOS automation and reinforcement learning validation.  
                    Your task is to evaluate whether the last action taken by the agent is a valid step toward achieving the goal : {msg}.  

                    [CONTEXT]
                    ## Initial State (t) : {state}
                    

                    ## Resulting State (t+1) : {next_state}

                    [OBJECTIVE]
                    Evaluate the validity of the last action based on the transition from state t to state t+1:
                    1. **Consistency Check**: Did the action produce an expected state change?  
                    2. **Goal Proximity**: Did the new state bring the agent closer to the goal?  
                    3. **Error Detection**: Did unexpected elements or errors appear?  

                    If the action is incorrect, provide a corrected sequence of key presses to achieve the goal.  

                    [OUTPUT FORMAT]
                    Return a **valid JSON** object with the following structure:
                    ```json
                    {{
                    "reasoning": "Step-by-step analysis of the action's effect",
                    "is_valid": 0 or 1,
                    "correction": ["list", "of", "keys"] or null,
                    "confidence": float (0.0 to 1.0),
                    "goal_proximity" : float (0.0 to 1.0),
                    }}
                    [EXAMPLE] Valid Action
                    {{
                    "reasoning": "The last action successfully opened the Terminal application. This is one step forward the goal.",
                    "is_valid": "1",
                    "correction": null,
                    "confidence": 0.95,
                    "goal_proximity" : 0.5
                    }}
                    [EXAMPLE] Invalid Action
                    {{
                    "reasoning": "The last action did not change the active application as expected. So...",
                    "is_valid": "0",
                    "correction": ["cmd+space", "Safari", "enter"],
                    "confidence": 0.87,
                    "goal_proximity" : 0.1
                    }}
                    [FINAL QUESTION] 
                    Evaluate if the action '{history[-1]}' made any progress towards the goal, even if small. 
                    Consider partial progress as valid. Only invalidate if the action clearly moved away from the goal or caused an error.

                    """

        try:
                
            chat_completion = self.client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="deepseek-r1-distill-llama-70b",
                    )
            key_sequence = chat_completion.choices[0].message.content
            return key_sequence
        except Exception as e:
                logging.error(f"Error in AI response: {e}")

    def correction(self, msg, state, next_state, history, env,correction=True):
        return self.response(msg, state, correction, next_state, history, env)
    
    # Function to encode the image
    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def vision(self, image_path, prompt):
           # Getting the base64 string
        base64_image = self.encode_image(image_path)



        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"{prompt}"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model="llama-3.2-90b-vision-preview",
        )

        vision = chat_completion.choices[0].message.content
        return vision