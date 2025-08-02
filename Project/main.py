import os
from env import Env
from utils import translate
from model import Actor, VisionActor, device

os.environ["TOKENIZERS_PARALLELISM"] = "false"
dim, hidden, vocab_size, in_channels = 512, 512, 1949, 1
vision = True
env = Env("macos")

current_info, vm_screenshot = env.reset()
instruction = "Open spotify"
state = [{
    "instruction": instruction,
    "active_app": current_info['open_apps'],
    "focused_element": current_info['focused_app'],
}]

if vision==True:
    model = VisionActor(in_channels, dim, hidden, vocab_size).to(device)
    action_id, mousse_pos = model.generate(state)
    action = translate(action_id[0])
else:
    model = Actor(dim, hidden, vocab_size).to(device)
    action_id = model.generate(state)
    action = translate(action_id[0])


print(action)
env.step(action)