import json
import logging
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime
from uuid import uuid4
from zoneinfo import ZoneInfo

ADMIN_DIR = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = ADMIN_DIR.parent / 'WildTrace'
if not (DEFAULT_ROOT / 'src/app.py').is_file():
    DEFAULT_ROOT = ADMIN_DIR.parent
WILDTRACE_ROOT = Path(os.environ.get('WILDTRACE_ROOT', str(DEFAULT_ROOT))).resolve()


def _new_log_file():
    now = datetime.now()
    return WILDTRACE_ROOT / 'logs' / (
        f'wildtrace-{now:%Y-%m-%d-%H-%M-%S}-{now.microsecond // 1000:03d}.log'
    )


def _log(message, log_file, raw=False):
    folder = WILDTRACE_ROOT / 'logs'
    try:
        folder.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(log_file, encoding='utf-8')
        try:
            handler.setFormatter(logging.Formatter(
                '%(message)s' if raw else '%(asctime)s | WildTrace | %(levelname)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'))
            handler.handle(logging.LogRecord('WildTrace', logging.INFO,
                                            __file__, 0, message, (), None))
        finally:
            handler.close()
    except OSError:
        logging.getLogger(__name__).exception('Écriture des logs WildTrace impossible')


def _run(arguments):
    script = WILDTRACE_ROOT / 'src/app.py'
    if not script.is_file():
        raise RuntimeError(f'WildTrace introuvable : {script}')
    candidates = [WILDTRACE_ROOT / name / 'bin/python' for name in ('.venv', 'venv')]
    python = next((str(p) for p in candidates if p.is_file()), sys.executable)
    log_file = _new_log_file()
    process_env = os.environ.copy()
    process_env["WILDTRACE_LOG_CAPTURED"] = "1"
    try:
        result = subprocess.run([python, str(script), *arguments], cwd=WILDTRACE_ROOT,
                                capture_output=True, text=True, env=process_env)
    except OSError as exc:
        _log(f'Impossible de lancer WildTrace : {exc}', log_file)
        raise
    if result.stdout:
        _log(result.stdout.rstrip(), log_file, raw=True)
    if result.stderr:
        _log(result.stderr.rstrip(), log_file, raw=True)
    _log(f'Fin WildTrace : code {result.returncode}', log_file)
    if result.returncode:
        raise RuntimeError(result.stderr or result.stdout or 'Échec de WildTrace')


def run_collect(moods: list[str], zone: str, environments: list[str]):
    if not moods:
        raise ValueError('Sélectionne au moins un mood avant de collecter.')
    zone = zone or 'Europe/Paris'
    if sys.platform != 'darwin':
        return _run(['-c', '-m', ','.join(moods), '-z', zone,
                     '-e', ','.join(environments)])
    # Sur Mac, conserver les observations sans dépendre des capteurs du Pi.
    started_at = datetime.now()
    log_file = _new_log_file()
    _log('--------------- WILDTRACE ---------------', log_file)
    _log('----- Data collect mode -----', log_file)
    _log('Collecte sans capteurs : mesures environnementales nulles.', log_file)
    now = datetime.now(ZoneInfo(zone))
    row = {
        'local_timestamp': now.strftime('%Y-%m-%d %H:%M:%S'),
        'timezone': zone,
        **dict.fromkeys(('temperature', 'humidity', 'luminosity',
                         'white_luminosity', 'latitude', 'longitude',
                         'altitude_m', 'concentration_co2')),
        'environments': {f'environment_{i}': value for i, value in enumerate(environments)},
        'moods': {f'mood_{i}': value for i, value in enumerate(moods)},
    }
    folder = WILDTRACE_ROOT / 'data/output/collected/environmental_to_send'
    folder.mkdir(parents=True, exist_ok=True)
    name = f'collect_process_data_{now:%d-%m-%Y-%H-%M-%S-%f}_{uuid4().hex}.json'
    # Une seule écriture durable, avec un nom unique pour chaque observation.
    with (folder / name).open('x', encoding='utf-8') as file:
        json.dump([row], file, ensure_ascii=False, indent=2, allow_nan=False)
        file.flush()
        os.fsync(file.fileno())
    _log(f'Collected data : {row}', log_file)
    _log('----- Writing collected data in JSON format -----', log_file)
    _log(f'File saved under name: {folder / name}', log_file)
    _log('----- End of data collection mode -----', log_file)
    _log(f'Collect duration: {datetime.now() - started_at}', log_file)
    _log('----- End of program -----', log_file)
    return folder / name


def run_send():
    return _run(['-b', 'True'])


def run_compute():
    return _run(['--computed'])


def run_contextualize():
    return _run(['--contextualize'])
