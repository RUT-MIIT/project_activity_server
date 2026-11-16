import os
import subprocess
import sys

import pytest


STARTUP_CHECK = (
    "import dotenv; "
    "dotenv.load_dotenv = lambda *args, **kwargs: False; "
    "from config import settings; "
    "import os; "
    "assert settings.SECRET_KEY == os.environ['SECRET_KEY']"
)


def run_settings_import(secret_key):
    env = os.environ.copy()
    if secret_key is None:
        env.pop("SECRET_KEY", None)
    else:
        env["SECRET_KEY"] = secret_key
    return subprocess.run(
        [sys.executable, "-c", STARTUP_CHECK],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def test_settings_use_secret_key_from_environment():
    result = run_settings_import("test-only-signing-key")
    assert result.returncode == 0
    assert "test-only-signing-key" not in result.stdout + result.stderr


@pytest.mark.parametrize("secret_key", [None, "", "   "])
def test_settings_reject_missing_or_empty_secret_key(secret_key):
    result = run_settings_import(secret_key)
    assert result.returncode != 0
    assert "SECRET_KEY must be set in the environment" in result.stderr
