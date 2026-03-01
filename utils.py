def open_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

    except PermissionError:
        print(f"Permission denied for file: {file_path}")
        return None
    
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None