#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Database Model."""
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()


class ScanResults(db.Model):
    __tablename__ = 'seclyzer_results'

    id = db.Column(db.Integer, primary_key=True)  # noqa: A003
    scan_file = db.Column(db.String)
    scan_hash = db.Column(db.String(64), unique=True)
    location = db.Column(db.String)
    nodejs = db.Column(JSON)
    templates = db.Column(JSON)
    files = db.Column(JSON)
    json_name = db.Column(JSON)
    duplication = db.Column(JSON)
    score = db.Column(JSON)
    forks = db.Column(db.Integer)
    watchers = db.Column(db.Integer)
    open_issues = db.Column(db.Integer)
    false_positive = db.Column(JSON)
    not_applicable = db.Column(JSON)
    timestamp = db.Column(db.DateTime())

    def __init__(self,
                 scan_file,
                 scan_hash,
                 location,
                 nodejs,
                 templates,
                 files,
                 json_name,
                 duplication,
                 score,
                 forks,
                 watchers,
                 open_issues,
                 false_positive,
                 not_applicable,
                 timestamp):
        self.scan_file = scan_file
        self.scan_hash = scan_hash
        self.location = location
        self.nodejs = nodejs
        self.templates = templates
        self.files = files
        self.json_name = json_name
        self.duplication = duplication
        self.score = score
        self.forks = forks
        self.watchers = watchers
        self.open_issues = open_issues
        self.false_positive = false_positive
        self.not_applicable = not_applicable
        self.timestamp = timestamp

    def __repr__(self):
        """Repr."""
        return '<id {}>'.format(self.id)
