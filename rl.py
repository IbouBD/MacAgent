import random
from collections import deque

class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)  # Gestion automatique du débordement
        self.max_capacity = capacity

    def store_transition(self, obs):
        """ Ajoute une transition à la mémoire """
        self.buffer.append(obs)  # Pas besoin de vérifier la capacité grâce à deque

    def push(self, batch_size=1):
        """ Tire un échantillon aléatoire d'expériences """
        if self.capacity() > 0:
            batch_size = min(batch_size, self.capacity())  # Éviter de prélever trop d'éléments
            batch = random.sample(self.buffer, batch_size)
            return batch  # Retourne une liste de transitions
        else:
            return "Replay Buffer is empty"

    def capacity(self):
        """ Retourne le nombre d'éléments stockés """
        return len(self.buffer)
