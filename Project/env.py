import paho.mqtt.client as mqtt
from validator import Validator
import numpy as np
import pytesseract
import threading
import base64
import time
import json
import cv2
import io

buffer = io.BytesIO()

BROKER = "localhost"
PORT = 1883
TOPIC_SUB_info = "env/info"
TOPIC_PUB_info = "env/request"
TOPIC_PUB_ex = "env/action"
TOPIC_SUB_ex = "env/response"
TOPIC_PUB_reset = "env/reset"
TOPIC_SUB_reset = "env/reset_response"  # Ajout pour la cohérence


class Env(object):
    def __init__(self, OS: str):
        self.OS = OS
        self.validator = Validator()
        
        # Locks pour thread safety
        self.info_lock = threading.Lock()
        self.ex_lock = threading.Lock()
        self.reset_lock = threading.Lock()
        
        # Client pour les infos
        self.client_info = mqtt.Client(client_id="info_client")
        self.client_info.on_message = self.on_message_info
        self.client_info.connect(BROKER, PORT, 60)
        self.client_info.subscribe(TOPIC_SUB_info)
        self.client_info.loop_start()
        self.received_info = False
        self.info = None
        
        # Client pour l'exécution
        self.client_ex = mqtt.Client(client_id="executor_client")
        self.client_ex.on_message = self.on_message_ex
        self.client_ex.connect(BROKER, PORT, 60)
        self.client_ex.subscribe(TOPIC_SUB_ex)
        self.client_ex.loop_start()
        self.received_ex = False
        self.ex_response = None
        
        # Client pour le reset
        self.client_reset = mqtt.Client(client_id="reset_client")
        self.client_reset.on_message = self.on_message_reset
        self.client_reset.connect(BROKER, PORT, 60)
        self.client_reset.subscribe(TOPIC_SUB_reset)
        self.client_reset.loop_start()
        self.received_reset = False

    def on_message_info(self, client, userdata, msg):
        with self.info_lock:
            try:
                payload = json.loads(msg.payload.decode())
                
                # Décoder image base64
                img_b64 = payload["image"]
                img_bytes = base64.b64decode(img_b64)
                img_np = np.frombuffer(img_bytes, dtype=np.uint8)  # Convert bytes to NumPy array
                img = cv2.imdecode(img_np, cv2.IMREAD_GRAYSCALE)  # Decode as BGR image (OpenCV default)
                #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                apps = payload["context"]
                self.info = [img, apps]
                self.received_info = True
            except Exception as e:
                print(f"Erreur lors du traitement du message info: {e}")
                self.received_info = False

    def on_message_ex(self, client, userdata, msg):
        with self.ex_lock:
            try:
                self.ex_response = msg.payload.decode()
                self.received_ex = True
            except Exception as e:
                print(f"Erreur lors du traitement du message ex: {e}")
                self.received_ex = False

    def on_message_reset(self, client, userdata, msg):
        with self.reset_lock:
            self.received_reset = True

    def is_action_valid(self, state, next_state):
        return self.validator.validate_action(state, next_state)

    def capture_info(self):
        # Pour la phase 2, on entrainera le model a ouvrir parfaitement une app
        # Pour la phase 3, on entrainera le model a naviguer dans une app sans vision seulement avec l'ocr
        # OCR contextuel
        if self.info is None:
            return None
            
        img, context = self.info
        text = pytesseract.image_to_string(img)
        ocr = text.split('\n')
        return context, img  # pour la phase 2
        # return [apps, ocr] # phase 3

    def get_win_info(self):
        pass

    def get_linux_info(self):
        pass

    def get_info(self, msg):
        if self.OS == "macos":
            return self.get_mac_info(msg)
        elif self.OS == "windows":
            return self.get_win_info()
        elif self.OS == "linux":
            return self.get_linux_info()

    def get_mac_info(self, msg):
        with self.info_lock:
            self.received_info = False  # Reset propre ici
        
        self.client_info.publish(TOPIC_PUB_info, msg)
        
        timeout = 10
        start = time.time()
        while not self.received_info and time.time() - start < timeout:
            time.sleep(0.1)
        
        if not self.received_info:
            print("Timeout: Aucune réponse reçue pour get_mac_info")
            time.sleep(3)
            return self.capture_info()
            
        return self.capture_info()

    def step(self, action):
        time.sleep(1.5)
        with self.ex_lock:
            self.received_ex = False
            self.ex_response = None
        
        # Publier l'action
        self.client_ex.publish(TOPIC_PUB_ex, f"{action}")
        
        # Attendre la réponse
        timeout = 5
        start = time.time()
        while not self.received_ex and time.time() - start < timeout:
            time.sleep(0.1)
        
        if not self.received_ex:
            print(f"Timeout: Aucune réponse reçue pour l'action '{action}'")
            time.sleep(3)
        
            # Obtenir les nouvelles infos
            return self.get_info("step")
        
        #print(f"Réponse reçue: {self.ex_response}")
        
        # Attendre que l'action soit complètement exécutée
        time.sleep(1)
        
        # Obtenir les nouvelles infos
        return self.get_info("step")

    def reset(self):
        self.client_info.publish(TOPIC_PUB_reset, "reset")
        return self.get_info("reset")

    def cleanup(self):
        """Méthode pour nettoyer les connexions MQTT"""
        self.client_info.loop_stop()
        self.client_info.disconnect()
        self.client_ex.loop_stop()
        self.client_ex.disconnect()
        self.client_reset.loop_stop()
        self.client_reset.disconnect()