import os

def checkdataset():
    if not os.path.exists('dataset'):
        os.makedirs('dataset')

def main():
    checkdataset()

if __name__ == "__main__":
    main()