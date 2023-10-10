import os

class DirectoryHandler:
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

    def print_csv_dir_tree(self, dir: str, file_extension: str = '.csv', tab: str = '') -> None:
        print(tab + os.path.basename(dir) + '/')
        tab += '    '
        for path in sorted(os.listdir(dir)):
            full_path = os.path.join(dir, path)
            if os.path.isfile(full_path) and full_path.endswith(file_extension):
                print(tab + os.path.basename(full_path))
            elif os.path.isdir(full_path):
                self.print_csv_dir_tree(full_path, file_extension, tab)