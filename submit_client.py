import json
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

import settings


def submit(task_id, endpoint, lesson_file, default_solution=None, argv=None):
    if endpoint is None:
        print(f'Проверка {task_id} пока недоступна в сервисе. '
              'Для этого задания ещё не реализован API.')
        return 1

    args = list(sys.argv[1:] if argv is None else argv)
    bundle = isinstance(default_solution, tuple)
    usage = ('Использование: python submit.py [connection_interests.py run_jobs.sh dag.py]'
             if bundle else 'Использование: python submit.py [путь_к_файлу_решения]')
    if args in (['--help'], ['-h']):
        print(usage)
        return 0
    if (bundle and len(args) not in (0, len(default_solution))) or (not bundle and len(args) > 1):
        print(usage)
        return 1
    if not args and default_solution is None:
        print('Укажите файл с кодом DAG: python submit.py /путь/к/dag.py')
        return 1

    base_url = settings.CHECK_SERVICE_URL.strip().rstrip('/')
    try:
        parsed = urlsplit(base_url)
        valid_url = (parsed.scheme in ('http', 'https') and parsed.hostname
                     and not parsed.query and not parsed.fragment
                     and not parsed.username and not parsed.password)
        parsed.port  # Validate the optional port.
    except ValueError:
        valid_url = False
    if not valid_url:
        print('Укажите в settings.py CHECK_SERVICE_URL — полный адрес сервиса '
              'с http:// или https://, без /api/v1/checks.')
        return 1
    student_id = settings.STUDENT_ID.strip()
    if not student_id:
        print('Укажите в settings.py STUDENT_ID — ваш учебный логин.')
        return 1

    names = default_solution if bundle else (default_solution,)
    paths = ([Path(arg).expanduser() for arg in args] if args else
             [Path(lesson_file).resolve().parent / name for name in names])
    contents = []
    for solution_path in paths:
        try:
            text = solution_path.read_text(encoding='utf-8')
        except (OSError, UnicodeError) as exc:
            print(f'Не удалось прочитать файл решения {solution_path}: {exc}')
            return 1
        if not text.strip():
            print(f'Файл решения {solution_path} пуст.')
            return 1
        contents.append(text)
    solution = (json.dumps(dict(zip(names, contents)), ensure_ascii=False)
                if bundle else contents[0])

    request = Request(
        base_url + endpoint,
        data=json.dumps({'student_id': student_id,
                         'student_solution': solution}).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    print(f'Проверяется задание {task_id}. Дождитесь результата...')
    try:
        with urlopen(request, timeout=300) as response:
            result = json.load(response)
    except HTTPError as exc:
        print(f'Сервис проверки вернул HTTP {exc.code}. '
              'Проверьте адрес сервиса и повторите отправку.')
        return 1
    except (URLError, TimeoutError, OSError):
        print('Не удалось связаться с сервисом проверки или истекло время ожидания. '
              'Проверьте подключение и повторите отправку.')
        return 1
    except (ValueError, UnicodeError):
        print('Сервис вернул некорректный JSON-ответ.')
        return 1

    if (not isinstance(result, dict)
            or result.get('status') not in ('success', 'error')
            or not isinstance(result.get('message'), str)):
        print('Неожиданный формат ответа сервиса: ожидаются status и message.')
        return 1
    # The API returns the platform code inside message, not in a separate field.
    print(result['message'])
    return 0 if result['status'] == 'success' else 1
