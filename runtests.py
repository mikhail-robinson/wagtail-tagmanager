#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.core.management import call_command
from django.test.utils import get_runner

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "src"))

os.environ["DJANGO_SETTINGS_MODULE"] = "wagtail_tagmanager.test_settings"

django.setup()

call_command("makemigrations", "testapp")
call_command("migrate")

if __name__ == "__main__":
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests"])
    sys.exit(bool(failures))
