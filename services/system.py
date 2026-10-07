import subprocess

def run(cmd: str):
    subprocess.run(cmd, shell=True)
