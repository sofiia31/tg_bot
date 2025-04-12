import json
import os
from config import logger

def save_to_json(user_id, selection, filename='selected_objects.json'):
    """Save selected data to JSON file"""
    data = {}
    
    # Try to read existing data if file exists
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as file:
                file_content = file.read().strip()
                if file_content:  # Check if file is not empty
                    data = json.loads(file_content)
                    # Ensure data is a dictionary
                    if not isinstance(data, dict):
                        logger.warning(f"Existing data is not a dictionary. Creating new.")
                        data = {}
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.error(f"Error reading JSON: {e}")
            data = {}
    
    # Convert user_id to string for JSON compatibility
    user_id_str = str(user_id)
    
    # Initialize user entry if not exists
    if user_id_str not in data:
        data[user_id_str] = []
    
    # Add new selection
    data[user_id_str].append(selection)
    
    # Save updated data
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        logger.error(f"Error saving JSON: {e}")
        return False