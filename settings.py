import os

# Адрес единого сервиса с http:// или https://, без /api/v1/checks.
# Значение сообщает команда курса после публикации сервиса.
CHECK_SERVICE_URL = os.environ.get('CHECK_SERVICE_URL', 'https://de-sp7-checks.de.education-services.ru')

# Ваш учебный логин со страницы `cloud-infra.de.education-services.ru` начинающийся с `s`.
STUDENT_ID = os.environ.get('STUDENT_ID', '')
