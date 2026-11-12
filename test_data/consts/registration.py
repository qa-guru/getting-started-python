"""Фиксированные данные тестов регистрации."""

# Ожидаемое сообщение после успешной регистрации.
REGISTRATION_SUCCESS_MESSAGE = "Congratulations! You've registered!"

# Ожидаемая ошибка при несовпадающих паролях.
PASSWORDS_MISMATCH_ERROR = "Passwords should be equal"

# Суффикс, делающий второй пароль отличным от первого.
MISMATCHED_PASSWORD_SUFFIX = "x"

# Шаблон ошибки занятого имени пользователя; {} подставляется имя.
USERNAME_TAKEN_ERROR_TEMPLATE = "Username `{}` already exists"
