import sys
import time
from .run import run_file, test, verify
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

last_trigger = time.time()

class PythonlingsHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global last_trigger
        if "__pycache__" in event.src_path:
            return
        elif (time.time() - last_trigger) > 0.5:
            clean_screen()
            verify(exercises_)
        last_trigger = time.time()

def clean_screen():
    print("\x1Bc")

def watch(exercises):
    clean_screen()
    global exercises_
    exercises_ = exercises
    verify(exercises_)
    try:
        event_handler = PythonlingsHandler()
        observer = Observer()
        observer.schedule(event_handler, path="exercises", recursive=True)
        observer.start()
        observer.join()
    except KeyboardInterrupt:
        sys.exit(1)
