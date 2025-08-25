import json

def save_data(file_path, table_data):
    """
    Saves spreadsheet data to a .pyxxell file in JSON format.

    The .pyxxell format is a JSON array where each object represents a cell
    and contains 'row', 'col', and 'text' keys.

    Args:
        file_path (str): The path to save the file to.
        table_data (list): A list of dictionaries representing the cell data.
    """
    try:
        with open(file_path, 'w') as f:
            json.dump(table_data, f, indent=4)
    except IOError as e:
        print(f"Error saving file: {e}")

def load_data(file_path):
    """
    Loads spreadsheet data from a .pyxxell file.

    Args:
        file_path (str): The path of the file to load.

    Returns:
        list: A list of dictionaries representing the cell data, or an empty list
              if the file is not found or contains invalid data.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading file: {e}")
        return []
