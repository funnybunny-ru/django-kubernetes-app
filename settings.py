import os
from pathlib import Path

def load_vault_secrets():
    vault_secrets_file = Path("/vault/secrets/django-config.sh")
    if vault_secrets_file.exists():
        with open(vault_secrets_file) as f:
            for line in f:
                line = line.strip()
                if line.startswith("export "):
                    var_line = line[7:]
                    if '=' in var_line:
                        key, value = var_line.split('=', 1)
                        value = value.strip('"').strip("'")
                        os.environ.setdefault(key, value)
        print("✅ Секреты загружены из Vault")
    else:
        print("⚠️айл секретов Vault не найден, используем переменные окружения")

load_vault_secrets()

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

if not SECRET_KEY:
    if os.environ.get("DJANGO_ENV") == "production":
        raise ValueError(
            "В production окружении DJANGO_SECRET_KEY должен быть установлен "
            "через Vault или переменные окружения!"
        )
    else:
        SECRET_KEY = "django-insecure-dev-key-change-in-production"
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
if "" in ALLOWED_HOSTS:
    ALLOWED_HOSTS.remove("")
if DEBUG and not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "NAME": os.environ.get("DB_NAME", "django_db"),
        "USER": os.environ.get("DB_USER", "django_user"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "django_pass"),
    }
}
