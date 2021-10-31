import subprocess
import sys


def django_shell():
    subprocess.call(["python", "manage.py", "shell"])


def kill_ports():
    processes = subprocess.run(["lsof", "-ti", "tcp:8000,8001"], capture_output=True, text=True).stdout.split("\n")[:-1]
    if processes:
        for process in processes:
            subprocess.run(["kill", "-9", process])
    else:
        print("No ports active!!")


def lint():
    subprocess.run(["black", "."])
    subprocess.run(["flake8"])


def manage():
    try:
        args = " ".join(sys.argv[1:])
        if args != "":
            subprocess.run(["python", "manage.py", args])
        else:
            print("Pass arguments after manage")

    except KeyboardInterrupt:
        print("\nKeyboard interrupted!!")


def migrate():
    subprocess.run(["python", "manage.py", "makemigrations"])
    subprocess.run(["python", "manage.py", "migrate"])


def reset_db():
    subprocess.run(["rm", "db.sqlite3"])
    migrate()


def server():
    try:
        subprocess.call("./runserver.sh")
    except KeyboardInterrupt:
        print("\nServer Stopped!!")
