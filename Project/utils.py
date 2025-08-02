import numpy as np
import torch
import math
import json
import cv2

device = torch.device("mps")

dict_path = "Models/id_to_action.json"
IMG_SIZE = 448

with open(dict_path) as f:
    id_to_action_raw = json.load(f)

id_to_action = {int(k): v for k, v in id_to_action_raw.items()}


def succes_rate(num_succes, num_total_episode):
    return num_succes / num_total_episode

def mean_episode_length(num_episode, step_list):
    return sum(step_list)/num_episode

def mean_reward(num_episode, reward_list):
    return sum(reward_list) / num_episode

def translate(seq):
    return [id_to_action[n] for n in seq.tolist() if n!=1 and n!=2 and n!=3]

def preprocess_image(img=None, img_size=(IMG_SIZE, IMG_SIZE)):
    # Chargement en niveaux de gris
    #img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is not None:
    
        # 2. Prétraitement
        blur = cv2.GaussianBlur(img, (5, 5), 1.4)
        edges = cv2.Canny(blur, threshold1=100, threshold2=200)  # Utiliser blur pour de meilleurs résultats
        edges = cv2.resize(edges, img_size)  # Taille attendue par MouseNet (64x64)

        # 3. Ajouter les dimensions manquantes
        # - Convertir en float32 et normaliser [0, 255] -> [0, 1]
        edges = edges.astype(np.float32) / 255.0

        # - Ajouter les dimensions: [Hauteur, Largeur] -> [Canaux, Hauteur, Largeur]
        edges = np.expand_dims(edges, axis=0)  # Maintenant shape (1, 64, 64)
        
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        img_arr = torch.tensor(edges, dtype=torch.float32).unsqueeze(0).to(device)

    
        return img_arr #,resized, img.shape[:2]  # image filtrée, taille originale
    else:
        return img

def compute_reward(self, state, next_state, target_app, acceptable_apps_list, reward, encoder, action, action_text: str = " ", alpha: float = 0.52, lamda: float = 1.0):
        instruction, context = state[0], state[1]
        next_instruction, next_context = next_state[0], next_state[1]
        current_apps = context["open_apps"]
        next_apps = next_context["open_apps"]
        expected_app = target_app
        diff = [x for x in next_apps if x not in current_apps]
        if len(diff) >= 1:
            open_app = diff[0]
        else:
            open_app = None

        # Match exact
        
        expected_app = self.normalize_app_name(expected_app)
        current_apps = [self.normalize_app_name(app_name) for app_name in current_apps]

        # Nettoyage action_text si absent
        if not action_text.strip():
            action_text = f"open {action[1]}" if len(action) > 1 else "open nothing"

        succes = False
        semantic_reward = self.semantic_similarity(instruction, action_text, encoder)  # ∈ [-1, 1]

        # Cas où aucune cible n’est connue : on juge juste la cohérence
        if not expected_app:
            if semantic_reward > alpha:
                semantic_reward += 3 * lamda * semantic_reward
                succes = True
            return semantic_reward, succes
        
        if acceptable_apps_list is not None and open_app is not None:
            acceptable_apps_list_norm = [self.normalize_app_name(app) for app in acceptable_apps_list]
            open_app = self.normalize_app_name(open_app)
            if open_app in acceptable_apps_list_norm:
                succes = True
                if semantic_reward > alpha:
                    semantic_reward += 3 * lamda * semantic_reward + 5.0
                return semantic_reward, succes

        # Similarité floue avec les apps ouvertes
        app_similarities = [self.semantic_similarity(expected_app, app, encoder) for app in current_apps]
        max_sim = max(app_similarities) if app_similarities else 0
        if max_sim > 0.7:
            reward += 3.0
            succes = True

        if expected_app in current_apps:
            reward += 5.0
            succes = True
        else:
            reward += 0.2 if current_apps else -0.5

        # L’agent mentionne explicitement l’app correcte
        if expected_app in action_text.lower():
            reward += 3.0
            succes = True

        # Bonus si action pertinente ET intention comprise
        if succes and semantic_reward > 0.6:
            reward += 2.0

        # Pénalité uniquement si l’action est mauvaise
        if not succes:
            reward -= 0.2

        # Pondération globale du signal sémantique
        reward += 2 * lamda * semantic_reward

        return reward, succes