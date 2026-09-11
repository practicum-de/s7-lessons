import contextlib
import io
import json
from pathlib import Path
import runpy
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import submit_client


class SubmitClientTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.lesson = Path(self.temp.name) / 'submit.py'
        self.solution = self.lesson.with_name('realization.txt')
        self.solution.write_text('Решение\nprint(1)', encoding='utf-8')
        self.output = io.StringIO()
        self.enterContext(contextlib.redirect_stdout(self.output))
        self.enterContext(patch.object(submit_client.settings, 'CHECK_SERVICE_URL', 'https://checks.example.test/'))
        self.enterContext(patch.object(submit_client.settings, 'STUDENT_ID', 'student-login'))
        self.network = self.enterContext(patch.object(submit_client, 'urlopen'))
        self.reply({'status': 'success', 'message': 'Задание выполнено. Ваш код: test-code'})

    def reply(self, value):
        self.network.return_value = io.BytesIO(json.dumps(value).encode())

    def submit(self, **kwargs):
        options = dict(task_id='de07040401',
                       endpoint='/api/v1/checks/de07040401_create_data_frame/',
                       lesson_file=self.lesson, default_solution='realization.txt', argv=[])
        options.update(kwargs)
        return submit_client.submit(**options)

    def test_success_request_and_code(self):
        self.assertEqual(self.submit(), 0)
        request = self.network.call_args.args[0]
        self.assertEqual(request.full_url, 'https://checks.example.test/api/v1/checks/de07040401_create_data_frame/')
        self.assertEqual(request.get_method(), 'POST')
        self.assertEqual(request.get_header('Content-type'), 'application/json')
        self.assertEqual(json.loads(request.data), {
            'student_id': 'student-login', 'student_solution': 'Решение\nprint(1)'})
        self.assertIn('test-code', self.output.getvalue())

    def test_three_file_bundle(self):
        names = ('connection_interests.py', 'run_jobs.sh', 'dag.py')
        for name in names:
            self.lesson.with_name(name).write_text(name + '\n# текст', encoding='utf-8')
        self.assertEqual(self.submit(default_solution=names), 0)
        request = self.network.call_args.args[0]
        bundle = json.loads(json.loads(request.data)['student_solution'])
        self.assertEqual(bundle, {name: name + '\n# текст' for name in names})

    def test_bundle_explicit_paths_and_invalid_count(self):
        names = ('connection_interests.py', 'run_jobs.sh', 'dag.py')
        for args in ([str(self.solution)], [str(self.solution)] * 2):
            self.assertEqual(self.submit(default_solution=names, argv=args), 1)
            self.network.assert_not_called()
        self.assertEqual(self.submit(default_solution=names, argv=[str(self.solution)] * 3), 0)
        bundle = json.loads(json.loads(self.network.call_args.args[0].data)['student_solution'])
        self.assertEqual(set(bundle), set(names))

    def test_solution_error(self):
        self.reply({'status': 'error', 'message': 'Исправьте решение'})
        self.assertEqual(self.submit(), 1)
        self.assertIn('Исправьте решение', self.output.getvalue())

    def test_explicit_dag_path(self):
        self.assertEqual(self.submit(default_solution=None, argv=[str(self.solution)]), 0)

    def test_dag_requires_file(self):
        self.assertEqual(self.submit(default_solution=None), 1)
        self.network.assert_not_called()

    def test_missing_endpoint(self):
        self.assertEqual(self.submit(endpoint=None), 1)
        self.network.assert_not_called()

    def test_missing_or_empty_or_non_utf8_file(self):
        for data in (None, b'', b'\xff'):
            with self.subTest(data=data):
                if data is None:
                    self.solution.unlink()
                else:
                    self.solution.write_bytes(data)
                self.assertEqual(self.submit(), 1)
                self.network.assert_not_called()

    def test_invalid_settings(self):
        for url in ('', 'xx.xx.xx.xx', 'file:///tmp/checks', 'https://checks.test:bad',
                    'https://checks.test/?query=yes', 'https://name:password@checks.test'):
            with self.subTest(url=url), patch.object(submit_client.settings, 'CHECK_SERVICE_URL', url):
                self.assertEqual(self.submit(), 1)
                self.network.assert_not_called()
        with patch.object(submit_client.settings, 'STUDENT_ID', ''):
            self.assertEqual(self.submit(), 1)
            self.network.assert_not_called()

    def test_network_errors(self):
        for error in (HTTPError('https://checks.test', 422, 'Invalid', {}, None),
                      HTTPError('https://checks.test', 500, 'Internal', {}, None),
                      URLError('offline'), TimeoutError()):
            with self.subTest(error=error):
                self.network.side_effect = error
                self.assertEqual(self.submit(), 1)

    def test_invalid_json(self):
        self.network.return_value = io.BytesIO(b'<html>Error</html>')
        self.assertEqual(self.submit(), 1)

    def test_invalid_response_shape(self):
        for value in ([], {}, {'status': 'unknown', 'message': 'test'},
                      {'status': 'success', 'message': None}):
            with self.subTest(value=value):
                self.reply(value)
                self.assertEqual(self.submit(), 1)

    def test_help(self):
        self.assertEqual(self.submit(argv=['--help']), 0)
        self.network.assert_not_called()

    def test_every_wrapper_dispatches_its_task(self):
        wrappers = sorted(ROOT.glob('Тема */*/Задание */submit.py'))
        self.assertEqual(len(wrappers), 35)
        for wrapper in wrappers:
            with self.subTest(wrapper=wrapper):
                constants = runpy.run_path(str(wrapper))
                with patch.object(submit_client, 'submit', return_value=0) as send:
                    with self.assertRaises(SystemExit) as result:
                        runpy.run_path(str(wrapper), run_name='__main__')
                    self.assertEqual(result.exception.code, 0)
                    send.assert_called_once_with(constants['TASK_ID'], constants['ENDPOINT'],
                                                 str(wrapper), constants['DEFAULT_SOLUTION'])


if __name__ == '__main__':
    unittest.main()
