import os

def set_current_dir(dir: str = os.path.dirname(os.path.abspath(__file__))) -> str:
    dir = os.path.dirname(dir)
    dir = os.path.join(dir, 'outputs')
    os.makedirs(dir, exist_ok=True)
    return dir

def check_repository(dir: str, name: str) -> None:
    dataset_directory = os.path.join(dir, name)
    if not os.path.exists(dataset_directory):
        os.makedirs(dataset_directory)
    return dataset_directory