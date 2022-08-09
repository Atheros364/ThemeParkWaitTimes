from ThemeParkTimeInjestor import *

def main():
    print("Starting injestor")
    path = input("Enter path to data folder: ")#S:/Projects/Programming Projects/ThemeParkTimeInjestor/TestOutput

    injestor = ThemeParkTimeInjestor(path)
    injestor.StartDataCollection()

if __name__ == '__main__':
    main()