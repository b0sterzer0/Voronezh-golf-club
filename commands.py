import click

import golf
from golf.models import db


@click.command('create_db')
def create_db():
    db.create_all()


@click.command('runserver')
def runserver():
    golf.app.run(host='127.0.0.1', port=8000, debug=True)
