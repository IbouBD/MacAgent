import numpy as np
from AppKit import NSWorkspace
from PIL import ImageGrab
import io
import pytesseract
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID
import paho.mqtt.client as mqtt
import json
import base64
import datetime
import subprocess
from PIL import Image, UnidentifiedImageError

from reset_env import reset

pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"



def format_info(info):
    apps = [w["app"] for w in info["active_app"]]
    visible_apps = ", ".join(sorted(set(apps)))
    ocr_lines = [line.strip() for line in info["ocr"] if line.strip()]
    ocr_context = ". ".join(ocr_lines)
    return f"visible apps: {visible_apps}. OCR: {ocr_context}"

class Env(object):
    def __init__(self):
        pass

    def get_windows(self):
        window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
        return [
            {
                "app": (w.get("kCGWindowOwnerName", "Unknown"), w.get('kCGWindowName', 'Unknown'), w['kCGWindowNumber']),
                "x": w["kCGWindowBounds"]["X"],
                "y": w["kCGWindowBounds"]["Y"],
                "width": w["kCGWindowBounds"]["Width"],
                "height": w["kCGWindowBounds"]["Height"],
                "title": w.get('kCGWindowName', 'Unknown')
            }
            for w in window_list
        ]

    def get_focused_window(self):
        # Nom de l'application actuellement en focus
        frontmost_app = NSWorkspace.sharedWorkspace().frontmostApplication()
        app_name = frontmost_app.localizedName()

        # Toutes les fenêtres visibles à l'écran
        window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)

        for window in window_list:
            owner = window.get('kCGWindowOwnerName', '')
            layer = window.get('kCGWindowLayer', 1)
            alpha = window.get('kCGWindowAlpha', 1.0)

            # On ne considère que les fenêtres visibles (layer 0, alpha > 0)
            if owner == app_name and layer == 0 and alpha > 0:
                title = window.get('kCGWindowName', 'Unknown')
                return {
                    "app": app_name,
                    "window_title": title or "Untitled"
                }

        # Si aucune correspondance trouvée
        return app_name


    def get_network_status(self):
        try:
            subprocess.check_output(['ping', '-c', '1', '8.8.8.8'])
            return "online"
        except:
            return "offline"

    def get_current_time(self):
        return datetime.datetime.now().isoformat()

    def get_day_of_week(self):
        return datetime.datetime.now().strftime("%A")

    def get_active_app(self):
        return NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
    
    def get_context(self):
        open_apps = [app['app'][0] for app in self.get_windows()]
        return  {
            "open_apps": open_apps,
            "focused_app": self.get_focused_window(),
            "focused_window_title": self.get_active_app(),
            "network_status": self.get_network_status(),
            "current_time": self.get_current_time(),
            "day_of_week": self.get_day_of_week(),
        }
    """
    def capture_screen(self):
        img = ImageGrab.grab()
        buffer = io.BytesIO()
        rgb_img = img.convert('RGB')
        rgb_img.save(buffer, format="JPEG")
        open_apps = self.get_windows()
        info = [buffer.getvalue(), open_apps]
        return json.dumps(info)
    """
    def capture_screen(self):
        context = self.get_context()
        try:
            screenshot = ImageGrab.grab()
            buffer = io.BytesIO()
            screenshot = screenshot.convert('RGB')
            screenshot.save(buffer, format="JPEG")
            img_bytes = buffer.getvalue()
            img_b64 = base64.b64encode(img_bytes).decode()
        except UnidentifiedImageError as e:
            print(f"Error: {e}")
            img_b64 = None

        # Paquet JSON
        payload = {
            "image": img_b64,
            "context": context
        }

        return json.dumps(payload)

    
    """
    def capture_info(self):
        screenshot = self.capture_screen()
        text = pytesseract.image_to_string(screenshot)
        active_app = self.get_windows()
        return {
            #"screenshot": screenshot,
            "ocr": text.split('\n'),
            "active_app": active_app
        }
    
    def get_env_info(self):

        return format_info(self.capture_info())
    """
    
env = Env()

# Configuration
BROKER = "192.168.1.175"
PORT = 1883
TOPIC_SUB = "env/request"
TOPIC_PUB = "env/info"

# Callback appelé lors de la connexion
def on_connect(client, userdata, flags, rc):
    print("Connecté avec le code de retour :", rc)
    client.subscribe(TOPIC_SUB)

# Callback appelé lors de la réception d’un message
def on_message(client, userdata, msg):
    #reset()
    #print(f"Message reçu sur {msg.topic}: {msg.payload.decode()}")

    # Exemple : répondre si le message reçu est "send"
    if msg.payload.decode() == "step":
        env_info = env.capture_screen()
        client.publish(TOPIC_PUB, env_info)
    if msg.payload.decode() == "reset":
        try:
            reset()
        except:
            print("error during reset")
        env_info = env.capture_screen()
        client.publish(TOPIC_PUB, env_info)


# Configuration du client MQTT
client = mqtt.Client()
client.publish("env/info", "hello world")
client.on_connect = on_connect
client.on_message = on_message

# Connexion au broker et boucle principale
client.connect(BROKER, PORT, 60)
client.loop_forever()