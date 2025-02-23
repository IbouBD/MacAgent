"""Definissons l'agent llm chargé de générer des séquences de touches pour atteindre un objectif donné."""
import logging
import json
from json.decoder import JSONDecodeError
from pynput.keyboard import Key, Controller
import time
import re
import ast
from brain import*


keyboard = Controller()



class Queue():
    def __init__(self):
        self.queue = []
        pass

    def add(self, item):
        self.queue.append(item)

    def remove(self):
        if len(self.queue) > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)

    def peek(self):
        if len(self.queue) > 0:
            return self.queue[0]
        else:
            return None

    def __str__(self):
        return str(self.queue)

class Agent:
    def __init__(self, brain):
        self.history = []
        self.actions = None
        self.queue = Queue()
        self.key_sequence = None
        self.brain = brain
        self.mouse = Controller()
        self.mouse_pos = (float('inf'), float('inf'))
        self.KEY_MAP = {
            "cmd": Key.cmd,
            "ctrl": Key.ctrl,
            "alt": Key.alt,
            "shift": Key.shift,
            "enter": Key.enter,
            "return":Key.enter,
            "space": Key.space,
            "esc": Key.esc
        }


    def split_key_sequence(self, ks):
        result = []
        current = []
        for key in ks:
            current.append(key)
            if key == "enter" or key== "return":
                result.append(current.copy())
                current.clear()
        # S'il reste des éléments après le dernier "enter", on les ajoute aussi.
        if current:
            result.append(current.copy())
        return result
    

    def generate_sequence(self, msg, state, env):
        # Générer une séquence de touches pour atteindre l'objectif
        key_sequence = self.brain.response(msg, state, correction=False, next_state=None, history=self.history, env=env)
        return key_sequence
    
    def extract_action(self, key_sequence):
        logging.info(f"Generated key sequence: {key_sequence}")
        
        # Extraction améliorée avec validation JSON
        try:
            parsed = json.loads(key_sequence.replace("'", "\""))
            if isinstance(parsed, list):
                key_sequence = parsed
        except JSONDecodeError:
            matches = re.findall(r"\[.*?\]", key_sequence)
            if matches:
                try:
                    key_sequence = ast.literal_eval(matches[0])
                except (SyntaxError, ValueError) as e:
                    logging.error(f"Invalid key syntax: {e}")
                    key_sequence = []
            else:
                key_sequence = []

        self.key_sequence = key_sequence
        sk = self.split_key_sequence(key_sequence)
        for s in sk:
            self.queue.add(s)
        
        return sk
    
    def step_action(self, key_sequence):
        """Exécute une séquence de touches"""

        for key_combo in key_sequence:
            try:
                time.sleep(0.05)  # Réduction du délai pour fluidité
                
                if isinstance(key_combo, str):
                    keys = key_combo.split('+')
                    key_objs = []
                    
                    # Conversion des touches
                    for k in keys:
                        key = self.KEY_MAP.get(k.lower(), k)
                        if isinstance(key, str) and len(key) == 1:
                            key = key.lower()  # Normalisation des caractères
                        key_objs.append(key)
                    
                    # Press des modificateurs d'abord
                    modifiers = [k for k in key_objs if isinstance(k, Key)]
                    non_modifiers = [k for k in key_objs if k not in modifiers]
                    
                    for mod in modifiers:
                        keyboard.press(mod)
                    
                    # Press des touches normales
                    for key in non_modifiers:
                        if isinstance(key, Key):
                            keyboard.press(key)
                            keyboard.release(key)
                        else:
                            for k in key:
                                keyboard.press(k)
                                keyboard.release(k)
                                time.sleep(0.05)
                            
                    
                    # Release des modificateurs
                    for mod in reversed(modifiers):
                        keyboard.release(mod)
                    
                elif isinstance(key_combo, list):
                    self.step_action(key_combo)  # Gestion récursive
                    
            except Exception as e:
                logging.error(f"Action failed for '{key_combo}': {str(e)}")
                self.rollback_safety()

    def rollback_safety(self):
        """Annule la dernière action"""
        keyboard.press(Key.ctrl)
        keyboard.press('z')
        keyboard.release('z')
        keyboard.release(Key.ctrl)
        time.sleep(0.5)