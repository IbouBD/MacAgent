"""Définissons l'environnement dans lequel notre 
agent devra évouler, soit toutes les informations relatives à l'état du système et 
les actions possibles.
"""

import numpy as np
from AppKit import NSWorkspace
from PIL import ImageGrab, Image, ImageFilter
import pytesseract
from brain import*
import json
from json.decoder import JSONDecodeError
import re
from agent import*
import tempfile
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID
from difflib import SequenceMatcher
import logging
from typing import List



class Env(object):
    def __init__(self, OS:str ):
        self.info = self.capture_info()
        self.state = []
        self.actions = []
        self.rewards = []
        self.next_state = []
        self.done = False
        self.os = OS
        self.brain = Brain()
        self.instant_memory = None
        self.prompt = f"""
        You are an expert in macOS interface analysis and automation. Your mission is to examine the provided image and produce a detailed, structured description of the user interface, formatted in a JSON output. 

        Context:
        - Active Application: {self.info.get('active_app')}.
        - (Additional context about the current UI state may be provided externally.)

        Your Task:
        1. Identify and list all interactive UI elements (buttons, menus, text fields, icons, etc.) present on the interface.
        2. Describe the spatial layout and the relative positions of these elements.
        3. Evaluate the status of the last performed action using your instant memory (provided as {self.instant_memory}) and determine if it had the intended effect.
        4. Assess how much the current interface state brings the system closer to achieving the goal, and provide a goal proximity score between 0 and 1.

        Output Requirements:
        Your response must be a valid JSON object containing exactly the following keys:
        - "active_app": the active application (as provided by the context),
        - "ui_elements": a detailed description of the UI elements (list, string, or structured data as appropriate),
        - "last_action_status": your evaluation of the last action's effect (using the instant memory data),
        - "goal_proximity": a numerical score between 0 and 1 representing progress toward the goal.

        Example:
        {{
        "active_app": "Safari",
        "ui_elements": "Found: search bar at top, navigation buttons, footer icons, etc.",
        "last_action_status": "The previous action successfully opened a new tab.",
        "goal_proximity": "0.85"
        }}

        Please ensure your output is valid JSON and contains only the four keys mentioned.
        """



    def getOS(self):
        return self.os
    
    def change_on_screen(self, img1, img2, threshold=0.15, grid=(2,2)) -> bool:
        """
        Compare deux images en les divisant en régions.
        Applique un flou gaussien pour réduire le bruit.
        Retourne True si au moins une région présente une différence de moyenne supérieure au seuil.
        """
        # Conversion en niveaux de gris
        img1_gray = Image.fromarray(img1).convert("L")
        img2_gray = Image.fromarray(img2).convert("L")
        
        # Appliquer un flou gaussien pour réduire le bruit
        img1_blur = img1_gray.filter(ImageFilter.GaussianBlur(radius=2))
        img2_blur = img2_gray.filter(ImageFilter.GaussianBlur(radius=2))
        
        # Convertir en tableau numpy pour les calculs
        np1 = np.array(img1_blur, dtype=np.float32)
        np2 = np.array(img2_blur, dtype=np.float32)
        
        h, w = np1.shape
        regions_y, regions_x = grid
        region_h = h // regions_y
        region_w = w // regions_x

        for i in range(regions_y):
            for j in range(regions_x):
                # Extraire la région (bloc) de l'image
                region1 = np1[i*region_h:(i+1)*region_h, j*region_w:(j+1)*region_w]
                region2 = np2[i*region_h:(i+1)*region_h, j*region_w:(j+1)*region_w]
                diff = abs(np.mean(region2) - np.mean(region1))
                print(f"Différence région ({i},{j}) : {diff}")
                if diff > threshold:
                    return True
        return False
    

    def get_windows(self):
        window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
        return [
            {
                "app": w.get("kCGWindowOwnerName", "Unknown"),
                "x": w["kCGWindowBounds"]["X"],
                "y": w["kCGWindowBounds"]["Y"],
                "width": w["kCGWindowBounds"]["Width"],
                "height": w["kCGWindowBounds"]["Height"]
            }
            for w in window_list
        ]
    
    def capture_screen(self):
        return np.array(ImageGrab.grab())


    def capture_info(self):
        # Capture d'écran
        screenshot = self.capture_screen()
        
        # OCR contextuel
        text = pytesseract.image_to_string(screenshot)
        
        # Metadata système
        active_app = self.get_windows()
        
        return {
            "screenshot": screenshot,
            "ocr": text.split('\n'),
            "active_app": active_app
        }
        
    def getState(self):
        try:
            # Récupérer la capture d'écran depuis self.info (supposée être un tableau NumPy)
            screenshot = self.info.get("screenshot")
            if screenshot is None:
                raise ValueError("Aucune capture d'écran trouvée dans self.info.")

            img = Image.fromarray(screenshot)

            # Sauvegarder dans un fichier temporaire
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                img.save(tmp, format="PNG")
                tmp_path = tmp.name

            # Utiliser le chemin temporaire dans self.brain.vision
            state = self.brain.vision(tmp_path, self.prompt)

            # Construire l'état courant à partir des informations disponibles
            self.state = state
            return self.state

        except Exception as e:
            print(f"Erreur dans getState : {e}")
            return None
    
    def getActions(self):
        return self.actions
    
    def getRewards(self):
        return self.rewards
    
    def getDone(self):
        return self.done
    
class Instructor(object):
    def __init__(self, brain, agent_history, env):
    
        self.history = []
        self.brain = brain
        self.agent_history = agent_history
        self.env = env
        #self.reward_model = object

    def sequence_similarity(self, seq1, seq2):
        """
        Measure the similarity between two sequences using the SequenceMatcher from difflib.

        Args:
        seq1 (str): The first sequence.
        seq2 (str): The second sequence.

        Returns:
        float: A float in the range [0, 1] representing the similarity between the sequences.
        """
        return SequenceMatcher(None, seq1, seq2).ratio()
    
    def reward(self, action, correction ,goal_proximity, is_valide):
        
        # Calcul de la différence, par exemple avec une distance d'édition (Levenshtein)
        #distance = compute_edit_distance(generated_sequence, corrected_sequence)
        
        # On peut définir une récompense inversement proportionnelle à cette distance
        # et éventuellement ajouter une composante basée sur la progression vers l'objectif.
        #reward_value = max(0, 1 - (distance / len(corrected_sequence)))
        if correction is not None:
            similarity = self.sequence_similarity(action, correction)
            # reward proportionnel a la longeur de la chaine, tel que
            reward_value = similarity * len(correction)

        else :
            reward_value = goal_proximity * len(action)
        if is_valide:
            return reward_value * 2
        else:
            return reward_value * -2
    
    
    def extract_eval(self, eval):
         # Extraction améliorée avec validation JSON
        match = re.search(r'\{.*\}', eval, re.DOTALL)
        is_valid = None
        correction = None
        goal_proximity = None
        if match:
            json_str = match.group(0)  # On récupère le JSON sous forme de string
            try:
                data = json.loads(json_str)  # On le convertit en dictionnaire Python
                print("data", data)
                if "is_valid" in data:
                    is_valid = int(data["is_valid"])
                    print("is_valid :", is_valid)
                if "correction" in data:
                    correction = data["correction"]
                if "goal_proximity" in data:
                    goal_proximity = data["goal_proximity"]

                return bool(is_valid), correction, float(goal_proximity)
            except json.JSONDecodeError as e:
                print("Erreur lors du décodage JSON :", e)
        else:
            print("Aucun JSON trouvé dans la chaîne.")
                
        
    def evaluate(self, msg, state, next_state):

        # Evaluation de l'action
        evaluation = self.brain.correction(msg = msg, state = state, next_state = next_state, history = self.agent_history, env = self.env)

        v, c, g = self.extract_eval(evaluation)
        print("is valid", v)
        print("correction", c)
        print("goal proximity :", g)
        
        return v, c, g
    
    def evaluate_and_train(self):
        pass


class UnsafeBlock:
    def __init__(self, banned_actions: List[List[str]] = None):
        self.banned_actions = banned_actions or [
            ["sudo", "rm", "-rf", "/"],
            ["sudo", "shutdown", "-h", "now"],
            ["sudo", "reboot"],
            ["sudo", "poweroff"],
            ["sudo", "halt"]
        ]
        self.blocked_actions = []
        logging.basicConfig(filename='unsafe_actions.log', level=logging.INFO)

    def check_action(self, action: List[str]) -> bool:
        """
        Vérifie si l'action est autorisée ou non.
        """
        if any(all(part in action for part in banned) for banned in self.banned_actions):
            self.blocked_actions.append(action)
            logging.info(f"Blocked action: {action}")
            return False
        return True

    def rollback_safety(self, action: List[str]):
        """
        Implémentez ici la logique de rollback, par exemple,
        en restaurant un snapshot de la VM.
        """
        if self.is_unsafe_action_performed(action):
            print("Rolling back to previous state...")
        else:
            pass

    def notify_admin(self, action: List[str]):
        """
        Notifie l'administrateur de l'action bloquée.
        """
        logging.warning(f"Admin alert: Action blocked - {action}")

    def is_unsafe_action_performed(self, action: List[str]) -> bool:
        """
        Vérifie si l'action dangereuse a été effectué.
        """
        if action in self.blocked_actions:
            return True
        else:
            return False