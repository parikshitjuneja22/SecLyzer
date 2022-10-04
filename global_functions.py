#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""Global functions to manage the app."""
import click

from seclyzer.app import (
    app,
    db,
)


@click.group()
def cli():
    pass


@cli.command()
def runserver():
    """Run Server."""
    click.echo('Running server....')
    app.run(
        threaded=True,
        debug=False,
        host='127.0.0.1',
        port=9090)


@cli.command()
def initialize_db():
    """initialize a database."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()
        click.echo('Database  Initialized!')


if __name__ == '__main__':
    cli()
