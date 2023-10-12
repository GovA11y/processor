# run.py
from app import startup
from app.processes import start_processes

def main():
    startup()
    start_processes()

if __name__ == '__main__':
    main()
