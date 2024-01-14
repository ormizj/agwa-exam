import uuid
import re

def create_uuid()->str:
    return uuid.uuid4().hex

def sanitize_filename(filename)->str:
    # remove invalid characters from filename (only allow alphanumeric, space, dash, and parenthesis)
    invalid_chars_pattern = r"[^-\w\s()]"
    sanitized_name = re.sub(invalid_chars_pattern, '', filename)
    
    # check long file name and shorten it if needed
    max_length = 100
    if len(sanitized_name) > max_length:
        sanitized_name = sanitized_name[:max_length]
        
    return sanitized_name