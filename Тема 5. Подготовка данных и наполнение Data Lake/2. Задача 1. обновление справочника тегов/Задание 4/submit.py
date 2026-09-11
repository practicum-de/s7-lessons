"""Отправка задания de07050204 в сервис проверок."""
from pathlib import Path
import sys

# Корень s7-lessons; работает и при запуске из другого рабочего каталога.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from submit_client import submit

TASK_ID = 'de07050204'
ENDPOINT = '/api/v1/checks/de07050204_joba_find_new_tags/'
DEFAULT_SOLUTION = 'realization.py'

if __name__ == '__main__':
    raise SystemExit(submit(TASK_ID, ENDPOINT, __file__, DEFAULT_SOLUTION))
