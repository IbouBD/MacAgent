import paho.mqtt.client as mqtt
from agent import Agent, ast, keyboard, Key
import time

agent = Agent(brain=None)
BROKER = "192.168.1.175"
PORT = 1883
TOPIC_SUB = "env/action"
TOPIC_PUB = "env/response"
action = None

# Callback appelé lors de la connexion
def on_connect(client, userdata, flags, rc):
    print("Connecté avec le code de retour :", rc)
    client.subscribe(TOPIC_SUB)

# Callback appelé lors de la réception d’un message
def on_message(client, userdata, msg):
    global action
    action = msg.payload.decode()
    #print(f"Message reçu sur {msg.topic}: {action}")
    action_sequence = ast.literal_eval(action)
    agent.step_action(action_sequence)
    time.sleep(0.5)
    keyboard.press(Key.esc)
    time.sleep(0.5)
    keyboard.press(Key.esc)
    client.publish(TOPIC_PUB, "msg")
    


# Configuration du client MQTT
client = mqtt.Client()
client.publish("env/info", "hello world")
client.on_connect = on_connect
client.on_message = on_message

# Connexion au broker et boucle principale
client.connect(BROKER, PORT, 60)
client.loop_forever()