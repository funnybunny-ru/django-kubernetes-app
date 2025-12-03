import os
import sys


def main():
    """Точка входа для Django-команд."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django-kubernetes-app.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. "
            "Убедись, что Django установлен и доступен в текущем виртуальном окружении."
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
