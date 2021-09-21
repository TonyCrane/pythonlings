import enum
import os, sys, re
import subprocess as sp
from functools import wraps 
import importlib

def run(exercise, verify=False):
    if exercise.mode == "test":
        if not test(exercise, verify):
            if verify:
                return False 
            else:
                sys.exit(1)
        return True
    else:
        if not run_file(exercise, verify):
            if verify:
                return False 
            else:
                sys.exit(1)
        return True

def verify(exercises):
    for exercise in exercises.copy():
        res = run(exercise, True)
        if not res:
            return
        exercises.remove(exercise)
    print("")
    print("🎉 All exercises completed! 🎉")
    print("")
    sys.exit(0)

def find_not_done(exercise):
    with open(exercise.path, "r") as file:
        content = file.read().split("\n")
        for ind, line in enumerate(content):
            if re.match(r'^\s*##*\s*I\s+AM\s+NOT\s+DONE', line, re.I):
                return (ind, content)
        return False

def print_not_done(ind, content):
    print("\n".join([
        "\033[34m{:>2} |\033[0m {}".format(
            i+1, content[i]
        ) for i in range(max(0, ind - 2), ind + 3)
    ]))

def run_file(exercise, verify=False):
    print(f"\033[33m◌\033[0m  Running {exercise.path}...")
    result = sp.run([sys.executable, exercise.path], capture_output=True)
    if result.returncode != 0:
        print(f"\033[31m⚠️  Ran {exercise.path} with errors:\033[0m")
        print(result.stderr.decode('utf-8'))
        return False
    else:
        if verify:
            res = find_not_done(exercise)
            if res:
                print(f"\033[32m✅ Successfully ran {exercise.path}\033[0m")
                print("\nOutput:\n====================")
                print(result.stdout.decode('utf-8'))
                print("====================")
                print("")
                print("You can keep working on this exercise,")
                print("or jump into the next one by removing the `I AM NOT DONE` comment:\n")
                ind, content = res 
                print_not_done(ind, content)
                return False
            else:
                print(f"\033[32m✅ Successfully ran {exercise.path}\033[0m")
                return True
        else:
            print(result.stdout.decode('utf-8'))
            print(f"\033[32m✅ Successfully ran {exercise.path}\033[0m")
        return True

# TODO, use global variable for counting instead of coroutine

def coroutine(func):
    @wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen 
    return primer 

@coroutine
def count_total():
    cnt = 0
    while True:
        rec = yield cnt 
        if rec == 1:
            cnt += 1
        else:
            cnt = 0

@coroutine
def count_failed():
    cnt = 0
    while True:
        rec = yield cnt 
        if rec == 1:
            cnt += 1
        else:
            cnt = 0

total_counter = count_total()
failed_counter = count_failed()

def counter(func):
    @wraps(func)
    def count_func(*args, **kwargs):
        cnt = total_counter.send(1)
        print(f"    Testing task#{cnt}...", end="")
        result = func(*args, **kwargs)
        if result == True:
            print("\033[32mPassed\033[0m")
        else:
            print("\033[31mFailed\033[0m")
            left, right = result 
            print(f"      left  value: {left}")
            print(f"      right value: {right}")
            _ = failed_counter.send(1)
    return count_func

@counter
def test_eq(a, b):
    if a == b:
        return True 
    else:
        return (a, b)

def test(exercise, verify=False):
    print(f"\033[33m◌\033[0m  Running {exercise.path}...")
    sys.path.append("..")
    test_module = importlib.import_module(exercise.path.replace(os.sep, ".").replace(".py", ""))
    test_module = importlib.reload(test_module)
    test_module.test_task()
    total = total_counter.send(1) - 1
    failed = failed_counter.send(1) - 1
    total_counter.send(0)
    failed_counter.send(0)
    if failed == 0:
        if verify:
            res = find_not_done(exercise)
            if res:
                print(f"\033[32m✅ Successfully tested {exercise.path}\033[0m")
                print("")
                print("You can keep working on this exercise,")
                print("or jump into the next one by removing the `I AM NOT DONE` comment:\n")
                ind, content = res 
                print_not_done(ind, content)
                return False
        print(f"\033[32m✅ Successfully tested {exercise.path}\033[0m")
        return True
    else:
        print(f"\033[31m⚠️  Testing of {exercise.path} failed {failed} / {total}\033[0m")
        return False