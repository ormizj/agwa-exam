from datetime import datetime

def get_current_timestamp():
    return datetime.now().strftime('%Y-%m-%d_%H-%M-%S_%f')
