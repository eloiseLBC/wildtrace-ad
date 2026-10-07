from services.system import run

WILDTRACE_PY = "/home/eloise/Desktop/WildTrace/src/app.py"
PYTHON = "/home/eloise/Desktop/WildTrace/venv/bin/python"

def run_collect(moods: list[str], zone: str, environments: list[str]):
    mood_arg = ",".join(moods)
    environment_arg = ",".join(environments)
    run(
        f"{PYTHON} {WILDTRACE_PY} -c True -m '{mood_arg}' -z '{zone}' -e '{environment_arg}'"
    )

def run_send():
    run(
        f"{PYTHON} {WILDTRACE_PY} -b True"
    )
    
def run_compute():
    run(
        f"{PYTHON} {WILDTRACE_PY} --computed True"
    )
    
def run_contextualize():
    run(
        f"{PYTHON} {WILDTRACE_PY} --contextualize True"
    )
