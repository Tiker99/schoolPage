import os
import json

STUDENTS_FILE = 'students.json'
EVENTS_FILE = 'events.json'


def load_students():
    """Load students from the JSON file."""
    if os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_students(students):
    """Save students to the JSON file."""
    with open(STUDENTS_FILE, 'w') as file:
        json.dump(students, file, indent=4)

def load_events():
    """Load events from the JSON file."""
    if os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_events(events):
    """Save events to the JSON file."""
    with open(EVENTS_FILE, 'w') as file:
        json.dump(events, file, indent=4)