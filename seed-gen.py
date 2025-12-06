import json
import random
import string
import os

def rand_string():
    return ''.join(random.choice(string.ascii_letters) for _ in range(6))

def rand_value(depth=0):
    if depth > 3:
        return random.choice([1, "x", True, None])
    t = random.choice(["obj", "array", "str", "num"])
    if t == "obj":
        return {rand_string(): rand_value(depth+1) for _ in range(random.randint(1, 4))}
    if t == "array":
        return [rand_value(depth+1) for _ in range(random.randint(1, 4))]
    if t == "str":
        return rand_string()
    if t == "num":
        return random.randint(0, 100)

os.makedirs("seeds", exist_ok=True)

for i in range(200):
    with open(f"seeds/{i}.json", "w") as f:
        json.dump(rand_value(), f)
