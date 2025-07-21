# utils.py - Our handy helper functions that make life easier

# We need the json library to read JSON files (that's where our data lives)
import json

def load_json(filepath):
    """Load JSON file from given filepath"""
    # This function is like a file opener specifically for JSON files
    # It takes a file path, opens the file, reads all the JSON data, and gives it back to us as Python objects
    with open(filepath, 'r') as file:  # Open the file in read mode ('r' means read-only)
        return json.load(file)  # Parse the JSON and convert it to Python dictionaries and lists
