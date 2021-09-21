import yaml
import re
from enum import Enum 

class State(Enum):
    DONE = 1
    NOTDONE = 0

class Exercise:
    def __init__(self, name, path, mode, hint, state=State.NOTDONE):
        self.name = name 
        self.path = path 
        self.mode = mode 
        self.hint = hint 
        self.state = state 
        self.check_state()
    
    def check_state(self):
        with open(self.path, "r") as file:
            content = file.read()
            if re.search(r'^\s*##*\s*I\s+AM\s+NOT\s+DONE', content, re.M | re.I):
                self.state = State.NOTDONE
            else:
                self.state = State.DONE

def read_exercises(filename):
    with open(filename, 'r') as file:
        res = yaml.load(file, Loader=yaml.SafeLoader)
    exercises = [Exercise(
        name=detail["name"],
        path=detail["path"],
        mode=detail["mode"],
        hint=detail["hint"]
    ) for _, detail in res.items()]
    return exercises
