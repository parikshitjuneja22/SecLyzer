#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Settings for seclyzer."""
from pathlib import Path

# GENERAL
VERSION = '4.7'
UPLOAD_FOLDER = Path('~/.seclyzer/').expanduser().as_posix()
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
UPLD_MIME = [
    'application/zip',
    'application/octet-stream',
    'application/x-zip-compressed',
    'binary/octet-stream',
]
IGNORE_PATHS = ('.git', '.DS_Store')
CHECK_MUST_HAVE = True

# Postgres DB Connection URL
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin123@127.0.0.1/mydb'

# Get Email alerts
NJS_FROM_EMAIL = ''
NJS_TO_EMAIL = ''
SMTP_SERVER = ''
SMTP_PORT = None
SMTP_STARTTLS = False
SMTP_USER = ''
SMTP_PASS = ''