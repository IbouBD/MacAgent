import re
import torch
import torch.nn.functional as F


def extract_app_name(text):
    # Liste de verbes ou phrases qui précèdent souvent le nom d'une application
    triggers = [
        r'\bopen\b', r'\blaunch\b', r'\brun\b', r'\bstart\b',
        r'\bI want you to run\b', r'\bexecute\b', r'\bI want you to run a \b', 
        r'\bI want you to run the \b'
    ]

    # Créez un motif regex qui cherche les déclencheurs suivis de mots
    pattern = re.compile(rf"(?:{'|'.join(triggers)})\s+([a-zA-Z]+)", re.IGNORECASE)

    # Recherchez le motif dans le texte
    match = pattern.search(text)
    if match:
        return match.group(1)
    else:
        return None

class Validator(object):

    def __init__(self):
        pass

    def is_safe(self, action):
        return not any(tok in action for tok in ["shutdown", "rm", "forcequit"])

    def validate_action(self, state_before, state_after):
        
        if state_before != state_after:
            return True
        else :
            return False
        
    def semantic_similarity(self, instr: str, action_text: str, encoder) -> float:
        instr_emb = encoder.encode(instr, convert_to_tensor=True)
        act_emb = encoder.encode(action_text, convert_to_tensor=True)
        sim = F.cosine_similarity(instr_emb, act_emb, dim=0).item()
        return sim

    def normalize(self, name):
        return name.strip().lower().replace(".app", "")
        
    def compute_reward(self,
    state,
    next_state,
    target_app,
    acceptable_apps_list,
    reward,
    encoder,
    action,
    step: int = 0,
    action_text: str = "",
    alpha: float = 0.6,
    beta: float = 0.8,
    max_steps: int = 3
):
        # --- Pré-traitements ---
        expected = self.normalize(target_app)
        open_before = [self.normalize(app) for app in state[1]["open_apps"]]
        open_after = [self.normalize(app) for app in next_state[1]["open_apps"]]
        action_app = self.normalize(action[1]) if len(action) > 1 else None
        action_text = action_text or f"open {action[1]}" if action_app else "open nothing"
        new_apps = [app for app in open_after if app not in open_before]

        # --- Initialisation ---
        success = False
        reward = 0.0

        # --- 1. Succès complet (application cible ouverte) ---
        for app in new_apps:
            sim = self.semantic_similarity(expected, app, encoder)
            if sim > beta:
                reward += 10.0
                success = True
                break

        # --- 2. Succès partiel (application acceptable ouverte) ---
        """
        if not success and acceptable_apps_list:
            acceptable_norm = [self.normalize(app) for app in acceptable_apps_list]
            for app in new_apps:
                if app in acceptable_norm or action_app in acceptable_norm:
                    reward += 5.0
                    success = True
                    break
        """

        # --- 3. Récompense sémantique (compréhension partielle de l’intention) ---
        sim_instruction_action = self.semantic_similarity(state[0], action_text, encoder)
        if sim_instruction_action > alpha:
            reward += (2.0 if not success else 0.0) + sim_instruction_action * 2.0

        # --- 4. Récompense pour mention explicite (forme linguistique correcte) ---
        sim_explicit = self.semantic_similarity(f"open {expected}", action_text, encoder)
        if sim_explicit > alpha and not success:
            reward += 2.0

        # --- 5. Pénalités ---
        if not success:
            reward -= 2.0  # Pénalité pour échec
        reward -= 0.5 * step  # Pénalité légère pour chaque essai

        if len(action) < 3:
            reward -= 20
        # --- Clipping (facultatif) ---
        #reward = max(min(reward, 10.0), -5.0)

        return reward, success
